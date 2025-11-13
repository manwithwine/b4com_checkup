"""
Команды для выполнения на устройствах B4COM
"""

# Базовые команды для всех устройств
BASE_COMMANDS = [
    "show run | i hostname",
    "term no mon",
    "terminal length 0",
    "show version | i Image Filename",
]

# Команды специфичные для B4COM
B4COM_COMMANDS = [
    "show system-information cpu-load",
    "show hardware-information memory | i Total  |Used  |Free  ",
    "sh run | i nvo.vxlan.id",
    "show nvo vxlan access-if br | i Total",
    r"sh running-config | grep -c mac\svrf\s",
    "sh ip int br | grep -c irb",
    "sh run | grep nvo.vxlan.id.",
    "sh ip int br | i vlan1.",
    "sh ip vrf | i tunvxlan",
    "sh nvo vxlan route-count | i Max|Active",
    "show forwarding profile limit",
    "sh nvo vxlan mac-table hardware | i Total",
    r"sh hsl evpn multihoming es | i \(R",
]

def get_b4com_commands():
    """Возвращает полный список команд для B4COM устройств"""
    return BASE_COMMANDS + B4COM_COMMANDS

def get_hw_shell_commands():
    """Возвращает команды для hw-shell режима"""
    return HW_SHELL_COMMANDS