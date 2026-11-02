
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# WITHDRAW FUNCTION TESTS

def test_valid_savings_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_valid_current_withdrawal():
    assert withdraw(10000, 2000, "current", True) == 8000


def test_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "salary", True)


def test_negative_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -100, "savings", True)


def test_zero_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_non_multiple_of_100():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


def test_daily_limit_exceeded():
    assert withdraw(50000, 26000, "savings", True) == "limit exceeded"


def test_current_daily_limit_exceeded():
    assert withdraw(60000, 51000, "current", True) == "limit exceeded"


def test_other_bank_fee():
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_high_withdrawal_fee():
    assert withdraw(20000, 11000, "savings", True) == 9000


def test_high_withdrawal_other_bank_fee():
    assert withdraw(20000, 11000, "savings", False) == 8970


def test_insufficient_funds():
    assert withdraw(1000, 2000, "savings", True) == "insufficient funds"


def test_insufficient_funds_with_fee():
    assert withdraw(1010, 1000, "savings", False) == "insufficient funds"


# PIN CHECK FUNCTION TESTS

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_wrong_pin_first_attempt():
    assert pin_check(1111, 1234, 0) == "retry"


def test_wrong_pin_second_attempt():
    assert pin_check(1111, 1234, 1) == "retry"


def test_wrong_pin_third_attempt():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_card_already_blocked():
    assert pin_check(1234, 1234, 3) == "card blocked"


# NOTE BREAKUP FUNCTION TESTS

def test_note_breakup_500():
    assert note_breakup(500) == (1, 0, 0)


def test_note_breakup_200():
    assert note_breakup(200) == (0, 1, 0)


def test_note_breakup_100():
    assert note_breakup(100) == (0, 0, 1)


def test_note_breakup_mixed():
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_without_200_note():
    assert note_breakup(600) == (1, 0, 1)


def test_invalid_note_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)
