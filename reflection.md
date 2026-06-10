# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app the game was unplayable in several ways. The hints were inverted — when my guess was too high, the game told me to go *higher*, which sent me in the wrong direction every time. On every even-numbered attempt the secret was silently converted to a string, so a guess of 9 against a secret of 50 would incorrectly report "Too High" because Python's string comparison puts `"9"` after `"50"` alphabetically. The Hard difficulty was actually *easier* than Normal (range 1–50 vs 1–100), and the score would sometimes *increase* after a wrong guess on even-numbered attempts.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, Secret 50 (attempt 1 — odd) | Hint: "Go LOWER!" | Hint: "Go HIGHER!" (messages swapped) | none |
| Guess 9, Secret 50 (attempt 2 — even) | "Too Low" (9 < 50) | "Too High" (string compare: `"9" > "50"` is True) | none |
| Select Hard difficulty | Range 1–500 (harder than Normal) | Range 1–50 (easier than Normal 1–100) | none |
| Wrong guess on even attempt number | Score decreases by 5 | Score increases by 5 (rewards wrong guesses) | none |
| First page load, Normal difficulty | "Attempts left: 8" | "Attempts left: 7" (attempts starts at 1 instead of 0) | none |

---

## 2. How did you use AI as a teammate?

I used Claude Code as my AI coding assistant throughout the project. It correctly identified that the hint messages in `check_guess` were swapped — "Go HIGHER!" was returned when the guess was too high when it should have said "Go LOWER!" — and the fix was straightforward: swap the two message strings. I verified this by tracing through `check_guess(60, 50)`: 60 > 50 is True, so the first branch ran, and I confirmed the corrected message matched the expected direction. The AI also correctly flagged the string-conversion bug (the `attempts % 2 == 0` block casting the secret to a string), explained exactly why `"9" > "50"` is True in Python, and suggested removing that block entirely. One misleading suggestion was adding a try/except around the score update to silently swallow ValueError — I rejected this because there is no ValueError possible there; the real fix was removing the bad logic, not hiding failures.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when both the manual game behavior matched expectations and the automated pytest suite passed. For example, after fixing `check_guess` I ran `pytest tests/` and confirmed all three starter tests passed — `test_winning_guess`, `test_guess_too_high`, and `test_guess_too_low` — which directly targeted the inverted-hint bug. I also added tests for the string-comparison edge case (`check_guess(9, 50)` → `"Too Low"`) and for the score fix (`update_score` with "Too High" on an even attempt number no longer returns a higher score). AI helped me understand that the existing tests were already written to test the *correct* behavior, so they would fail against the original buggy code and pass after the fix — which was a useful insight for understanding what "test-driven" means.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time a user interacts with the page — clicking a button, typing in an input, anything. Without `st.session_state`, every variable would reset on each rerun, so the secret number would change with every button click, making the game impossible to win. `st.session_state` is a dictionary that persists between reruns, which is how we keep the secret, the attempt count, and the score stable. Think of it like a sticky note on the fridge — the kitchen gets reorganized every time someone walks in, but the note stays put.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is reading failing tests *before* writing any fix — the test already tells you exactly what correct behavior looks like, which makes the target clear. Next time I work with AI on a debugging task I would give it one bug at a time in a fresh chat, because when I described multiple issues at once it tended to bundle unrelated suggestions together and I had to untangle them. This project changed how I think about AI-generated code: it can produce code that *runs* without producing code that *works*, and the gap between those two things is exactly where human judgment is most valuable.
