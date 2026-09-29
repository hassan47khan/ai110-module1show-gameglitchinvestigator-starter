import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

HINTS = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def start_new_game(low, high):
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.feedback = None
    st.session_state.guess_input = ""


def new_game_clicked(low, high):
    start_new_game(low, high)
    st.session_state.feedback = {"kind": "success", "text": "New game started."}


def submit_clicked(low, high, attempt_limit):
    """Handle a guess. Runs as a button callback, so state is updated before the page renders."""
    ok, guess_int, err = parse_guess(st.session_state.guess_input, low, high)

    if not ok:
        st.session_state.feedback = {"kind": "error", "text": err}
        return

    st.session_state.attempts += 1
    st.session_state.history.append(guess_int)
    st.session_state.guess_input = ""

    secret = st.session_state.secret
    outcome = check_guess(guess_int, secret)
    st.session_state.score = update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
    )

    if outcome == "Win":
        st.session_state.status = "won"
        st.session_state.feedback = {
            "kind": "success",
            "celebrate": True,
            "text": f"You won! The secret was {secret}. Final score: {st.session_state.score}",
        }
    elif st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        st.session_state.feedback = {
            "kind": "error",
            "text": f"Out of attempts! The secret was {secret}. Score: {st.session_state.score}",
        }
    else:
        st.session_state.feedback = {"kind": "hint", "outcome": outcome}


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")
#FIXME : new game message never shows up.
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(low, high)
# FIXME:refactor:invalid input goes into history. Entries like "banana" or "" are appended even though they aren't guesses and don't count as attempts. Only append valid guesses.
st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
#FIXME: wrong message style. the "🎉 Correct!""
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

playing = st.session_state.status == "playing"

st.text_input("Enter your guess:", key="guess_input", disabled=not playing)

col1, col2, col3 = st.columns(3)
with col1:
    st.button(
        "Submit Guess 🚀",
        on_click=submit_clicked,
        args=(low, high, attempt_limit),
        disabled=not playing,
    )
with col2:
    st.button("New Game 🔁", on_click=new_game_clicked, args=(low, high))
with col3:
    show_hint = st.checkbox("Show hint", value=True)

feedback = st.session_state.feedback
if feedback:
    if feedback["kind"] == "hint":
        if show_hint:
            st.warning(HINTS[feedback["outcome"]])
    else:
        getattr(st, feedback["kind"])(feedback["text"])

    if feedback.pop("celebrate", False):
        st.balloons()

if not playing:
    st.info("Game over. Start a new game to play again.")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
