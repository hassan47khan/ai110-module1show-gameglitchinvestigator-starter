# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

  The game looked normal, but it was unplayable. The hints told me to go the wrong way, and on every second guess the game seemed to ignore the secret number entirely. The attempts counter also started at 1 instead of 0. "New Game" didn't behave like a fresh game either, and after a win or loss the game stayed locked.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess higher than the secret (e.g. secret 40, guess 60) | "📉 Go LOWER!" | "📈 Go HIGHER!". The hint text was swapped in `check_guess` | No error, just a wrong message |
| Any guess on an even-numbered attempt (2nd, 4th…) | Compare the guess to the secret as numbers | The secret was converted with `str(secret)`, so the comparison was string vs. int or string vs. string. The hint was wrong and a correct guess could fail to win | Caught silently by `except TypeError` in `check_guess` |
| Start a new session and check "Attempts left" | Full attempt count shown (e.g. 8) | `attempts` started at 1, so it showed one attempt too few | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  For this project I use Claude Code in VS Code.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude found that on even attempts the secret was converted to a string, which broke the comparison. That would explain why some guesses got wrong hints. I checked it by adding a pytest for `check_guess(60, 50)` and by playing the game to confirm the hints and win now work on every attempt.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

  When Claude reviewed the code, it also flagged two things beyond the real bugs: decimal guesses like `42.9` being silently truncated to `42`, and the score being able to go negative. I chose not to change either. They are design choices, not glitches, and changing them would have gone beyond the task. I checked my version by confirming the existing tests (which expect `42.9` to become `42`) still pass and the game still plays correctly.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I reran the exact steps that used to break it and then added a pytest for it, so it would fail if the bug came back.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

  A test I ran: `test_update_score_too_high_penalizes_consistently` checks that a wrong "Too High" guess subtracts 5 on both odd and even attempts. The old code failed it. I also ran a Streamlit script check that played through an out-of-range guess, a win, New Game and running out of attempts.

- Did AI help you design or understand any tests? How?

  AI's role: Claude helped write the tests and suggested edge cases like boundary values, `1.0e999` and whitespace-only input, and I read them before keeping them.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit reruns your whole script from the top every time you click a button or type in a box. Because of that, ordinary variables reset each time. `st.session_state` is a small dictionary that survives those reruns, so the secret number, attempts and score go in it, and it is set up only once instead of on every run. In the original app the secret was fine, but the counters and status weren't reset properly, so the game got stuck between rounds.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  I want to write a small test for each bug as I fix it, so I know it stays fixed. Reading the original code and comparing it with the fixed version also made it clear what had actually changed.

- What is one thing you would do differently next time you work with AI on a coding task?

  I'd check what the AI is going to change before it edits my files, and I'd ask for one fix at a time instead of everything at once. Next time, what I want to do differently is that highlight each code in detail so the AI agent can give me a detailed explanation of what's going on.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI is a useful partner, but you still need to understand what the code does and whether it makes sense.
