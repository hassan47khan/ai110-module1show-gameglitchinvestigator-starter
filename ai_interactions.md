# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->
I first described the problems I faced when I was testing the game. For example, I couldn't reset the game when I clicked "New game". I also found out that "New Game" ignores difficulty, lines 136 in app.py hardcodes random.randint(1, 100) instead of using get_range_for_difficulty(difficulty). In conclusion, I gave the agent of analyzing these problems with addition of asking it to find more problems.

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->
Files edited:

logic_utils.py — replaced the four stub functions (which all raised NotImplementedError) with working implementations refactored out of app.py:

get_range_for_difficulty — returns the (low, high) range per difficulty
parse_guess — validates/parses the text input into an int
check_guess — now returns just the outcome string ("Win"/"Too High"/"Too Low"), fixed to always compare against the real int secret (no more int/str comparison bug)
update_score — removed the parity-based (attempt_number % 2) scoring inconsistency
app.py — rewrote to:

Import the four functions from logic_utils instead of redefining them
Add a HINTS dict with the corrected hint text (original had "Go HIGHER!"/"Go LOWER!" swapped)
Add a start_new_game() helper that resets secret, attempts, score, status, and history together (fixes "New Game" leaving status as "won"/"lost", which permanently locked the game via st.stop())
Use the difficulty-correct low/high range when generating a new secret (was hardcoded 1, 100)
Start attempts at 0 instead of 1 (fixed the off-by-one)
Trigger a full game reset when the difficulty selectbox changes
Show the real range in the instructions text instead of a hardcoded "1 and 100"
Only increment attempts on valid guesses, not invalid input
Commands run:

find . -type f -not -path "./.git/*" and git ls-files — to inventory the project (first attempt accidentally included .venv, so I switched to git ls-files for just tracked files)
python -m pytest tests/ -v (with a py -m pytest fallback) — confirmed all 3 tests in tests/test_game_logic.py pass after the fix



**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** |Sonnet 5 High | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
