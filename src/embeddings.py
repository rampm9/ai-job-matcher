import os, time, numpy as np
from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError

def _retry(fn, tries=3, base=0.5, factor=2.0):
    for i in range(tries):
        try:
            return fn()
        except (RateLimitError, APIConnectionError, APIStatusError):
            if i == tries - 1:
                raise
            time.sleep(base * (factor ** i))

def _fallback_vec(text: str) -> np.ndarray:
    """Generate deterministic fallback vector"""
    h = abs(hash(text)) % (10**6)
    rng = np.random.default_rng(h)
    return rng.standard_normal(1536)

def embed_func(text: str):
    """
    Returns (vector: np.ndarray, mode: str)
    mode is 'ai-powered' if real embeddings were used, else 'fallback'.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_vec(text), "fallback"

    client = OpenAI(api_key=api_key)
    try:
        resp = _retry(lambda: client.embeddings.create(
            model="text-embedding-3-small",  # cheaper; change to -large if you prefer
            input=text,
            timeout=25
        ))
        vec = np.array(resp.data[0].embedding, dtype=float)
        return vec, "ai-powered"
    except Exception:
        return _fallback_vec(text), "fallback"

def embed_many(texts: list[str]):
    """
    Batch embedding function - more efficient for multiple texts
    Returns (vectors: list[np.ndarray], mode: str)
    """
    if not texts:
        return [], "fallback"
        
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return [_fallback_vec(t) for t in texts], "fallback"
    
    client = OpenAI(api_key=api_key)
    try:
        resp = _retry(lambda: client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
            timeout=25
        ))
        vecs = [np.array(x.embedding, dtype=float) for x in resp.data]
        return vecs, "ai-powered"
    except Exception:
        return [_fallback_vec(t) for t in texts], "fallback"
