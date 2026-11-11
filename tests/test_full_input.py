"""Regressão para exportações com mais de 200 reservas."""

from helpers import run_cli


def test_report_includes_reservations_after_row_200(tmp_path):
    rows = [
        {"reservation_id": f"R-{number}", "status": "CANCELLED"}
        for number in range(1, 201)
    ]
    rows.append({"reservation_id": "R-201", "status": "CONFIRMED", "amount": "42.00"})

    summary = run_cli(tmp_path, rows)["summary"]

    assert summary["total_reservations"] == 201
    assert summary["confirmed_reservations"] == 1
    assert summary["cancelled_reservations"] == 200
    assert summary["total_room_nights"] == 1
    assert summary["total_amount_brl"] == "42.00"
