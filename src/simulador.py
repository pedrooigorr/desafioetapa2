"""
Feature 3 — Simulador de Investimento Cultural.

Deixa o gestor escolher um tipo de equipamento e um raio de atuação, clicar
num município no mapa, e ver o impacto simulado de instalar esse
equipamento ali: quantas pessoas passariam a ter acesso, e o quanto isso
reduziria o déficit cultural da mesorregião.

Também inclui o Termômetro de Investimento Público — que cruza o Índice de
Prioridade (Radar Cultural) com valores de investimento público. Os
valores usados aqui são ILUSTRATIVOS (ver função gerar_investimento_ilustrativo
e data/README.md) — o dado real existe e é público via SALIC/Lei Rouanet,
mas não foi possível integrá-lo automaticamente neste protótipo.
"""

from __future__ import annotations

import pandas as pd

from src.geo import haversine_km

TIPOS_EQUIPAMENTO = {
    "tem_museu": "Museu",
    "tem_teatro_sala_espetaculo": "Teatro / Sala de espetáculo",
    "tem_cinema": "Cinema",
}


def calcular_simulacao(
    df: pd.DataFrame, municipio_alvo: str, coluna_equipamento: str, raio_km: float
) -> dict:
    """
    Simula o impacto de instalar o equipamento `coluna_equipamento` no
    município `municipio_alvo`, com um raio de atuação de `raio_km`.
    """
    alvo = df.loc[df["municipio"] == municipio_alvo].iloc[0]
    mesorregiao = alvo["mesorregiao"]

    distancias = df.apply(
        lambda linha: haversine_km(alvo["lat"], alvo["lon"], linha["lat"], linha["lon"]),
        axis=1,
    )
    dentro_do_raio = distancias <= raio_km

    # Pessoas que passam a ter acesso: municípios dentro do raio que HOJE
    # não têm esse equipamento (o próprio alvo incluso, se for o caso)
    sem_equipamento_hoje = ~df[coluna_equipamento]
    beneficiados = df[dentro_do_raio & sem_equipamento_hoje]
    populacao_beneficiada = int(beneficiados["populacao"].sum())
    municipios_beneficiados = beneficiados["municipio"].tolist()

    # Impacto no déficit da mesorregião: % de municípios sem o equipamento,
    # antes x depois de considerar quem passaria a ter acesso
    df_meso = df[df["mesorregiao"] == mesorregiao]
    tinha_antes = df_meso[coluna_equipamento]
    pct_antes = 100 * (~tinha_antes).mean()

    passa_a_ter = df_meso["municipio"].isin(municipios_beneficiados) | (
        df_meso["municipio"] == municipio_alvo
    )
    tem_depois = tinha_antes | passa_a_ter
    pct_depois = 100 * (~tem_depois).mean()

    reducao_pp = pct_antes - pct_depois
    reducao_relativa = (reducao_pp / pct_antes * 100) if pct_antes > 0 else 0.0

    return {
        "municipio_alvo": municipio_alvo,
        "mesorregiao": mesorregiao,
        "populacao_beneficiada": populacao_beneficiada,
        "n_municipios_beneficiados": len(municipios_beneficiados),
        "municipios_beneficiados": municipios_beneficiados,
        "pct_sem_equipamento_antes": pct_antes,
        "pct_sem_equipamento_depois": pct_depois,
        "reducao_pp": reducao_pp,
        "reducao_relativa": reducao_relativa,
    }