import re
from typing import Any, Dict
from .base_metric import RegexMetric
from config.thresholds import get_threshold

class ARPMetric(RegexMetric):
    """Метрика количества ARP записей"""

    def __init__(self):
        super().__init__(
            name="arp_count",
            description="ARP Entries Count",
            pattern=r'hosts\s+:\s+(\d+)\s+/\s+\d+',
            value_type=int,
            display_name = "ARP"
        )
        self.threshold = get_threshold("arp")

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