import pytest

from pricing import (
    calculate_subtotal,
    apply_member_discount,
    add_tax,
    calculate_total,
    write_receipt,
)


@pytest.mark.parametrize(
    "unit_price, quantity, expected",
    [
        (10000, 2, 20000),
        (15000, 3, 45000),
        (0, 5, 0),
    ],
)
def test_calculate_subtotal_valid_inputs(unit_price, quantity, expected):
    assert calculate_subtotal(unit_price, quantity) == expected


def test_calculate_subtotal_negative_price_raises_value_error():
    with pytest.raises(ValueError, match="unit_price must not be negative"):
        calculate_subtotal(-10000, 2)


def test_calculate_subtotal_zero_quantity_raises_value_error():
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_subtotal(10000, 0)


def test_calculate_subtotal_negative_quantity_raises_value_error():
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_subtotal(10000, -1)


def test_apply_member_discount_applies_ten_percent():
    result = apply_member_discount(100000, True)
    assert result == pytest.approx(90000)


def test_apply_member_discount_non_member_pays_full_price():
    result = apply_member_discount(100000, False)
    assert result == 100000


def test_apply_member_discount_zero_subtotal():
    assert apply_member_discount(0, True) == 0


def test_add_tax_applies_eleven_percent():
    result = add_tax(100000)
    assert result == pytest.approx(111000)


def test_add_tax_zero_amount():
    assert add_tax(0) == 0


def test_calculate_total_for_member():
    result = calculate_total(100000, 1, is_member=True)
    assert result == pytest.approx(99900)


def test_calculate_total_for_non_member():
    result = calculate_total(100000, 1, is_member=False)
    assert result == pytest.approx(111000)


def test_calculate_total_defaults_to_non_member():
    result = calculate_total(100000, 1)
    assert result == pytest.approx(111000)


def test_calculate_total_negative_price_raises_value_error():
    with pytest.raises(ValueError, match="unit_price must not be negative"):
        calculate_total(-10000, 2, is_member=True)


def test_calculate_total_zero_quantity_raises_value_error():
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_total(10000, 0)


def test_write_receipt_writes_lines_with_final_newline(tmp_path):
    receipt_path = tmp_path / "receipt.txt"
    lines = [
        "My Store",
        "Subtotal: Rp100000",
        "Total: Rp111000",
    ]

    write_receipt(receipt_path, lines)

    assert receipt_path.read_text(encoding="utf-8") == (
        "My Store\n" "Subtotal: Rp100000\n" "Total: Rp111000\n"
    )


def test_write_receipt_with_empty_lines(tmp_path):
    receipt_path = tmp_path / "empty_receipt.txt"

    write_receipt(receipt_path, [])

    assert receipt_path.read_text(encoding="utf-8") == "\n"


def test_write_receipt_overwrites_existing_file(tmp_path):
    receipt_path = tmp_path / "receipt.txt"
    receipt_path.write_text("Old receipt\n", encoding="utf-8")

    write_receipt(receipt_path, ["New receipt"])

    assert receipt_path.read_text(encoding="utf-8") == "New receipt\n"
