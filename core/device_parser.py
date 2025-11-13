"""
Динамический парсер, который автоматически обрабатывает все зарегистрированные метрики
"""
import re
from typing import Dict, Any, List
from config.metrics_config import get_all_metrics, get_metric_display_names

class DeviceParser:
    """Парсер, который автоматически работает со всеми метриками"""

    def __init__(self):
        self.metrics = get_all_metrics()

    def parse_device_output(self, file_path: str) -> Dict[str, Any]:
        """Парсит вывод из файла используя все зарегистрированные метрики"""

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        result = self._extract_basic_info(content)

        # Парсим все метрики динамически
        for metric_name, metric in self.metrics.items():
            try:
                metric_result = metric.parse(content)
                # Сохраняем details для отображения в таблице
                result[metric_name] = metric_result.get('details', 'N/A')
                # Сохраняем полные данные для расширенного анализа
                result[f'{metric_name}_full'] = metric_result
            except Exception as e:
                result[metric_name] = f"ERROR: {str(e)}"
                print(f"Error parsing metric {metric_name}: {e}")

        return result

    def _extract_basic_info(self, content: str) -> Dict[str, Any]:
        """Извлекает базовую информацию (hostname, версия)"""
        result = {}

        # 1) Новый вариант — вывод команды "show run | i hostname"
        cfg_hostname = re.search(r'^\s*hostname\s+(\S+)', content, re.MULTILINE)
        if cfg_hostname:
            hostname = cfg_hostname.group(1)
        else:
            # 2) Старый вариант — вывод команды "show hostname"
            hostname_match = re.search(r'Command \d+:\s*show hostname\s+(\S+)', content)
            hostname = hostname_match.group(1) if hostname_match else 'Unknown'

        result['hostname'] = hostname

        # Software version
        software_match = re.search(r'Command 4: show version \| i Image Filename\s*Image Filename:\s*([^\n]+)', content)
        if software_match:
            software_version = software_match.group(1).strip()
            result['hostname_with_version'] = f"{result['hostname']}<br><small>{software_version}</small>"
        else:
            result['hostname_with_version'] = result['hostname']

        return result

    def get_metric_names(self) -> List[str]:
        """Возвращает список имен всех метрик"""
        return list(self.metrics.keys())

    def get_table_headers(self) -> List[str]:
        """Возвращает заголовки для таблицы на основе зарегистрированных метрик"""
        headers = ["#", "Hostname"]

        # Автоматически получаем display_name из самих метрик
        for metric_name in self.get_metric_names():
            metric = self.metrics[metric_name]
            headers.append(metric.display_name)

        return headers

    def get_metric_display_map(self) -> Dict[str, str]:
        """Возвращает маппинг имен метрик для отображения"""
        return get_metric_display_names()