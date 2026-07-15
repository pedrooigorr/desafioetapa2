"""
Carregamento e preparação dos dados do Radar Cultural.

Fontes:
  - Equipamentos culturais: IBGE — MUNIC, Suplemento de Cultura 2014
  - População e renda per capita: Atlas Brasil (PNUD), Censo 2010

Ver data/README.md para detalhes de como as duas bases foram cruzadas.
"""

import pandas as pd
import streamlit as st

DATA_PATH = "data/radar_cultural_ce.csv"

# Nome de exibição de cada coluna booleana de equipamento
EQUIPAMENTOS = {
    "tem_museu": "Museu",
    "tem_teatro_sala_espetaculo": "Teatro / Sala de espetáculo",
    "tem_cinema": "Cinema",
    "tem_biblioteca": "Biblioteca",
}

# Equipamentos que de fato diferenciam municípios entre si — biblioteca
# existe em 100% dos municípios do Ceará (ver data/README.md), então não
# entra no cálculo de prioridade/equidade
EQUIPAMENTOS_RAROS = ["tem_museu", "tem_teatro_sala_espetaculo", "tem_cinema"]


@st.cache_data
def carregar_dados(path: str = DATA_PATH) -> pd.DataFrame:
    """Lê o CSV combinado e calcula as colunas derivadas usadas no app."""
    df = pd.read_csv(path)

    for col in EQUIPAMENTOS:
        df[col] = df[col].astype(bool)

    df["n_equipamentos"] = df[list(EQUIPAMENTOS)].sum(axis=1)
    df["n_equipamentos_raros"] = df[EQUIPAMENTOS_RAROS].sum(axis=1)

    df["indice_prioridade"] = calcular_indice_prioridade(df)
    return df


def calcular_indice_prioridade(df: pd.DataFrame) -> pd.Series:
    """
    Índice de Equidade Cultural: combina ausência de equipamentos "raros"
    (museu, teatro, cinema) com baixa renda per capita.

    Quanto maior o índice, mais urgente a atenção — municípios de baixa
    renda SEM esses equipamentos pesam mais como prioridade.
    """
    renda_normalizada = df["renda_per_capita"] / df["renda_per_capita"].max()
    return (3 - df["n_equipamentos_raros"]) * (1 - renda_normalizada)


def montar_tabela_prioritarios(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """Monta a tabela de municípios prioritários, pronta para exibição."""
    top = df.sort_values("indice_prioridade", ascending=False).head(n)
    return top[
        [
            "municipio",
            "mesorregiao",
            "populacao",
            "renda_per_capita",
            "n_equipamentos",
            "indice_prioridade",
        ]
    ].rename(
        columns={
            "municipio": "Município",
            "mesorregiao": "Mesorregião",
            "populacao": "População",
            "renda_per_capita": "Renda per capita (R$)",
            "n_equipamentos": "Nº equipamentos",
            "indice_prioridade": "Índice de Prioridade",
        }
    )


def aplicar_filtros(
    df: pd.DataFrame,
    mesorregioes: list[str],
    faixa_populacao: tuple[int, int],
    excluir_fortaleza: bool,
    equipamentos_ausentes: list[str],
) -> pd.DataFrame:
    """Aplica os filtros escolhidos na sidebar e retorna o DataFrame filtrado."""
    df_f = df[
        df["mesorregiao"].isin(mesorregioes)
        & df["populacao"].between(*faixa_populacao)
    ]

    if excluir_fortaleza:
        df_f = df_f[df_f["municipio"] != "Fortaleza"]

    for label in equipamentos_ausentes:
        col = next(k for k, v in EQUIPAMENTOS.items() if v == label)
        df_f = df_f[~df_f[col]]

    return df_f