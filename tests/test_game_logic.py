from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_guess_one_above_secret():
    # Off-by-one above the secret should still read as too high
    result = check_guess(51, 50)
    assert result == "Too High"

def test_guess_one_below_secret():
    # Off-by-one below the secret should still read as too low
    result = check_guess(49, 50)
    assert result == "Too Low"

def test_guess_with_negative_numbers():
    # Comparisons should hold for negative guesses/secrets too
    assert check_guess(-5, -10) == "Too High"
    assert check_guess(-10, -5) == "Too Low"
    assert check_guess(-3, -3) == "Win"

def test_guess_at_boundary_values():
    # Boundary values (e.g. edges of the Easy/Hard ranges) should compare correctly
    assert check_guess(1, 1) == "Win"
    assert check_guess(100, 1) == "Too High"
    assert check_guess(1, 100) == "Too Low"


# --- parse_guess ---

def test_parse_guess_valid_integer_string():
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_guess_truncates_decimal_string():
    ok, value, error = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_guess_empty_string():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_guess_none_input():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_guess_non_numeric_string():
    ok, value, error = parse_guess("banana")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

def test_parse_guess_negative_integer_string():
    ok, value, error = parse_guess("-7")
    assert ok is True
    assert value == -7
    assert error is None


# --- update_score ---

def test_update_score_win_early_attempt():
    # Winning on attempt 1 should score higher than winning later
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score == 90

def test_update_score_win_never_drops_below_ten_points():
    # Even after many attempts, a win should never be worth less than 10 points
    score = update_score(current_score=0, outcome="Win", attempt_number=50)
    assert score == 10

def test_update_score_too_high_penalizes_consistently():
    # "Too High" should always subtract points, regardless of attempt number parity
    assert update_score(current_score=50, outcome="Too High", attempt_number=1) == 45
    assert update_score(current_score=50, outcome="Too High", attempt_number=2) == 45

def test_update_score_too_low_penalizes():
    score = update_score(current_score=50, outcome="Too Low", attempt_number=3)
    assert score == 45

def test_update_score_unknown_outcome_leaves_score_unchanged():
    score = update_score(current_score=50, outcome="Something Else", attempt_number=1)
    assert score == 50


# --- get_range_for_difficulty ---

def test_range_for_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_for_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_for_hard():
    assert get_range_for_difficulty("Hard") == (1, 200)

def test_hard_range_is_widest():
    sizes = {d: get_range_for_difficulty(d)[1] for d in ("Easy", "Normal", "Hard")}
    assert sizes["Easy"] < sizes["Normal"] < sizes["Hard"]

def test_attempt_limits():
    assert get_attempt_limit("Easy") == 8
    assert get_attempt_limit("Normal") == 10
    assert get_attempt_limit("Hard") == 8

def test_attempt_limit_unknown_difficulty_defaults_to_normal():
    assert get_attempt_limit("Nightmare") == 10


# --- parse_guess range / overflow ---

def test_parse_guess_infinite_float_does_not_crash():
    ok, value, error = parse_guess("1.0e999")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

def test_parse_guess_whitespace_only():
    ok, _, error = parse_guess("   ")
    assert ok is False
    assert error == "Enter a guess."

def test_parse_guess_out_of_range_rejected():
    assert parse_guess("0", 1, 20)[0] is False
    assert parse_guess("21", 1, 20)[0] is False
    assert parse_guess("-500", 1, 20)[0] is False
    ok, value, error = parse_guess("21", 1, 20)
    assert value is None
    assert error == "Guess must be between 1 and 20."

def test_parse_guess_range_edges_accepted():
    assert parse_guess("1", 1, 20) == (True, 1, None)
    assert parse_guess("20", 1, 20) == (True, 20, None)

def test_range_for_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Nightmare") == (1, 100)
