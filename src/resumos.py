"""
Resumos automáticos — frases geradas a partir dos dados reais de cada
painel. Servem dois propósitos de acessibilidade ao mesmo tempo:

  1. O resumo de 1 frase no topo de cada painel (orientação rápida pra
     quem se perde fácil em muita informação, ou quer confirmar que
     está no lugar certo antes de explorar).
  2. O "resumo automático dos gráficos" — dá pra quem usa leitor de tela
     captar o insight principal sem precisar navegar gráfico por
     gráfico, já que um SVG de gráfico não é lido de forma útil por
     leitores de tela.

Cada função aqui recebe o DataFrame já filtrado (mesmo filtro que a
pessoa está vendo na tela) e devolve uma única frase pronta.
"""

from __future__ import annotations

import pandas as pd

from src.data_loader import EQUIPAMENTOS


def resumo_visao_geral(df: pd.DataFrame) -> str:
    if df.empty:
        return "Nenhum município corresponde aos filtros escolhidos."
    sem_nenhum = int((df["n_equipamentos_raros"] == 0).sum())
    total = len(df)
    pct = 100 * sem_nenhum / total
    return (
        f"Visão geral do Radar Cultural: dos {total} municípios "
        f"filtrados, {sem_nenhum} ({pct:.0f}%) não têm nenhum museu, "
        f"teatro ou cinema."
    )


def resumo_mapa(df: pd.DataFrame) -> str:
    if df.empty:
        return "Nenhum município corresponde aos filtros escolhidos."
    sem_nenhum = int((df["n_equipamentos_raros"] == 0).sum())
    renda_media = df["renda_per_capita"].mean()
    return (
        f"O mapa mostra {len(df)} municípios do Ceará. {sem_nenhum} "
        f"deles não têm museu, teatro nem cinema, e a renda per capita "
        f"média desse grupo é de R$ {renda_media:.2f} (Censo 2022)."
    )


def resumo_presenca_equipamentos(df: pd.DataFrame) -> str:
    if df.empty:
        return "Nenhum município corresponde aos filtros escolhidos."
    percentuais = {
        nome: 100 * df[col].mean() for col, nome in EQUIPAMENTOS.items()
    }
    mais_raro = min(percentuais, key=percentuais.get)
    pct = percentuais[mais_raro]
    return (
        f"Entre os equipamentos culturais rastreados, {mais_raro.lower()} "
        f"é o mais raro: só {pct:.0f}% dos municípios filtrados têm um."
    )


def resumo_equidade_mesorregiao(df: pd.DataFrame) -> str:
    if df.empty or df["mesorregiao"].nunique() == 0:
        return "Nenhum município corresponde aos filtros escolhidos."
    por_meso = (
        df.groupby("mesorregiao")["n_equipamentos_raros"]
        .apply(lambda s: 100 * (s == 0).mean())
        .sort_values(ascending=False)
    )
    pior = por_meso.index[0]
    pct = por_meso.iloc[0]
    return (
        f"A mesorregião com maior déficit cultural, entre as filtradas, "
        f"é {pior}: {pct:.0f}% dos seus municípios não têm museu, "
        f"teatro nem cinema."
    )


def resumo_municipios_prioritarios(df: pd.DataFrame) -> str:
    if df.empty:
        return "Nenhum município corresponde aos filtros escolhidos."
    top = df.sort_values("indice_prioridade", ascending=False).iloc[0]
    return (
        f"{top['municipio']} lidera o ranking de deserto cultural entre "
        f"os municípios filtrados, com Índice de Prioridade "
        f"{top['indice_prioridade']:.2f}."
    )


def resumo_demanda_cidada() -> str:
    return (
        "Escolha o seu município, veja o que já existe lá e registre o "
        "que mais falta — cada pedido pesa no ranking de prioridades e "
        "sugere investimentos no Simulador."
    )


def resumo_simulador() -> str:
    return (
        "Escolha um tipo de equipamento cultural e um raio de atuação "
        "na barra lateral, depois clique num município no mapa pra ver "
        "quantas pessoas passariam a ter acesso cultural."
    )


def resumo_transparencia(ranking_publico: pd.DataFrame) -> str:
    if ranking_publico.empty:
        return "Nenhum dado disponível para o Painel de Transparência."
    top = ranking_publico.iloc[0]
    return (
        f"Ranking público de deserto cultural do Ceará — "
        f"{top['Município']} está em 1º lugar, com Índice de Prioridade "
        f"{top['Índice de Prioridade']:.2f}."
    )