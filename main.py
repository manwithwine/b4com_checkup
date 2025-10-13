"""
Основной скрипт для сбора данных с устройств B4COM
"""
import os
import sys

# Добавляем пути для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'metrics'))

from core.device_manager import DeviceManager
from utils.file_utils import read_ip_addresses


def main():
    """Основная функция"""
    print("🚀 B4COM Checkup System")
    print("=" * 50)

    # Читаем IP адреса из файла
    ip_addresses = read_ip_addresses("ip.txt")

    if not ip_addresses:
        print("❌ No IP addresses found in ip.txt")
        return

    print(f"📡 Found {len(ip_addresses)} devices to check")

    # Собираем данные с устройств
    device_manager = DeviceManager()
    device_manager.execute_commands(ip_addresses)

    # Запускаем анализ данных
    print("\n" + "=" * 50)
    print("🔍 Analyzing collected data...")
    print("=" * 50)

    from parser import process_all_results
    process_all_results("cfg")


if __name__ == "__main__":
    main()