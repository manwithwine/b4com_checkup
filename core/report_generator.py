import os

from datetime import datetime
from config.thresholds import get_threshold_row
from templates.report_template import HTML_TEMPLATE
from config.tooltips import THRESHOLD_TOOLTIP

class ReportGenerator:
    """Генератор HTML и Markdown отчетов"""

    def __init__(self, parser):
        self.parser = parser

    def generate_html_report(self, parsed_data_list: list, output_folder: str) -> str:
        """Генерирует красивый HTML отчет"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        devices_count = len(parsed_data_list)
        healthy_count = self._count_status(parsed_data_list, 'OK')
        warning_count = self._count_status(parsed_data_list, 'WARNING')
        alert_count = self._count_status(parsed_data_list, 'ALERT')
        table_content = self._generate_html_table(parsed_data_list)
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        html_content = HTML_TEMPLATE.format(
            devices_count=devices_count,
            healthy_count=healthy_count,
            warning_count=warning_count,
            alert_count=alert_count,
            table_content=table_content,
            timestamp=current_timestamp
        )

        html_path = os.path.join(output_folder, f"report_{timestamp}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML отчет сохранен: {html_path}")
        return html_path

    def _count_status(self, parsed_data_list: list, status: str) -> int:
        """Считает количество устройств с определенным статусом"""
        count = 0
        for device in parsed_data_list:
            device_str = str(device).upper()
            if status.upper() in device_str:
                count += 1
        return count

    def _generate_html_table(self, parsed_data_list: list) -> str:
        """Генерирует HTML таблицу с данными"""

        headers = self.parser.get_table_headers()
        metric_names = self.parser.get_metric_names()
        metrics = self.parser.metrics

        table_html = '<table>\n<thead>\n<tr>\n'

        # Заголовки ТОЛЬКО для метрик
        for i, header in enumerate(headers):
            if i == 0:  # №
                table_html += f'<th>{header}</th>\n'
            elif i == 1:  # Hostname
                table_html += f'<th>{header}</th>\n'
            else:  # Метрики
                metric_index = i - 2
                if metric_index < len(metric_names):
                    metric_name = metric_names[metric_index]
                    metric = metrics[metric_name]
                    # Двойная подсказка: общая + индивидуальная
                    combined_tooltip = f"{metric.tooltip}\n\n{THRESHOLD_TOOLTIP}"
                    table_html += f'<th data-tooltip="{combined_tooltip}">{header}</th>\n'
                else:
                    table_html += f'<th>{header}</th>\n'

        table_html += '</tr>\n</thead>\n<tbody>\n'

        # Строка с порогами - БЕЗ подсказок
        table_html += '<tr class="threshold-row">\n'
        threshold_row = get_threshold_row()
        for i, item in enumerate(threshold_row):
            table_html += f'<td>{item}</td>\n'
        table_html += '</tr>\n'

        # Данные устройств - БЕЗ подсказок
        for i, device in enumerate(parsed_data_list, 1):
            table_html += '<tr class="device-row">\n'
            table_html += f'<td><strong>{i}</strong></td>\n'

            hostname_display = device.get("hostname_with_version", device.get("hostname", "N/A"))
            table_html += f'<td><strong>{hostname_display}</strong></td>\n'

            # Данные метрик БЕЗ подсказок
            for metric_name in metric_names:
                value = device.get(metric_name, 'N/A')
                table_html += f'<td>{self._format_cell(value)}</td>\n'

            table_html += '</tr>\n'

        table_html += '</tbody>\n</table>'
        return table_html

    def _format_cell(self, value):
        """Форматирует ячейку с подсветкой статуса"""
        if value == 'N/A':
            return '<span style="color: #6c757d;">N/A</span>'

        lines = str(value).split('<br>')
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if 'Result=OK' in line:
                formatted_lines.append(f'<span class="status-ok">✓ {line.replace("Result=OK", "").strip()}</span>')
            elif 'Result=WARNING' in line:
                formatted_lines.append(
                    f'<span class="status-warning">⚠ {line.replace("Result=WARNING", "").strip()}</span>')
            elif 'Result=ALERT' in line:
                formatted_lines.append(
                    f'<span class="status-alert">🚨 {line.replace("Result=ALERT", "").strip()}</span>')
            elif 'LOAD_AVERAGE' in line or 'CORE_USAGE' in line:
                formatted_lines.append(f'<div class="metric-details">{line}</div>')
            elif any(x in line for x in ['%', '/']):
                formatted_lines.append(f'<div class="metric-value">{line}</div>')
            else:
                formatted_lines.append(f'<div>{line}</div>')

        return ''.join(formatted_lines)