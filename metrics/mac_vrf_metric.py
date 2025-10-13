import re
from typing import Any, Dict
from .base_metric import RegexMetric
from config.thresholds import get_threshold


class MacVrfMetric(RegexMetric):
    """Метрика количества MAC VRF"""

    def __init__(self):
        super().__init__(
            name="mac_vrf_count",
            description="MAC VRF Count",
            pattern=r'Command 9: sh running-config \| grep -c mac\\svrf\\s\s*(\d+)',
            value_type=int,
            display_name="MAC VRF"
        )
        self.threshold = get_threshold("mac_vrf")

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