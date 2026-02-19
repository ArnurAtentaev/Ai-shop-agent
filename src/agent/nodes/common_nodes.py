import json
import logging

from agent.states import OverallAgentState
from agent.prompts import (
    INTENT_PROMPT,
    MODEL_FALLBACK_PROMPT,
    TOOL_BASE_ANSWER_PROMPT,
    ASK_MISSING_SLOTS_PROMPT,
    NOT_AVAILABLE_PROMPT,
    INSERT_NER_CLASSIFICATION_PROMPT,
    SELECT_NER_CLASSIFICATION_PROMPT,
)
from utils.agent_utils import (
    ner_classification,
    clean_ner_slot_value,
    detect_language,
)
from core.config import support_settings

from langchain_core.prompts import PromptTemplate


logging.basicConfig(level=logging.INFO)

INTENT_TO_MODE = {
    "find_product": "select",
    "find_similar": "select",
    "make_order": "insert",
}

PROMPTS = {
    "select": SELECT_NER_CLASSIFICATION_PROMPT,
    "insert": INSERT_NER_CLASSIFICATION_PROMPT,
}


def intent_classification(
    state: OverallAgentState, intents: dict, models
) -> OverallAgentState:
    if state.waiting_confirmation is True:
        return state

    state.tool_res = None
    state.answer = None

    prompt = PromptTemplate(
        input_variables=["intents", "question"],
        template=INTENT_PROMPT,
    )

    intents_names = intents.keys()
    intent_and_description = {}

    for intent in intents_names:
        intent_and_description[intent] = (
            "description: " + intents[intent]["description"]
        )

    intent_chain = prompt | models["generative_model"]
    intent_result = intent_chain.invoke(
        {
            "intents": intent_and_description,
            "question": state.query,
        },
        temperature=0.0,
    )

    intent = intent_result.content.strip()
    logging.info(f"DEFINED INTENT: {intent}")

    if intent not in intents_names or intent == "did_not_classified":
        state.intent_result = None
        return state

    state.intent_result = intent
    return state


def confirmation_parser_node(state: OverallAgentState) -> OverallAgentState:
    text = state.query.lower().strip()

    if text in (
        "да",
        "yes",
        "иә",
        "подтверждаю",
        "ok",
        "confirm",
        "жақсы",
    ):
        state.confirmation_status = "yes"
        return state

    elif text in ("нет", "no", "жоқ", "отмена", "cancel", "бас тарту"):
        state.confirmation_status = "stop"
        state.waiting_confirmation = False
        state.answer = "Order has been cancelled."
        return state

    else:
        state.confirmation_status = "other"
        state.answer = "Please answer 'yes' or 'no'."
        return state


def intent_dispatcher(state: OverallAgentState) -> OverallAgentState:
    if not state.intent_result:
        state.answer = "I did not understand what you meant."
        return state

    return state


def ner_slots_classification_node(
    state: OverallAgentState, intents: dict, models
) -> OverallAgentState:
    intent = state.intent_result
    schema = intents.get(intent, {}).get("slots")
    logging.info(f"SCHEMA: {schema}")

    state.slots = {slot_name: None for slot_name in schema.get("properties", {}).keys()}
    missing_slots = [slot for slot, value in state.slots.items() if value is None]

    mode = INTENT_TO_MODE.get(intent)
    prompt = PROMPTS.get(mode)

    if missing_slots:
        ner_result_str = ner_classification(
            models["generative_model"],
            selected_prompt=prompt,
            question=state.query,
            schema=schema,
        )

        try:
            slot_values = json.loads(ner_result_str)
        except Exception as e:
            logging.error(f"Failed to parse NER JSON: {e}")
            slot_values = {}

        for slot_name, slot_cfg in schema.get("properties", {}).items():
            raw_value = slot_values.get(slot_name)
            cleaned_value = clean_ner_slot_value(raw_value, slot_cfg)
            state.slots[slot_name] = cleaned_value

        logging.info(f"SLOT VALUES: {state.slots}")
    return state


def ask_missing_slots_node(state: OverallAgentState, models) -> OverallAgentState:
    missing = [
        slot
        for slot, value in state.slots.items()
        if (value is None) or (isinstance(value, list) and len(value) == 0)
    ]

    slots_str = ", ".join(missing)

    prompt = PromptTemplate(
        input_variables=["missing"], template=ASK_MISSING_SLOTS_PROMPT
    )
    chain = prompt | models["generative_model"]

    result = chain.invoke(
        {"missing": slots_str},
        temperature=0.0,
    ).content
    logging.info(f"MISSING: {result}")

    state.answer = result

    return state


def tool_base_answer_node(state: OverallAgentState, models) -> OverallAgentState:
    prompt = PromptTemplate(
        input_variables=["data", "intent"],
        template=TOOL_BASE_ANSWER_PROMPT,
    )

    chain = prompt | models["generative_model"]
    result = chain.invoke(
        {
            "data": state.tool_res,
            "intent": state.intent_result,
        },
        temperature=0.6,
    )

    state.answer = result.content
    return state


def model_fallback_node(state: OverallAgentState, models) -> OverallAgentState:
    if state.intent_result == "make_order":
        prompt = PromptTemplate(
            input_variables=["data"],
            template=NOT_AVAILABLE_PROMPT,
        )
        llm_chain = prompt | models["generative_model"]
        answer = llm_chain.invoke(
            {
                "data": state.tool_res,
            },
            temperature=0.6,
        )

    else:
        prompt = PromptTemplate(
            input_variables=["question", "intent", "slots", "tool_res"],
            template=MODEL_FALLBACK_PROMPT,
        )

        if state.intent_result == "general_question" and state.tool_res is None:
            supp = support_settings.model_dump()
            logging.info(f"SUPPORT: {supp}")

        else:
            supp = None

        llm_chain = prompt | models["generative_model"]
        answer = llm_chain.invoke(
            {
                "query": state.query,
                "intent": state.intent_result,
                "slots": state.slots,
                "tool_res": state.tool_res,
                "support": supp,
            },
            temperature=0.6,
        )

    state.answer = answer.content
    return state


def language_adaptation_node(state: OverallAgentState, models) -> OverallAgentState:
    tokenized = models["seq2seq_tokenizer"](
        state.answer, truncation=True, return_tensors="pt"
    )
    detected_lang = detect_language(state.query)

    if detected_lang is None:
        return state

    generated = models["seq2seq_model"].generate(
        **tokenized,
        forced_bos_token_id=models["seq2seq_tokenizer"].get_lang_id(detected_lang),
        do_sample=False,
    )

    result = models["seq2seq_tokenizer"].decode(generated[0], skip_special_tokens=True)

    state.answer = result
    return state
