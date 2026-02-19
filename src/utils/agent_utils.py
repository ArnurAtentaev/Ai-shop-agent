import logging

from mediapipe.tasks import python
from mediapipe.tasks.python import text

from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)


def extract_slots_from_schema(schema: dict) -> list[str]:
    """Рекурсивно извлекает ключи верхнего уровня из JSON-схемы."""
    if not schema or "properties" not in schema:
        return []
    return list(schema["properties"].keys())


def ner_classification(
    model, selected_prompt: str, question: str, schema: dict | None = None
):
    prompt = PromptTemplate(
        input_variables=["slots_list_str", "schema", "question"],
        template=selected_prompt,
    )
    input_vars = {
        "schema": schema,
        "question": question,
    }

    ner_chain = prompt | model

    ner_result = ner_chain.invoke(input_vars, temperature=0.0)
    return ner_result.content


def clean_ner_slot_value(value, slot_cfg):
    if value is None:
        return None

    expected_type = slot_cfg.get("type")

    if expected_type == "string":
        return value if isinstance(value, str) else None

    if expected_type == "number":
        return value if isinstance(value, (int, float)) else None

    if expected_type == "array":
        if not isinstance(value, list):
            return []
        return value

    if expected_type == "object":
        return value if isinstance(value, dict) else None

    return None


def detect_language(sentence) -> str:
    model_path = "./language_detector.tflite"

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = text.LanguageDetectorOptions(
        base_options=base_options,
        score_threshold=0.5,
        category_allowlist=["en", "ru", "kk"],
    )

    with python.text.LanguageDetector.create_from_options(options) as detector:
        detected = detector.detect(sentence)
        if detected.detections:
            lang = detected.detections[0].language_code
            logging.info(f"DETECTED LANGUAGE: {lang}")

            score = detected.detections[0].probability
            logging.info(f"PROBABILITY LANGUAGE SCORES: {score}")
            return lang
        else:
            return None
