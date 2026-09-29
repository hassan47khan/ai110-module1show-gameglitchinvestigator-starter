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
- [x] Detail which bugs you found.

Bugs
logic_utils.py:26: crash on some inputs. The except only catches TypeError and ValueError. Typing 1.0e999 makes float() return infinity, and int(inf) raises OverflowError. I ran it and the app would crash. Add OverflowError to the tuple.

app.py:91-98 and logic_utils.py:12-29: no range check. A guess of -500 or 9999 is accepted, counts as an attempt and costs points, even though the game says "between 1 and 20". parse_guess doesn't know low and high, so the check needs to go there (with new parameters) or in app.py.

app.py:57-67: stale display. "Attempts left" and the Debug Info panel (attempts, score, history) render before the submit is processed. After each guess they are one step behind until the next interaction. Move that display below the if submit: block, or call st.rerun() after processing.

logic_utils.py:8 with app.py:30-34: difficulty makes no sense. Hard is 1–50 with 5 attempts, which is easier than Normal at 1–100 with 8. Easy gets only 6 attempts, fewer than Normal. Hard should have the widest range. The test at test_game_logic.py:122-123 asserts (1, 50), so it would need updating too.

- [x] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
platform win32 -- Python 3.13.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Codepath\CodePath assignments\Game Glitch Investigator\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.12.1
collected 29 items                                                                                                                        
tests\test_game_logic.py .............................                                                                              [100%]
=========================================================== 29 passed in 0.04s ===========================================================


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
