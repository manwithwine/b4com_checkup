import os
import re
import time

from datetime import datetime
from netmiko import ConnectHandler
from dotenv import load_dotenv
from config.commands import get_b4com_commands
from config.hw_shell_commands import get_hw_shell_commands
from utils.file_utils import get_device_credentials


class DeviceManager:
    """Управление подключением и выполнением команд на устройствах"""

    def __init__(self):
        load_dotenv()

    def execute_commands(self, ip_addresses: list):
        """Основная функция выполнения команд"""
        folder_name = "cfg/cfg_" + datetime.now().strftime("%Y%m%d_%H%M")
        os.makedirs(folder_name, exist_ok=True)

        username, password = get_device_credentials()

        for ip_address in ip_addresses:
            print(f"Connecting to {ip_address}...")
            try:
                with ConnectHandler(
                        device_type='autodetect',
                        host=ip_address,
                        username=username,
                        password=password,
                        global_delay_factor=2,
                        read_timeout_override=100,
                        timeout=30,
                        fast_cli=False
                ) as net_connect:
                    print(f"Connected to {ip_address}")

                    # Определяем вендора
                    vendor = self._detect_vendor(net_connect)
                    if vendor != 'B4COM':
                        print(f"Unsupported vendor for {ip_address}. Skipping...")
                        continue

                    # Выполняем команды
                    combined_output = self._execute_vendor_commands(net_connect)
                    hw_output = self._execute_hw_shell_commands(net_connect)
                    combined_output += "=== HW-SHELL COMMANDS ===\n" + hw_output

                    # Сохраняем результат
                    self._save_output(combined_output, ip_address, folder_name)

            except Exception as e:
                print(f"Connection failed for {ip_address}: {str(e)}")
                self._log_error(ip_address, str(e))

    def _detect_vendor(self, net_connect) -> str:
        """Определяет вендора устройства"""
        output = net_connect.send_command("show version")
        bcom_output = net_connect.send_command("show ver | i BCOM")
        return 'B4COM' if 'BCOM' in output or 'BCOM' in bcom_output else 'UNKNOWN'

    def _execute_vendor_commands(self, net_connect) -> str:
        """Выполняет основные команды вендора"""
        vendor_commands = get_b4com_commands()
        combined_output = ""

        for i, command in enumerate(vendor_commands, start=1):
            combined_output += f"Command {i}: {command}\n"
            try:
                output = net_connect.send_command(command, expect_string=r'#', read_timeout=60)
                combined_output += output
            except Exception as e:
                combined_output += f"ERROR executing command: {str(e)}\n"
            combined_output += "\n\n"

        return combined_output

    def _execute_hw_shell_commands(self, net_connect) -> str:
        """Выполняет команды hw-shell режима"""
        hw_commands = get_hw_shell_commands()
        hw_output = ""

        for i, cmd_config in enumerate(hw_commands, 1):
            command = cmd_config["command"]
            delay = cmd_config["delay"]

            # Так же как обычные команды
            hw_output += f"Command {i}: {command}\n"

            # Отправляем команду
            net_connect.write_channel(f"{command}\n")
            time.sleep(delay)

            # Читаем вывод
            output = net_connect.read_channel()
            hw_output += output
            hw_output += "\n\n"

        return hw_output

    def _save_output(self, content: str, ip_address: str, folder: str):
        """Сохраняет вывод в файл"""
        hostname = self._extract_hostname(content, ip_address)
        filename = f"{hostname}.txt"
        file_path = os.path.join(folder, filename)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Saved output to {filename}")

    def _extract_hostname(self, content: str, ip_address: str) -> str:
        """Извлекает hostname из вывода команд"""

        # Новый вариант
        cfg_hostname = re.search(r'^\s*hostname\s+(\S+)', content, re.MULTILINE)
        if cfg_hostname:
            return cfg_hostname.group(1)

        # 2) Старый вариант
        hostname_match = re.search(r'Command \d+:\s*show hostname\s+(\S+)', content)
        if hostname_match:
            return hostname_match.group(1)

        for line in content.split('\n'):
            clean_line = line.strip()
            if clean_line and not clean_line.startswith('Command'):
                parts = clean_line.split()
                if parts and not parts[0].startswith('#'):
                    # если строка начинается с "hostname", берём второе слово
                    if parts[0].lower() == 'hostname' and len(parts) >= 2:
                        return parts[1]
                    return parts[0]

        return f"{ip_address}_Unknown"


    def _log_error(self, ip_address: str, error: str):
        """Логирует ошибки"""
        with open("error_log.txt", "a", encoding='utf-8') as error_file:
            error_file.write(f"{datetime.now()}: {ip_address} - {error}\n")