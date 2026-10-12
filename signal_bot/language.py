from lingua import Language, LanguageDetectorBuilder

SUPPORTED = [
    Language.GERMAN,
    Language.ENGLISH,
    Language.FRENCH,
    Language.ITALIAN,
    Language.SPANISH,
    Language.DUTCH,
]

# Chat messages are short, so confidences are low. Only the lead over the
# runner-up tells whether the guess is trustworthy.
MIN_WORDS = 2
MIN_LEAD = 0.2

detector = LanguageDetectorBuilder.from_languages(*SUPPORTED).build()


def detect_language_name(text: str) -> str | None:
    """Return the English name of the language of text, or None if unsure."""
    if len(text.split()) < MIN_WORDS:
        return None
    best, runner_up = detector.compute_language_confidence_values(text)[:2]
    if best.value - runner_up.value < MIN_LEAD:
        return None
    return best.language.name.capitalize()
