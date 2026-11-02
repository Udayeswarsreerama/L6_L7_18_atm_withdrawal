
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# WITHDRAW: ACCOUNT TYPE BRANCHES

def test_valid_account():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_invalid_account():
    with pytest.raises(ValueError):
        withdraw(5000, 1000, "unknown", True)


# WITHDRAW: AMOUNT VALIDATION BRANCHES

def test_negative_amount():
    with pytest.raises(ValueError):
        withdraw(5000, -100, "savings", True)


def test_amount_not_multiple_of_100():
    with pytest.raises(ValueError):
        withdraw(5000, 150, "savings", True)


def test_valid_amount():
    assert withdraw(5000, 100, "savings", True) == 4900


# WITHDRAW: DAILY LIMIT BRANCHES

def test_amount_within_limit():
    assert withdraw(30000, 1000, "savings", True) == 29000


def test_amount_above_limit():
    assert withdraw(30000, 26000, "savings", True) == "limit exceeded"


# WITHDRAW: BANK FEE BRANCHES

def test_own_bank():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_other_bank():
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_amount_above_10000():
    assert withdraw(20000, 11000, "savings", True) == 9000


def test_amount_at_10000():
    assert withdraw(20000, 10000, "savings", True) == 10000


def test_high_amount_other_bank():
    assert withdraw(20000, 11000, "savings", False) == 8970


# WITHDRAW: BALANCE BRANCHES

def test_sufficient_balance():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_insufficient_balance():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_balance_insufficient_after_fee():
    assert withdraw(1010, 1000, "savings", False) == "insufficient funds"


# PIN CHECK: ATTEMPT BRANCHES

def test_attempts_less_than_three_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_attempts_less_than_three_wrong_pin():
    assert pin_check(1111, 1234, 1) == "retry"


def test_attempts_equal_three():
    assert pin_check(1234, 1234, 3) == "card blocked"


# PIN CHECK: CORRECT AND WRONG PIN

def test_correct_pin():
    assert pin_check(1234, 1234, 1) == "ok"


def test_wrong_pin():
    assert pin_check(1111, 1234, 0) == "retry"


# PIN CHECK: THIRD ATTEMPT

def test_attempts_equal_two():
    assert pin_check(1111, 1234, 2) == "card blocked"


# NOTE BREAKUP: VALIDATION

def test_valid_note_amount():
    assert note_breakup(500) == (1, 0, 0)


def test_invalid_note_amount():
    with pytest.raises(ValueError):
        note_breakup(150)


# NOTE BREAKUP: 200 NOTE CONDITION

def test_remaining_amount_at_least_200():
    assert note_breakup(800) == (1, 1, 1)


def test_remaining_amount_less_than_200():
    assert note_breakup(600) == (1, 0, 1)


def test_exact_200_note():
    assert note_breakup(200) == (0, 1, 0)
