import re
from typing import Any, Dict
from .base_metric import RegexMetric
from config.thresholds import get_threshold


class IrbIntMetric(RegexMetric):
    """Метрика количества IRB интерфейсов"""

    def __init__(self):
        super().__init__(
            name="irb_int_count",
            description="IRB Interface Count",
            pattern=r'Command 10: sh ip int br \| grep -c irb\s*(\d+)',
            value_type=int,
            display_name="IRB INT"
        )
        self.threshold = get_threshold("irb_int")

    def check_threshold(self, value: int) -> Dict[str, Any]:
        if value < 1300:
            status = "OK"
        elif value <= 1500:
            status = "WARNING"
        else:
            status = "ALERT"

        return {
            "status": status,
            "details": f"{value}<br>Result={status}",
            "raw_data": value
        }