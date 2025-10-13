import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold

class AsicMacMetric(BaseMetric):
    """Метрика использования ASIC MAC таблицы"""

    def __init__(self):
        super().__init__(
            name="asic_mac_addr_count",
            description="ASIC MAC Address Table Usage",
            display_name="ASIC MAC"
        )
        self.threshold = get_threshold("asic_mac")

    def extract_value(self, content: str) -> Dict[str, int]:
        # Получаем профиль из Command 15
        profile_match = re.search(r'Configured profile : (\S+)', content)
        if not profile_match:
            return None

        # Ищем значение MAC-Table для профиля
        table_match = re.search(
            r'Forwarding Profile Table Size.*?l2-profile-three\s+(\d+)k\s+(\d+)k\s+(\d+)k\s+(\d+)k\s+(\d+)k\s+(\d+)k',
            content, re.DOTALL
        )

        if table_match:
            mac_table_k = int(table_match.group(1))
        else:
            # Альтернативный поиск
            profile_match = re.search(r'l2-profile-three\s+(\d+)k\s+(\d+)k\s+(\d+)k\s+(\d+)k\s+(\d+)k\s+(\d+)k',
                                      content)
            if profile_match:
                mac_table_k = int(profile_match.group(1))
            else:
                return None

        mac_table_total = mac_table_k * 1024

        # Получаем использованные MAC адреса из Command 16
        cmd16_match = re.search(
            r'Command 16: sh nvo vxlan mac-table hardware \| i Total.*?Total number of entries are\s+(\d+)',
            content, re.DOTALL
        )
        if not cmd16_match:
            return None

        used_mac = int(cmd16_match.group(1))

        return {"total": mac_table_total, "used": used_mac}

    def check_threshold(self, value: Dict[str, int]) -> Dict[str, Any]:
        if value["total"] > 0:
            percent = (value["used"] / value["total"]) * 100
            percent_str = f"{percent:.1f}%"

            if percent < self.threshold:
                status = "OK"
            else:
                status = "ALERT"

            return {
                "status": status,
                "details": f"{value['used']}/{value['total']}<br>{percent_str}<br>Result={status}",
                "raw_data": value,
                "percentage": percent
            }

        return {
            "status": "UNKNOWN",
            "details": "N/A",
            "raw_data": value
        }