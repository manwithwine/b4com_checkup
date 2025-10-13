import re

from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class AccessIfMetric(BaseMetric):
    """Метрика количества access интерфейсов"""

    def __init__(self):
        super().__init__(
            name="access_if_count",
            description="Access Interface Count",
            display_name="ACCES-IF"
        )
        self.threshold = get_threshold("access_if")

    def extract_value(self, content: str) -> int:
        # Считаем строки в Command 7
        cmd7_match = re.search(r'Command 7: sh run \| i nvo\.vxlan\.id(.*?)(?=Command \d+:|$)', content, re.DOTALL)
        cmd7_count = 0
        if cmd7_match:
            cmd7_content = cmd7_match.group(1)
            cmd7_count = len(re.findall(r'nvo vxlan id \d+', cmd7_content))

        # Получаем число из Command 8
        cmd8_match = re.search(
            r'Command 8: show nvo vxlan access-if br \| i Total.*?Total number of entries are\s+(\d+)',
            content, re.DOTALL
        )
        cmd8_count = int(cmd8_match.group(1)) if cmd8_match else 0

        return cmd7_count + cmd8_count

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