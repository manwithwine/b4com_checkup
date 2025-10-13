"""
Конфигурация команд для hw-shell режима
"""

HW_SHELL_COMMANDS = [
    {
        "command": "hw-shell",
        "description": "Enter HW Shell mode",
        "delay": 2,
        "expect_string": None
    },
    {
        "command": "l3 info",
        "description": "Get L3 information",
        "delay": 5,
        "expect_string": None
    },
    {
        "command": "exit",
        "description": "Exit HW Shell mode",
        "delay": 1,
        "expect_string": None
    },
]

def get_hw_shell_commands():
    """Возвращает команды hw-shell с их настройками"""
    return HW_SHELL_COMMANDS

def add_hw_shell_command(command: str, description: str, delay: int = 1, expect_string: str = None):
    """Добавляет новую команду hw-shell"""
    HW_SHELL_COMMANDS.append({
        "command": command,
        "description": description,
        "delay": delay,
        "expect_string": expect_string
    })