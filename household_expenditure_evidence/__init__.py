"""家庭支出调查数据"""

from . import beneficiary_lines, reference_period, home_production, bundle_bridge, followup_coverage
from .contract import Row

PIPELINES = {
    "beneficiary-lines": beneficiary_lines.build_facts,
    "reference-period": reference_period.build_facts,
    "home-production": home_production.build_facts,
    "bundle-bridge": bundle_bridge.build_facts,
    "followup-coverage": followup_coverage.build_facts,
}

def process(pipeline: str, data: Row) -> list[Row]:
    """Validate and transform an independent input dataset into keyed facts."""
    if pipeline not in PIPELINES:
        raise ValueError(f"unknown pipeline: {pipeline}")
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return PIPELINES[pipeline](data)
