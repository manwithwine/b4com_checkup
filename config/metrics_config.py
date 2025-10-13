"""
Регистрация всех метрик системы
"""
from metrics.cpu_metric import CPUMetric
from metrics.memory_metric import MemoryMetric
from metrics.access_if_metric import AccessIfMetric
from metrics.mac_vrf_metric import MacVrfMetric
from metrics.irb_int_metric import IrbIntMetric
from metrics.l2vni_metric import L2VNIMetric
from metrics.l3_svi_metric import L3SVIMetric
from metrics.ip_vrf_metric import IPVrfMetric
from metrics.evpn_route_count_metric import EVPNRouteCountMetric
from metrics.asic_mac_metric import AsicMacMetric
from metrics.es_lag_metric import ESLagMetric
from metrics.arp_metric import ARPMetric
from metrics.ipv4_routes_metric import IPv4RoutesMetric
from metrics.ecmp_groups_metric import ECMPMetric
from metrics.l3_nexthop_metric import L3NextHopMetric

# Регистрация всех метрик
METRICS_REGISTRY = {
    "cpu": CPUMetric(),
    "memory": MemoryMetric(),
    "access_if_count": AccessIfMetric(),
    "mac_vrf_count": MacVrfMetric(),
    "irb_int_count": IrbIntMetric(),
    "l2vni_count": L2VNIMetric(),
    "l3_svi_count": L3SVIMetric(),
    "ip_vrf_count": IPVrfMetric(),
    "evpn_route_count": EVPNRouteCountMetric(),
    "asic_mac_addr_count": AsicMacMetric(),
    "es_lag_count": ESLagMetric(),
    "arp_count": ARPMetric(),
    "ipv4_routes": IPv4RoutesMetric(),
    "ecmp_groups": ECMPMetric(),
    "l3_nexthop": L3NextHopMetric(),
}

def get_metric(metric_name: str):
    """Возвращает метрику по имени"""
    return METRICS_REGISTRY.get(metric_name)

def get_all_metrics():
    """Возвращает все зарегистрированные метрики"""
    return METRICS_REGISTRY.copy()

def get_metric_display_names():
    """Возвращает словарь {metric_name: display_name}"""
    return {name: metric.display_name for name, metric in METRICS_REGISTRY.items()}

def register_metric(metric_name: str, metric_instance):
    """Регистрирует новую метрику"""
    METRICS_REGISTRY[metric_name] = metric_instance

def unregister_metric(metric_name: str):
    """Удаляет метрику из регистра"""
    if metric_name in METRICS_REGISTRY:
        del METRICS_REGISTRY[metric_name]