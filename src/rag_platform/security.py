import re
import unicodedata

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

ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u2060\ufeff]")
TOKEN = re.compile(r"[a-z0-9]+")
OVERRIDE_TERMS = {"abandon", "bypass", "disable", "discard", "disregard", "evade", "forget", "ignore", "override", "remove"}
CONTROL_TERMS = {
    "constraint", "constraints", "developer", "guardrail", "guardrails", "instruction", "instructions",
    "policy", "policies", "restriction", "restrictions", "rule", "rules", "safeguard", "safeguards", "system",
}
EXFILTRATION_TERMS = {"disclose", "display", "expose", "leak", "print", "repeat", "return", "reveal", "show"}
PROTECTED_TERMS = {"configuration", "developer", "hidden", "instruction", "instructions", "message", "policy", "prompt", "secret", "system"}
REQUEST_PREFIX = re.compile(
    r"^(?:please\s+)?(?:can|could|would|will)?\s*(?:you\s+)?"
    r"(?:abandon|bypass|disable|discard|disregard|evade|forget|ignore|override|remove|"
    r"disclose|display|expose|leak|print|repeat|return|reveal|show)\b"
)


def normalize_security_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).lower()
    normalized = ZERO_WIDTH.sub("", normalized)
    return " ".join(normalized.split())


def detect_prompt_injection(text: str) -> bool:
    normalized = normalize_security_text(text)
    if any(re.search(pattern, normalized) for pattern in INJECTION_PATTERNS):
        return True
    tokens = set(TOKEN.findall(normalized))
    score = 0
    score += 2 * int(bool(tokens & OVERRIDE_TERMS) and bool(tokens & CONTROL_TERMS))
    score += 2 * int(bool(tokens & EXFILTRATION_TERMS) and bool(tokens & PROTECTED_TERMS))
    score += int(bool(REQUEST_PREFIX.search(normalized)))
    score += 3 * int(bool(re.search(r"\b(?:act|pretend|behave) as\b.*\b(?:unfiltered|unrestricted|without safeguards)\b", normalized)))
    return score >= 3


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
