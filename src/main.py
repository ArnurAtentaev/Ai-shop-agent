import os
import json
import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from agent.graph import build_graph, gen_png_graph
from core.models import Base, db_helper
from agent.views import agent_router
from database_api import router as router_actions

logging.basicConfig(level=logging.INFO)

load_dotenv(".env")
embed_model_name = os.getenv("EMBEDDING_MODEL")
cross_enc_model_name = os.getenv("CROSS_ENCODER_MODEL")
llm_model_name = os.getenv("LLM_MODEL")
seq2seq_model_name = os.getenv("SEQ2SEQ_MODEL")

OLLAMA_PORT_SERVICE = os.getenv("OLLAMA_PORT_SERVICE")
OLLAMA_URL = f"http://ollama:{OLLAMA_PORT_SERVICE}"


class ModelContainer:
    def __init__(self, models: dict):
        self.models = models

    def __getitem__(self, key):
        if key in self.models:
            return self.models[key]
        else:
            raise KeyError(f"Model '{key}' not found.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

    with open("agent/intents.json") as f:
        app.state.intents = json.load(f)

    logging.info("INITIALIZING EMBEDDING MODEL")
    embedding_model = SentenceTransformer(embed_model_name)
    logging.info("INITIALIZING RERANKER MODEL")
    reranker_model = CrossEncoder(cross_enc_model_name)
    logging.info("INITIALIZING GENERATIVE MODEL")
    generative_model = ChatOllama(model=llm_model_name, base_url=OLLAMA_URL)
    logging.info("INITIALIZING TOKENIZER OF SEQ2SEQ MODEL")
    seq2se2_tokenizer = AutoTokenizer.from_pretrained(seq2seq_model_name)
    logging.info("INITIALIZING SEQ2SEQ MODEL")
    seq2seq_model = AutoModelForSeq2SeqLM.from_pretrained(seq2seq_model_name)

    mapped_model = {
        "embedding_model": embedding_model,
        "reranker_model": reranker_model,
        "generative_model": generative_model,
        "seq2seq_tokenizer": seq2se2_tokenizer,
        "seq2seq_model": seq2seq_model,
    }

    models = ModelContainer(mapped_model)
    app.state.models = models

    app.state.agent_graph = await build_graph(intents=app.state.intents, models=models)
    gen_png_graph(app.state.agent_graph, name_photo="main_graph.png")

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_actions, prefix="/creating_actions")
app.include_router(router=agent_router, prefix="/agent")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
