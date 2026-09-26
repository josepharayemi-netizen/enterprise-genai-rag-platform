import re

INJECTION_PATTERNS = (
    r"ignore (all|any|the|your) (previous|prior|system) instructions",
    r"reveal (the )?(system|developer) prompt",
    r"bypass (the )?(guardrails|policy|security)",
    r"act as (an? )?(unrestricted|unfiltered)",
)

PII_PATTERNS = (
    (re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"), "[EMAIL_REDACTED]"),
    (re.compile(r"\b(?:\+?234|0)[789][01]\d{8}\b"), "[PHONE_REDACTED]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[IDENTIFIER_REDACTED]"),
)


def detect_prompt_injection(text: str) -> bool:
    normalized = " ".join(text.lower().split())
    return any(re.search(pattern, normalized) for pattern in INJECTION_PATTERNS)


def redact_pii(text: str) -> str:
    for pattern, replacement in PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def validate_question(text: str) -> str:
    cleaned = text.strip()
    if not cleaned or len(cleaned) > 2000:
        raise ValueError("question must contain between 1 and 2000 characters")
    if detect_prompt_injection(cleaned):
        raise ValueError("potential prompt injection detected")
    return redact_pii(cleaned)
