import os
import asyncio

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

load_dotenv(".env")
embed_model_name = os.getenv("EMBEDDING_MODEL")
cross_enc_model_name = os.getenv("CROSS_ENCODER_MODEL")
llm_model_name = os.getenv("LLM_MODEL")
seq2seq_model_name = os.getenv("SEQ2SEQ_MODEL")

OLLAMA_PORT_SERVICE = os.getenv("OLLAMA_PORT_SERVICE")
OLLAMA_URL = f"http://ollama:{OLLAMA_PORT_SERVICE}"


class ModelGetter:
    def __init__(self, models: dict):
        self.models = models

    def __getitem__(self, key):
        if key in self.models:
            return self.models[key]
        else:
            raise KeyError(f"Model '{key}' not found.")


async def load_models() -> dict:
    loop = asyncio.get_running_loop()
    
    generative_model = ChatOllama(model=llm_model_name, base_url=OLLAMA_URL)

    embedding_model = await loop.run_in_executor(
        None, lambda: SentenceTransformer(embed_model_name)
    )
    reranker_model = await loop.run_in_executor(
        None, lambda: CrossEncoder(cross_enc_model_name)
    )
    seq2seq_tokenizer = await loop.run_in_executor(
        None, lambda: AutoTokenizer.from_pretrained(seq2seq_model_name)
    )
    seq2seq_model = await loop.run_in_executor(
        None, lambda: AutoModelForSeq2SeqLM.from_pretrained(seq2seq_model_name)
    )

    return {
        "embedding_model": embedding_model,
        "reranker_model": reranker_model,
        "generative_model": generative_model,
        "seq2seq_tokenizer": seq2seq_tokenizer,
        "seq2seq_model": seq2seq_model,
    }
