import re

from abc import ABC, abstractmethod
from typing import Any, Dict
from config.tooltips import get_metric_tooltip


class BaseMetric(ABC):
    """Абстрактный базовый класс для всех метрик"""

    def __init__(self, name: str, description: str, display_name: str = None):
        self.name = name
        self.description = description
        self.display_name = display_name or name.upper()
        self.tooltip = get_metric_tooltip(name)

    @abstractmethod
    def extract_value(self, content: str) -> Any:
        """Извлекает значение из сырого вывода команд"""
        pass

    @abstractmethod
    def check_threshold(self, value: Any) -> Dict[str, Any]:
        """Проверяет значение против порога"""
        pass

    def parse(self, content: str) -> Dict[str, Any]:
        """Основной метод парсинга метрики"""
        value = self.extract_value(content)
        if value is None:
            return {
                "value": "N/A",
                "status": "UNKNOWN",
                "details": "Data not found",
                "name": self.name,
                "display_name": self.display_name
            }

        result = self.check_threshold(value)
        result["value"] = value
        result["name"] = self.name
        result["display_name"] = self.display_name
        return result


class RegexMetric(BaseMetric):
    """Метрика на основе регулярных выражений"""

    def __init__(self, name: str, description: str, pattern: str, display_name: str = None,
                 value_type: type = str, group: int = 1):
        super().__init__(name, description, display_name)
        self.pattern = pattern
        self.value_type = value_type
        self.group = group

    def extract_value(self, content: str) -> Any:
        match = re.search(self.pattern, content, re.DOTALL)
        if match:
            try:
                raw_value = match.group(self.group)
                return self.value_type(raw_value)
            except (ValueError, IndexError):
                return None
        return None