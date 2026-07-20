"""
Funções geográficas compartilhadas — usadas tanto no Feed Cultural (cálculo
de "a X km de você") quanto no Simulador de Investimento (raio de atuação).
"""

import math


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância em linha reta (km) entre duas coordenadas."""
    raio_terra = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * raio_terra * math.asin(math.sqrt(a))