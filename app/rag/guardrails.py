from typing import Optional

FINANCE_KEYWORDS = {
    "stock", "market", "equity", "bond", "etf", "index", "nasdaq", "s&p",
    "gdp", "inflation", "cpi", "fed", "interest rate", "macro", "economy",
    "sec", "regulation", "filing", "earnings", "portfolio", "asset", "fund",
    "trade", "price", "yield", "treasury", "fiscal", "monetary", "recession",
    "bull", "bear", "volatility", "hedge", "derivative", "option", "future",
    "dividend", "valuation", "sector", "financial", "investment", "capital",
}

BLOCKED_PATTERNS = [
    "ignore previous", "ignore all", "disregard", "jailbreak",
    "you are now", "act as", "pretend you",
]


class GuardrailError(Exception):
    pass


def check_query(query: str) -> Optional[str]:
    """
    Returns None if query is allowed, or a refusal message string if blocked.
    """
    lowered = query.lower()

    # Prompt injection check
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return "This query cannot be processed."

    # Scope check — must contain at least one finance-related term
    if not any(kw in lowered for kw in FINANCE_KEYWORDS):
        return (
            "I can only answer questions about US financial markets, "
            "macroeconomic indicators, and financial regulations. "
            "Please rephrase your question with a financial focus."
        )

    return None
