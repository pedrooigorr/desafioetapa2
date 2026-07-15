"""
Funções que constroem cada visualização do Radar Cultural em Plotly.

Cada função recebe o DataFrame já filtrado e uma altura em pixels — usada
tanto para os painéis compactos da Visão Geral (altura menor) quanto para
as páginas dedicadas de cada gráfico (altura maior).
"""

import pandas as pd
import plotly.express as px

from src.data_loader import EQUIPAMENTOS
from src.theme import NORDESTE_DISCRETA, NORDESTE_SEQUENCIAL


def mapa_municipios(df: pd.DataFrame, altura: int = 600):
    """
    Mapa do Ceará com um ponto por município — tamanho proporcional à
    população, cor proporcional à renda per capita. Usa OpenStreetMap
    (não precisa de token do Mapbox).
    """
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="populacao",
        color="renda_per_capita",
        hover_name="municipio",
        hover_data={
            "mesorregiao": True,
            "renda_per_capita": ":.2f",
            "n_equipamentos": True,
            "populacao": ":,",
            "lat": False,
            "lon": False,
        },
        color_continuous_scale=NORDESTE_SEQUENCIAL,
        size_max=32,
        zoom=6,
        center={"lat": -5.2, "lon": -39.3},
        labels={
            "renda_per_capita": "Renda per capita (R$)",
            "mesorregiao": "Mesorregião",
            "n_equipamentos": "Nº de equipamentos",
            "populacao": "População",
        },
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        height=altura,
        margin=dict(t=10, l=0, r=0, b=0),
    )
    return fig


def grafico_renda_x_equipamentos(df: pd.DataFrame, altura: int = 420):
    """Dispersão: renda per capita x nº de equipamentos culturais."""
    fig = px.scatter(
        df,
        x="renda_per_capita",
        y="n_equipamentos",
        size="populacao",
        color="mesorregiao",
        hover_name="municipio",
        labels={
            "renda_per_capita": "Renda per capita (R$)",
            "n_equipamentos": "Nº de equipamentos culturais",
            "mesorregiao": "Mesorregião",
        },
        opacity=0.8,
        color_discrete_sequence=NORDESTE_DISCRETA,
    )
    fig.update_layout(yaxis=dict(dtick=1), height=altura, margin=dict(t=10))
    return fig


def grafico_presenca_equipamentos(df: pd.DataFrame, altura: int = 420):
    """Barras horizontais: % de municípios que têm cada equipamento."""
    presenca = pd.DataFrame(
        {
            "Equipamento": list(EQUIPAMENTOS.values()),
            "% dos municípios que têm": [
                100 * df[col].mean() if len(df) else 0 for col in EQUIPAMENTOS
            ],
        }
    ).sort_values("% dos municípios que têm")

    fig = px.bar(
        presenca,
        x="% dos municípios que têm",
        y="Equipamento",
        orientation="h",
        text_auto=".1f",
        color="% dos municípios que têm",
        color_continuous_scale=NORDESTE_SEQUENCIAL,
    )
    fig.update_layout(coloraxis_showscale=False, height=altura, margin=dict(t=10))
    return fig


def grafico_equidade_por_mesorregiao(df: pd.DataFrame, altura: int = 420):
    """Barras: % de municípios sem museu/teatro/cinema, por mesorregião."""
    por_meso = (
        df.groupby("mesorregiao")
        .agg(
            municipios=("municipio", "count"),
            pct_sem_equipamento=(
                "n_equipamentos_raros",
                lambda s: 100 * (s == 0).mean(),
            ),
            renda_media=("renda_per_capita", "mean"),
        )
        .reset_index()
        .sort_values("pct_sem_equipamento", ascending=False)
    )

    fig = px.bar(
        por_meso,
        x="mesorregiao",
        y="pct_sem_equipamento",
        color="renda_media",
        text_auto=".1f",
        labels={
            "mesorregiao": "Mesorregião",
            "pct_sem_equipamento": "% de municípios sem museu, teatro ou cinema",
            "renda_media": "Renda média per capita (R$)",
        },
        color_continuous_scale=NORDESTE_SEQUENCIAL,
    )
    fig.update_xaxes(tickangle=-25)
    fig.update_layout(height=altura, margin=dict(t=10))
    return fig