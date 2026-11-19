from __future__ import annotations

from .contract import Row, apply_rows, integer


def transform(row: Row) -> Row:
    """按自用单位与明确可比的单位价形成非现金消费估值。"""
    retained = integer(row, "retained_units")
    if retained + integer(row, "gift_units") + integer(row, "sold_units") > integer(row, "produced_units"):
        raise ValueError("allocated units exceed production")
    price = integer(row, "unit_price_cents") if row["unit_price_cents"] is not None else None
    value = retained * price if price is not None else (None if retained else 0)
    return {"retained_units": retained, "imputed_cents": value,
            "unpriced_units": retained if price is None else 0}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
