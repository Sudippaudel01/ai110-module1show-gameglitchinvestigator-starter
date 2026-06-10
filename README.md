# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number guessing game where the player picks a difficulty, is given a range, and has a limited number of attempts to guess the secret number. Wrong guesses receive "Too High" or "Too Low" hints. Score increases on a win and decreases for each wrong guess.
- [x] **Bugs found:**
  1. Hint messages were inverted — "Go HIGHER!" displayed when the guess was already too high.
  2. On every even-numbered attempt the secret was cast to a string, causing wrong outcomes via lexicographic comparison (e.g. `"9" > "50"` is True).
  3. Hard difficulty range was 1–50 (easier than Normal's 1–100).
  4. Wrong guesses on even-numbered attempts rewarded the player with +5 instead of −5.
  5. `attempts` counter started at 1 instead of 0, making the "Attempts left" display off by one from the start.
  6. New Game button always generated a secret in range 1–100, ignoring the selected difficulty.
  7. Info banner hardcoded "1 and 100" regardless of the actual difficulty range.
- [x] **Fixes applied:** All logic moved to `logic_utils.py`. Hint messages corrected. String-secret conversion removed. Hard range set to 1–500. Score always deducts 5 for wrong guesses. `attempts` starts at 0. New Game respects difficulty. Info banner uses actual `low`/`high` values.

## 📸 Demo Walkthrough

1. User opens the app on Normal difficulty (range 1–100, 8 attempts allowed).
2. The info bar reads "Guess a number between 1 and 100. Attempts left: 8."
3. User types **40**. Secret is 75. Game returns "📈 Go HIGHER!" — hint is correct.
4. User types **90**. Game returns "📉 Go LOWER!" — hint is correct.
5. User types **75**. Game returns "🎉 Correct!" with balloons. Final score is shown.
6. User clicks **New Game**. Attempt counter resets to 0, a fresh secret is picked within the difficulty range, and the board clears.

## 🧪 Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3
collected 13 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 15%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 23%]
tests/test_game_logic.py::test_small_guess_vs_large_secret_is_too_low PASSED [ 30%]
tests/test_game_logic.py::test_guess_one_below_secret PASSED             [ 38%]
tests/test_game_logic.py::test_guess_one_above_secret PASSED             [ 46%]
tests/test_game_logic.py::test_win_on_first_attempt_gives_points PASSED  [ 53%]
tests/test_game_logic.py::test_wrong_guess_always_loses_points PASSED    [ 61%]
tests/test_game_logic.py::test_too_low_always_loses_points PASSED        [ 69%]
tests/test_game_logic.py::test_win_score_never_drops_below_minimum PASSED [ 76%]
tests/test_game_logic.py::test_easy_range PASSED                         [ 84%]
tests/test_game_logic.py::test_normal_range PASSED                       [ 92%]
tests/test_game_logic.py::test_hard_range_is_harder_than_normal PASSED   [100%]

============================== 13 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
