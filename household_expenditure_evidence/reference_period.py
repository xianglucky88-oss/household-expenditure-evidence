from __future__ import annotations

from .contract import Row, apply_rows, day, integer, read_rows


def transform(row: Row) -> Row:
    """用消费日而非录入日归入调查期间并单列消费日不明的金额。"""
    start = day(row, "from")
    end = day(row, "until")
    if start >= end:
        raise ValueError("survey period must be nonempty")
    sums = {"in_period": 0, "out_of_period": 0, "unknown": 0}
    for entry in read_rows(row, "entries"):
        day(entry, "entered_on")
        when = day(entry, "consumed_on") if entry["consumed_on"] is not None else None
        key = "unknown" if when is None else "in_period" if start <= when < end else "out_of_period"
        sums[key] += integer(entry, "cents")
    return {"period_cents": sums}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
