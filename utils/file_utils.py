"""
Утилиты для работы с файлами
"""
import os
from typing import List


def read_ip_addresses(filename: str) -> List[str]:
    """Читает IP адреса из файла"""
    ip_addresses = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                ip = line.strip()
                if ip and not ip.startswith('#'):  # Игнорируем пустые строки и комментарии
                    ip_addresses.append(ip)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")

    return ip_addresses


def get_device_credentials():
    """Получает учетные данные из переменных окружения"""
    import os
    from dotenv import load_dotenv

    load_dotenv()

    username = os.getenv('DEVICE_USERNAME')
    password = os.getenv('DEVICE_PASSWORD')

    if not username or not password:
        raise ValueError("DEVICE_USERNAME or DEVICE_PASSWORD not set in .env file")

    return username, password


def find_latest_results_folder(base_folder: str = "cfg") -> str:
    """Находит самую свежую папку с результатами"""
    if not os.path.exists(base_folder):
        return None

    folders = []
    for item in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item)
        if os.path.isdir(item_path) and item.startswith('cfg_'):
            folders.append(item_path)

    if not folders:
        return None

    # Сортируем по времени создания (новейшие first)
    folders.sort(key=os.path.getctime, reverse=True)
    return folders[0]


def ensure_directory(path: str):
    """Создает директорию если она не существует"""
    os.makedirs(path, exist_ok=True)