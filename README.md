# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

  A Streamlit number-guessing game. The player picks a difficulty, and the game chooses a secret number in that difficulty's range. The player has a limited number of attempts, gets a Higher or Lower hint after each guess, and earns a score that rewards winning in fewer attempts.

- [x] Detail which bugs you found.

  **Original starter bugs**

  - **Hints swapped** (`check_guess`): a guess above the secret said "Go HIGHER!" and a guess below it said "Go LOWER!".
  - **Secret converted to a string:** on every even attempt the secret was cast with `str()`, so the comparison was wrong and a correct guess could fail to win.
  - **Scoring errors** (`update_score`): a wrong "Too High" guess *added* 5 points on even attempts, and a win was scored with `attempt_number + 1`.
  - **Attempts counter started at 1:** so the game showed one attempt too few.
  - **New Game broken:** it ignored the difficulty (hardcoded `random.randint(1, 100)`) and didn't reset `status`, score or history, so the game stayed locked after a win or loss.
  - **Other state bugs:** the instructions always said "between 1 and 100", changing difficulty didn't restart the game, and a blank or invalid guess still used up an attempt.

  **Found in a second review**

  - **Crash on some inputs** (`logic_utils.py:26`): the `except` only caught `TypeError` and `ValueError`. Typing `1.0e999` makes `float()` return infinity, and `int(inf)` raises `OverflowError`, so the app would crash. Fix: add `OverflowError` to the tuple.
  - **No range check** (`app.py:91-98`, `logic_utils.py:12-29`): a guess of `-500` or `9999` was accepted, counted as an attempt and cost points, even though the game says "between 1 and 20". `parse_guess` didn't know `low` and `high`, so the check needs to go there (with new parameters) or in `app.py`.
  - **Stale display** (`app.py:57-67`): "Attempts left" and the Debug Info panel (attempts, score, history) rendered before the submit was processed, so after each guess they were one step behind until the next interaction. Fix: move that display below the `if submit:` block, or call `st.rerun()` after processing.
  - **Difficulty made no sense** (`logic_utils.py:8`, `app.py:30-34`): Hard was 1–50 with 5 attempts, easier than Normal at 1–100 with 8, and Easy got only 6 attempts, fewer than Normal. Hard should have the widest range. The test at `test_game_logic.py:122-123` asserted `(1, 50)`, so it needed updating too.

- [x] Explain what fixes you applied.

  - **Logic moved into `logic_utils.py`:** `check_guess` always compares integers and returns only the outcome string, with the hint text corrected in `app.py`. `update_score` now applies a flat 5-point penalty for any wrong guess and scores a win from the real attempt number.
  - **Difficulty settings in one table:** `DIFFICULTY_SETTINGS` holds each range and attempt limit, with a new `get_attempt_limit()`. Easy is 1–20 with 8 attempts, Normal is 1–100 with 10, and Hard is 1–200 with 8, so Hard is now the widest range.
  - **Safer input handling:** `parse_guess` catches `OverflowError`, treats whitespace-only input as empty, and takes optional `low` and `high` so out-of-range guesses are rejected without using an attempt.
  - **State handling in `app.py`:** `start_new_game(low, high)` resets everything and uses the correct range. It also runs when the difficulty changes. Attempts now start at 0.
  - **Callbacks instead of inline processing:** Submit and New Game run as button callbacks, so attempts, score and history update before the page draws. Feedback is stored in `session_state`, so the "New game started." message now shows.
  - **Cleaner behavior:** only valid guesses go into history, the "Correct!" hint no longer shows as a yellow warning, and the input and Submit button are disabled when the game ends.
  - **Tests:** the pytest suite grew to 29 tests covering scoring, parsing, range validation, overflow and difficulty settings.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py`. Choose a difficulty in the sidebar. The range and number of attempts shown update to match.
2. Type a guess into the box and click **Submit Guess**. The "Attempts left" counter drops right away.
3. Read the hint. "Go HIGHER!" means the secret is above your guess and "Go LOWER!" means it is below.
4. Try `0` or `9999`, or type text like `banana`. The game shows an error and does not use an attempt.
5. Keep guessing until you win (the game shows your score and balloons) or run out of attempts. The input then locks. Click **New Game** to start a fresh round in the same difficulty.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
platform win32 -- Python 3.13.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Codepath\CodePath assignments\Game Glitch Investigator\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.12.1
collected 29 items
tests\test_game_logic.py .............................                                                                              [100%]
=========================================================== 29 passed in 0.04s ===========================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
