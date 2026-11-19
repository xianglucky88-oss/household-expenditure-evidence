from __future__ import annotations

from .contract import Row, apply_rows, index_rows, integer, read_rows


def transform(row: Row) -> Row:
    """对比同一抽样组的完整日记与补访加入后的可用金额和样本数。"""
    initial = []
    augmented = []
    households = index_rows(read_rows(row, "households"), "household")
    for sample in households.values():
        if sample["diary_cents"] is not None:
            value = integer(sample, "diary_cents")
            initial.append(value)
            augmented.append(value)
        elif sample["followup_cents"] is not None:
            augmented.append(integer(sample, "followup_cents"))
    return {"sample_size": len(households), "complete_count": len(initial), "with_followup_count": len(augmented),
            "complete_mean_cents": sum(initial) / len(initial) if initial else None,
            "with_followup_mean_cents": sum(augmented) / len(augmented) if augmented else None}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
