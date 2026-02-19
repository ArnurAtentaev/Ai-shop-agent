# import os
# from dotenv import load_dotenv
# 
# from langchain_ollama import ChatOllama
# from sentence_transformers import CrossEncoder
# from sentence_transformers import SentenceTransformer
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# 
# load_dotenv(".env")
# embed_model = os.getenv("EMBEDDING_MODEL")
# cross_enc_model = os.getenv("CROSS_ENCODER_MODEL")
# llm_model = os.getenv("LLM_MODEL")
# seq2seq_model = os.getenv("SEQ2SEQ_MODEL")
# 
# OLLAMA_PORT_SERVICE = os.getenv("OLLAMA_PORT_SERVICE")
# OLLAMA_URL = f"http://ollama:{OLLAMA_PORT_SERVICE}"
# 
# embedding_model = SentenceTransformer(embed_model)
# 
# reranker_model = CrossEncoder(cross_enc_model)
# 
# generative_model = ChatOllama(model=llm_model, base_url=OLLAMA_URL)
# 
# seq2seq_tokenizer = AutoTokenizer.from_pretrained(seq2seq_model)
# seq2seq_model = AutoModelForSeq2SeqLM.from_pretrained(seq2seq_model)
