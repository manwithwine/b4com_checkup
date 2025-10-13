import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class ESLagMetric(BaseMetric):
    """Метрика количества ES LAG сессий"""

    def __init__(self):
        super().__init__(
            name="es_lag_count",
            description="ES LAG Sessions Count",
            display_name="ES LAG"
        )
        self.threshold = get_threshold("es_lag")

    def extract_value(self, content: str) -> int:
        cmd17_match = re.search(r'Command 17:.*?(\(R\).*?)(?=Command|\Z)', content, re.DOTALL)
        if cmd17_match:
            cmd17_content = cmd17_match.group(1)
            return len(re.findall(r'\(R\)', cmd17_content))
        return 0

    def check_threshold(self, value: int) -> Dict[str, Any]:
        if value <= self.threshold:
            status = "OK"
        else:
            status = "ALERT"

        return {
            "status": status,
            "details": f"{value}<br>Result={status}",
            "raw_data": value
        }