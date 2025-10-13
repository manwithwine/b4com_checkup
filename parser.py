"""
Парсер для анализа собранных данных и генерации отчетов
"""
import os
import sys

# Добавляем пути для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'metrics'))

from utils.file_utils import find_latest_results_folder
from core.device_parser import DeviceParser
from core.report_generator import ReportGenerator


def process_all_results(results_folder: str = "cfg"):
    """Обрабатывает все результаты в папке и генерирует отчеты"""

    # Находим самую свежую папку с результатами
    latest_folder = find_latest_results_folder(results_folder)
    if not latest_folder:
        print("❌ Не найдено папок с результатами")
        return

    print(f"📂 Обрабатываю папку: {latest_folder}")

    # Создаем парсер и генератор отчетов
    parser = DeviceParser()
    report_generator = ReportGenerator(parser)

    parsed_data_list = []

    # Ищем все файлы в найденной папке
    for file in os.listdir(latest_folder):
        if file.endswith('.txt'):
            file_path = os.path.join(latest_folder, file)
            print(f"📄 Обрабатываю файл: {file}")

            try:
                parsed_data = parser.parse_device_output(file_path)
                parsed_data_list.append(parsed_data)
            except Exception as e:
                print(f"❌ Ошибка при обработке файла {file}: {e}")

    if not parsed_data_list:
        print("❌ Не найдено файлов для обработки")
        return

    # Генерируем HTML отчет
    html_path = report_generator.generate_html_report(parsed_data_list, latest_folder)

    print(f"\n📊 Отчеты сохранены в папке: {latest_folder}")
    print(f"• 📄 HTML отчет: {os.path.basename(html_path)}")
    print(f"\n🔗 Откройте файл в браузере для лучшего просмотра:")
    print(f"file://{html_path}")

    # Показываем статистику по метрикам
    print(f"\n📈 Обработано метрик: {len(parser.get_metric_names())}")
    print("📋 Метрики:", ", ".join(parser.get_metric_names()))


if __name__ == "__main__":
    process_all_results()