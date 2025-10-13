import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class CPUMetric(BaseMetric):
    """Метрика загрузки CPU"""

    def __init__(self):
        super().__init__(
            name="cpu",
            description="CPU Load and Core Usage",
            display_name="CPU"
        )
        # Берем пороги из единого источника
        self.load_threshold = get_threshold("cpu_load")
        self.core_threshold = get_threshold("cpu_core")

    def extract_value(self, content: str) -> Dict[str, Any]:
        load_match = re.search(r'Load Average\(5 min\)\s+:\s+([\d.]+)%', content)
        core_matches = re.findall(r'CPU core (\d+) Usage\s+:\s+([\d.]+)%', content)

        if not load_match:
            return None

        load_5min = float(load_match.group(1))
        cores = {int(core): float(usage) for core, usage in core_matches}

        return {"load_5min": load_5min, "cores": cores}

    def check_threshold(self, value: Dict[str, Any]) -> Dict[str, Any]:
        load_status = "OK" if value["load_5min"] <= self.load_threshold else "WARNING" if value[
                                                                                              "load_5min"] <= 80 else "ALERT"

        core_statuses = {}
        for core_num, usage in value["cores"].items():
            if usage <= self.core_threshold:
                core_statuses[core_num] = "OK"
            elif usage <= 90:
                core_statuses[core_num] = "WARNING"
            else:
                core_statuses[core_num] = "ALERT"

        # Общий статус
        overall_status = "OK"
        if any(status == "ALERT" for status in core_statuses.values()) or load_status == "ALERT":
            overall_status = "ALERT"
        elif any(status == "WARNING" for status in core_statuses.values()) or load_status == "WARNING":
            overall_status = "WARNING"

        details = f"LOAD_AVERAGE={value['load_5min']}%<br>CORE_USAGE:<br>"
        for core_num in sorted(value["cores"].keys()):
            usage = value["cores"][core_num]
            status = core_statuses[core_num]
            details += f"{core_num}={usage}%<br>"
        details += f"Result={overall_status}"

        return {
            "status": overall_status,
            "details": details,
            "raw_data": value
        }