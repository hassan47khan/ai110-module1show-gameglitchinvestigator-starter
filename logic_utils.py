DIFFICULTY_SETTINGS = {
    "Easy": {"range": (1, 20), "attempts": 8},
    "Normal": {"range": (1, 100), "attempts": 10},
    "Hard": {"range": (1, 200), "attempts": 8},
}
DEFAULT_DIFFICULTY = "Normal"


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])["range"]


def get_attempt_limit(difficulty: str):
    """Return the number of guesses allowed for a given difficulty."""
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])["attempts"]


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    If low and high are given, the guess must fall within that inclusive range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (TypeError, ValueError, OverflowError):
        return False, None, "That is not a number."

    if low is not None and high is not None and not low <= value <= high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
