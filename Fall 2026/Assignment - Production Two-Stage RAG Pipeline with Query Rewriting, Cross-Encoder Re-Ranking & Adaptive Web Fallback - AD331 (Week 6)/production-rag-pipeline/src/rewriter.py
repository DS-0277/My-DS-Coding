"""Query transformation with a deterministic fallback for local development."""

import re

from .settings import OPENAI_REWRITER_MODEL, RAG_MODE


class QueryRewriter:
    """Rewrite conversational input while preserving technical identifiers.

    A live LLM adapter can replace ``rewrite`` later. The local implementation
    is intentionally deterministic so Step 2 works without an API key.
    """

    def rewrite(self, query: str, conversation_context: str | None = None) -> str:
        cleaned = " ".join(query.strip().split())
        if not cleaned:
            raise ValueError("Query cannot be empty")

        if RAG_MODE == "hybrid":
            try:
                from openai import OpenAI

                prompt = f"Rewrite this into one precise search query. Preserve technical names and identifiers.\nContext: {conversation_context or 'none'}\nQuestion: {cleaned}"
                response = OpenAI().chat.completions.create(
                    model=OPENAI_REWRITER_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    timeout=15,
                )
                rewritten = response.choices[0].message.content or cleaned
                return rewritten.strip().rstrip("?.!")
            except Exception:
                pass

        if conversation_context:
            context = " ".join(conversation_context.strip().split())
            if re.search(r"\b(it|its|that|this|they|them|those)\b", cleaned, re.I):
                subject = self._extract_subject(context)
                if subject:
                    cleaned = f"{cleaned} Context subject: {subject}"

        return cleaned.rstrip("?.!")

    @staticmethod
    def _extract_subject(context: str) -> str:
        match = re.search(r"(?:about|for|regarding|using)\s+([^.!?]+)", context, re.I)
        return match.group(1).strip() if match else context[:120]

