"""
Funções que constroem cada visualização do Radar Cultural em Plotly.

Cada função recebe o DataFrame já filtrado e uma altura em pixels — usada
tanto para os painéis compactos da Visão Geral (altura menor) quanto para
as páginas dedicadas de cada gráfico (altura maior).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.ceara_boundary import CEARA_GEOJSON
from src.data_loader import EQUIPAMENTOS
from src.mascara_fora_ceara import MASCARA_GEOJSON
from src.theme import (
    NORDESTE_DISCRETA,
    NORDESTE_SEQUENCIAL,
    TEXTO_ESCURO,
    aplicar_texto_escuro,
)

_CEARA_CENTRO = {"lat": -5.32, "lon": -39.34}
_CEARA_ZOOM = 6.3
_COR_FUNDO_PAGINA = "#FFFDF8"  # mesma cor de fundo do app (config.toml)


def mapa_municipios(df: pd.DataFrame, altura: int = 600):
    """
    Mapa real (OpenStreetMap, com nomes de cidades e estradas) mostrando
    só o Ceará — os estados vizinhos ficam "apagados" por uma máscara na
    cor de fundo do app, e um contorno terracota demarca a fronteira.
    Tem um ponto por município — tamanho proporcional à população (em
    escala raiz quadrada, para Fortaleza não "engolir" as bolhas menores),
    cor proporcional à renda per capita.
    """
    df = df.copy()
    # Raiz quadrada comprime a escala: Fortaleza (~2,4 mi hab.) não deixa os
    # municípios pequenos praticamente invisíveis no mapa
    df["_tamanho"] = df["populacao"] ** 0.5

    fig = go.Figure()

    # Camada 1: máscara cobrindo tudo AO REDOR do Ceará, na cor de fundo do
    # app — "apaga" visualmente os estados vizinhos sem esconder o mapa
    # real (ruas, nomes de cidades) dentro do próprio Ceará
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=MASCARA_GEOJSON,
            locations=["mascara"],
            z=[1],
            featureidkey="properties.id",
            colorscale=[[0, _COR_FUNDO_PAGINA], [1, _COR_FUNDO_PAGINA]],
            showscale=False,
            marker_line_width=0,
            hoverinfo="skip",
        )
    )

    # Camada 2: contorno do Ceará (só a borda, dá o acabamento visual)
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=CEARA_GEOJSON,
            locations=["CE"],
            z=[1],
            featureidkey="properties.SIGLA",
            colorscale=[[0, "#C1440E"], [1, "#C1440E"]],
            showscale=False,
            marker_opacity=0,
            marker_line_color="#C1440E",
            marker_line_width=2.5,
            hoverinfo="skip",
        )
    )

    # Camada 3: um ponto por município, por cima de tudo
    pontos = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="_tamanho",
        color="renda_per_capita",
        hover_name="municipio",
        hover_data={
            "mesorregiao": True,
            "renda_per_capita": ":.2f",
            "n_equipamentos": True,
            "populacao": ":,",
            "_tamanho": False,
            "lat": False,
            "lon": False,
        },
        color_continuous_scale=NORDESTE_SEQUENCIAL,
        size_max=27,
        labels={
            "renda_per_capita": "Renda per capita (R$)",
            "mesorregiao": "Mesorregião",
            "n_equipamentos": "Nº de equipamentos",
            "populacao": "População",
        },
    ).data[0]
    pontos.marker.sizemin = 3.5
    fig.add_trace(pontos)

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=_CEARA_CENTRO, zoom=_CEARA_ZOOM),
        height=altura,
        margin=dict(t=10, l=0, r=0, b=0),
        coloraxis=dict(
            colorscale=NORDESTE_SEQUENCIAL,
            cmin=df["renda_per_capita"].min(),
            cmax=df["renda_per_capita"].max(),
            colorbar=dict(
                title=dict(text="Renda per<br>capita (R$)", font=dict(color=TEXTO_ESCURO)),
                tickfont=dict(color=TEXTO_ESCURO),
            ),
        ),
        font=dict(color=TEXTO_ESCURO, size=13),
    )
    return fig


def mapa_simulador(df: pd.DataFrame, coluna_equipamento: str, altura: int = 600):
    """
    Mapa clicável para o Simulador de Investimento: cada município aparece
    colorido conforme TEM ou NÃO TEM o equipamento escolhido — verde
    "cactos" para quem tem, terracota para quem não tem (deserto cultural).
    Usa `custom_data=["municipio"]` para que o clique no ponto (via
    `st.plotly_chart(..., on_select="rerun")`) identifique qual município
    foi selecionado.
    """
    df = df.copy()
    df["_status"] = df[coluna_equipamento].map({True: "Tem", False: "Não tem"})
    df["_tamanho"] = df["populacao"] ** 0.5

    fig = go.Figure()

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=MASCARA_GEOJSON,
            locations=["mascara"],
            z=[1],
            featureidkey="properties.id",
            colorscale=[[0, _COR_FUNDO_PAGINA], [1, _COR_FUNDO_PAGINA]],
            showscale=False,
            marker_line_width=0,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=CEARA_GEOJSON,
            locations=["CE"],
            z=[1],
            featureidkey="properties.SIGLA",
            colorscale=[[0, "#C1440E"], [1, "#C1440E"]],
            showscale=False,
            marker_opacity=0,
            marker_line_color="#C1440E",
            marker_line_width=2.5,
            hoverinfo="skip",
        )
    )

    pontos_fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="_tamanho",
        color="_status",
        custom_data=["municipio"],
        hover_name="municipio",
        color_discrete_map={"Tem": "#4C6444", "Não tem": "#C1440E"},
        size_max=26,
        labels={"_status": "Situação"},
    )
    for trace in pontos_fig.data:
        trace.marker.sizemin = 4
        trace.hovertemplate = "<b>%{customdata[0]}</b><extra></extra>"
        fig.add_trace(trace)

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=_CEARA_CENTRO, zoom=_CEARA_ZOOM),
        height=altura,
        margin=dict(t=10, l=0, r=0, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
        clickmode="event+select",
    )
    aplicar_texto_escuro(fig)
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
    aplicar_texto_escuro(fig)
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
    fig.update_traces(
        textposition="outside",
        textfont=dict(color=TEXTO_ESCURO, size=13),
        cliponaxis=False,
    )
    fig.update_layout(
        coloraxis_showscale=False,
        height=altura,
        margin=dict(t=10),
        xaxis=dict(range=[0, 112]),
    )
    aplicar_texto_escuro(fig)
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
    fig.update_traces(
        textposition="outside",
        textfont=dict(color=TEXTO_ESCURO, size=13),
        cliponaxis=False,
    )
    fig.update_xaxes(tickangle=-25)
    fig.update_layout(height=altura, margin=dict(t=10))
    aplicar_texto_escuro(fig)
    return fig