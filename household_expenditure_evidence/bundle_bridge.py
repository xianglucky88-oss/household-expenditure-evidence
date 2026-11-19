from __future__ import annotations

from .contract import Row, apply_rows, integer, read_rows, text


def transform(row: Row) -> Row:
    """保留组合收费原分类，将有明细支持的金额桥接到新分类。"""
    breakdown = {}
    total = integer(row, "total_cents")
    for item in read_rows(row, "components"):
        category = text(item, "new_category")
        breakdown[category] = breakdown.get(category, 0) + integer(item, "cents")
    remainder = total - sum(breakdown.values())
    if remainder < 0:
        raise ValueError("itemized value exceeds bundle total")
    return {"old_category": text(row, "old_category"), "total_cents": total,
            "by_new_category": breakdown, "unclassified_cents": remainder}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
