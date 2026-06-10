from logic_utils import check_guess, get_range_for_difficulty, update_score


# --- check_guess ---

def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # 60 > 50, so outcome must be "Too High" (player needs to go lower)
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # 40 < 50, so outcome must be "Too Low" (player needs to go higher)
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_small_guess_vs_large_secret_is_too_low():
    # FIX regression: original code cast secret to str on even attempts,
    # making "9" > "50" True (lexicographic). Verify numeric comparison is used.
    result = check_guess(9, 50)
    assert result == "Too Low"


def test_guess_one_below_secret():
    result = check_guess(49, 50)
    assert result == "Too Low"


def test_guess_one_above_secret():
    result = check_guess(51, 50)
    assert result == "Too High"


# --- update_score ---

def test_win_on_first_attempt_gives_points():
    # attempt_number=1 → points = 100 - 10*(1+1) = 80
    result = update_score(0, "Win", 1)
    assert result == 80


def test_wrong_guess_always_loses_points():
    # FIX regression: original gave +5 on even attempt numbers for "Too High".
    result_even = update_score(100, "Too High", 2)
    result_odd = update_score(100, "Too High", 3)
    assert result_even == 95
    assert result_odd == 95


def test_too_low_always_loses_points():
    result = update_score(100, "Too Low", 2)
    assert result == 95


def test_win_score_never_drops_below_minimum():
    # After many attempts the points floor at 10
    result = update_score(0, "Win", 20)
    assert result == 10


# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_hard_range_is_harder_than_normal():
    # FIX regression: Hard was (1, 50), easier than Normal (1, 100).
    low, high = get_range_for_difficulty("Hard")
    assert high > 100, "Hard difficulty must have a larger range than Normal"
