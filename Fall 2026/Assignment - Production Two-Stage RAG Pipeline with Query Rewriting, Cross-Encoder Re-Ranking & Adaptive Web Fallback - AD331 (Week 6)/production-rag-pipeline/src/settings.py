"""Runtime settings for local and hybrid execution."""

import os
from dotenv import load_dotenv

load_dotenv()

RAG_MODE = os.getenv("RAG_MODE", "local").lower()
OPENAI_REWRITER_MODEL = os.getenv("OPENAI_REWRITER_MODEL", "gpt-4o-mini")
OPENAI_GENERATOR_MODEL = os.getenv("OPENAI_GENERATOR_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CROSS_ENCODER_MODEL = os.getenv("CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
CROSS_ENCODER_LOGIT_BIAS = float(os.getenv("CROSS_ENCODER_LOGIT_BIAS", "6.0"))
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")

