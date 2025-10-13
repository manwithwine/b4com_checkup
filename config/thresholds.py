"""
Единый источник пороговых значений
"""

THRESHOLDS = {
    "cpu_load": 50,
    "cpu_core": 80,
    "memory_free": 20,
    "access_if": 14500,
    "mac_vrf": 2000,
    "irb_int": 2000,
    "l2vni": 4000,
    "l3_svi": 4030,
    "ip_vrf": 500,
    "evpn_route_count": 80,
    "asic_mac": 80,
    "es_lag": 1800,
    "arp": 144000,
    "ipv4_routes": 32768,
    "ecmp_groups": 80,
    "l3_nexthop": 80,
}

def get_threshold(metric_name: str):
    """Возвращает порог для метрики"""
    return THRESHOLDS.get(metric_name)

def get_threshold_row():
    """Возвращает строку с пороговыми значениями для таблиц"""
    return [
        "THRESHOLD", "",
        f"LOAD≤{THRESHOLDS['cpu_load']}%<br>CORE≤{THRESHOLDS['cpu_core']}%",
        f"FREE≥{THRESHOLDS['memory_free']}%",
        f"≤{THRESHOLDS['access_if']}",
        f"≤{THRESHOLDS['mac_vrf']}",
        f"≤{THRESHOLDS['irb_int']}",
        f"≤{THRESHOLDS['l2vni']}",
        f"≤{THRESHOLDS['l3_svi']}",
        f"≤{THRESHOLDS['ip_vrf']}",
        f"≤{THRESHOLDS['evpn_route_count']}%",
        f"≤{THRESHOLDS['asic_mac']}%",
        f"≤{THRESHOLDS['es_lag']}",
        f"≤{THRESHOLDS['arp']//1000}K",
        f"≤{THRESHOLDS['ipv4_routes']//1000}K",
        f"≤{THRESHOLDS['ecmp_groups']}%",
        f"≤{THRESHOLDS['l3_nexthop']}%"
    ]