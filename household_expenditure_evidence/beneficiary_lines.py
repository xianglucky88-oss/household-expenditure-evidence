from __future__ import annotations

from .contract import Row, apply_rows, index_rows, integer, read_rows, text


def transform(row: Row) -> Row:
    """按购物条目的实际受益家庭归属整行金额，不猜未确认的家庭。"""
    grouped = {}
    unresolved = 0
    for line in index_rows(read_rows(row, "lines"), "line").values():
        cents = integer(line, "cents")
        if line["beneficiary"] is None:
            unresolved += cents
        else:
            household = text(line, "beneficiary")
            grouped[household] = grouped.get(household, 0) + cents
    return {"consumption_cents": grouped, "unresolved_cents": unresolved}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
