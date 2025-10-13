"""
Подсказки для метрик
"""

METRIC_TOOLTIPS = {
    "cpu": "Загрузка CPU\n• Load Average: средняя загрузка за 5 минут\n• CORE_USAGE: загрузка по ядрам\n\nПороги:\n• LOAD ≤50%, CORE ≤80%",
    "memory": "Использование памяти\n• Свободная память в %\n\nПорог:\n• FREE ≥20%",
    "access_if_count": "Access-if интерфейсы VXLAN\n• Общее количество интерфейсов\n\nПорог:\n• ≤14500",
    "mac_vrf_count": "MAC VRF\n• Количество MAC VRF\n\nПороги:\n• ≤2000 (WARNING: 1300-1500)",
    "irb_int_count": "IRB интерфейсы\n• Количество IRB интерфейсов\n\nПороги:\n• ≤2000 (WARNING: 1300-1500)",
    "l2vni_count": "L2 VNI\n• Количество L2 VNI\n\nПороги:\n• ≤4000 (WARNING: 3000-3500)",
    "l3_svi_count": "L3 SVI\n• Количество L3 SVI интерфейсов\n\nПорог:\n• ≤4030",
    "ip_vrf_count": "IP VRF\n• Количество IP VRF\n\nПороги:\n• ≤500 (WARNING: 400-450)",
    "evpn_route_count": "EVPN Route count: MAC-only, MAC-IPv4/v6\n• Использование таблицы EVPN маршрутов\n\nПорог:\n• ≤80%",
    "asic_mac_addr_count": "ASIC MAC таблица (зависит от forwarding HW profile)\n\nПорог:\n• ≤80%",
    "es_lag_count": "ES LAG сессии\n• Количество ES LAG сессий\n\nПорог:\n• ≤1800",
    "arp_count": "ARP записи\n• Количество ARP записей\n\nПорог:\n• ≤144K",
    "ipv4_routes": "IPv4 маршруты\n• Количество IPv4 маршрутов\n\nПорог:\n• ≤32K",
    "ecmp_groups": "ECMP группы\n• Использование ECMP групп\n\nПорог:\n• ≤80%",
    "l3_nexthop": "L3 next-hop\n• Использование next-hop записей\n\nПорог:\n• ≤80%",
}

THRESHOLD_TOOLTIP = """⚠️ ВНИМАНИЕ: Пороговые значения зависят от топологии и дизайна сети.
Рекомендуется уточнять актуальные пороги у представителей B4com."""

def get_metric_tooltip(metric_name: str) -> str:
    """Возвращает подсказку для метрики"""
    return METRIC_TOOLTIPS.get(metric_name, "Информация о метрике")

def get_all_tooltips() -> dict:
    """Возвращает все подсказки"""
    return METRIC_TOOLTIPS.copy()