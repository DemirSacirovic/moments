import random
import time


class LLMError(Exception):
    """Raised when the (mock) LLM call fails."""
    pass

def extract_signal(content: str) -> dict:
    """
    Mock LLM that decides if a piece of content is a 'moment that matters'. Returns a dict with score and reasoning. Sometimes fails - by design."""
    #Simulate network latency
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)

    #Simulate 15% failure rate
    if random.random() < 0.15:
        raise LLMError("Mock LLM faield (simulated transient error)")

    # Fake "scoring"
    score = round(random.uniform(0, 1), 2)
    is_moment = score > 0.6
    return {
        "score": score,
        "is_moment": is_moment,
        "reasoning": f"Content length: {len(content)} chars, mock score: {score}",
        "latency_seconds": round(delay, 2),
    }
