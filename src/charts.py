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
    TEXTO_ESCURO,
    aplicar_texto_escuro,
    paleta_ativa,
)

_CEARA_CENTRO = {"lat": -5.32, "lon": -39.34}
_CEARA_ZOOM = 6.3
_COR_FUNDO_PAGINA = "#FFFDF8"  # mesma cor de fundo do app (config.toml)


def mapa_municipios(
    df: pd.DataFrame, altura: int = 600, municipio_destacado: str | None = None
):
    """
    Mapa real (OpenStreetMap, com nomes de cidades e estradas) mostrando
    só o Ceará — os estados vizinhos ficam "apagados" por uma máscara na
    cor de fundo do app, e um contorno terracota demarca a fronteira.
    Tem um ponto por município — tamanho proporcional à população (em
    escala raiz quadrada, para Fortaleza não "engolir" as bolhas menores),
    cor proporcional à renda per capita.

    Se `municipio_destacado` for passado (nome exato, vindo da busca), o
    mapa já abre centralizado e com zoom nele, e ganha um halo dourado
    ao redor do ponto pra confirmar visualmente qual foi encontrado.
    """
    paleta = paleta_ativa()
    df = df.copy()
    # Raiz quadrada comprime a escala: Fortaleza (~2,4 mi hab.) não deixa os
    # municípios pequenos praticamente invisíveis no mapa
    df["_tamanho"] = df["populacao"] ** 0.5

    centro, zoom = _CEARA_CENTRO, _CEARA_ZOOM
    linha_destacada = None
    if municipio_destacado:
        encontrado = df[df["municipio"] == municipio_destacado]
        if not encontrado.empty:
            linha_destacada = encontrado.iloc[0]
            centro = {"lat": linha_destacada["lat"], "lon": linha_destacada["lon"]}
            zoom = 10.5

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
            colorscale=[[0, paleta["deserto"]], [1, paleta["deserto"]]],
            showscale=False,
            marker_opacity=0,
            marker_line_color=paleta["deserto"],
            marker_line_width=2.5,
            hoverinfo="skip",
        )
    )

    # Camada 3 (só quando tem busca): halo dourado por baixo do ponto
    # encontrado — desenhado ANTES dos pontos normais pra ficar atrás,
    # como um círculo maior e translúcido em volta do ponto de verdade.
    if linha_destacada is not None:
        fig.add_trace(
            go.Scattermapbox(
                lat=[linha_destacada["lat"]],
                lon=[linha_destacada["lon"]],
                mode="markers",
                marker={"size": 42, "color": "#FFD700", "opacity": 0.55},
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Camada 4: um ponto por município, por cima de tudo
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
        color_continuous_scale=paleta["sequencial"],
        size_max=27,
        labels={
            "renda_per_capita": "Renda per capita (R$, Censo 2022)",
            "mesorregiao": "Mesorregião",
            "n_equipamentos": "Nº de equipamentos",
            "populacao": "População",
        },
    ).data[0]
    pontos.marker.sizemin = 3.5
    fig.add_trace(pontos)

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox={"center": centro, "zoom": zoom},
        height=altura,
        margin={"t": 10, "l": 0, "r": 0, "b": 0},
        coloraxis={
            "colorscale": paleta["sequencial"],
            "cmin": df["renda_per_capita"].min(),
            "cmax": df["renda_per_capita"].max(),
            "colorbar": {
                "title": {"text": "Renda per<br>capita (R$)", "font": {"color": TEXTO_ESCURO}},
                "tickfont": {"color": TEXTO_ESCURO},
            },
        },
        font={"color": TEXTO_ESCURO, "size": 13},
    )
    return fig


def mapa_simulador(
    df: pd.DataFrame,
    coluna_equipamento: str,
    altura: int = 600,
    rotulo_equipamento: str = "o equipamento",
    municipio_destacado: str | None = None,
):
    """
    Mapa clicável para o Simulador de Investimento: cada município aparece
    colorido conforme TEM ou NÃO TEM o equipamento escolhido — verde
    "cactos" para quem tem, terracota para quem não tem (deserto cultural).
    Usa `custom_data=["municipio"]` para que o clique no ponto (via
    `st.plotly_chart(..., on_select="rerun")`) identifique qual município
    foi selecionado.

    Se `municipio_destacado` for passado (nome exato, vindo da busca), o
    mapa já abre centralizado e com zoom nele, com um halo dourado ao
    redor do ponto pra confirmar visualmente qual foi encontrado.
    """
    paleta = paleta_ativa()
    df = df.copy()
    df["_status"] = df[coluna_equipamento].map(
        {True: "Tem", False: "Deserto Cultural"}
    )
    df["_tamanho"] = df["populacao"] ** 0.5

    centro, zoom = _CEARA_CENTRO, _CEARA_ZOOM
    linha_destacada = None
    if municipio_destacado:
        encontrado = df[df["municipio"] == municipio_destacado]
        if not encontrado.empty:
            linha_destacada = encontrado.iloc[0]
            centro = {"lat": linha_destacada["lat"], "lon": linha_destacada["lon"]}
            zoom = 10.5

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
            colorscale=[[0, paleta["deserto"]], [1, paleta["deserto"]]],
            showscale=False,
            marker_opacity=0,
            marker_line_color=paleta["deserto"],
            marker_line_width=2.5,
            hoverinfo="skip",
        )
    )

    if linha_destacada is not None:
        fig.add_trace(
            go.Scattermapbox(
                lat=[linha_destacada["lat"]],
                lon=[linha_destacada["lon"]],
                mode="markers",
                marker={"size": 40, "color": "#FFD700", "opacity": 0.55},
                hoverinfo="skip",
                showlegend=False,
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
        # O par de cores vem da paleta ativa (paleta_ativa()["tem"]/
        # ["nao_tem"]) — já nasce evitando a combinação verde/vermelho,
        # a mais difícil pra quem tem daltonismo, e se ajusta ainda mais
        # conforme o modo escolhido em Acessibilidade
        color_discrete_map={"Tem": paleta["tem"], "Deserto Cultural": paleta["nao_tem"]},
        size_max=26,
        labels={"_status": "Situação"},
    )
    for trace in pontos_fig.data:
        trace.marker.sizemin = 4
        # O nome do trace é o próprio status ("Tem" / "Deserto Cultural"),
        # então dá pra mostrá-lo no hover sem passar customdata extra
        sufixo = (
            "🏜️ Deserto Cultural"
            if trace.name == "Deserto Cultural"
            else f"Tem {rotulo_equipamento.lower()}"
        )
        trace.hovertemplate = (
            "<b>%{customdata[0]}</b><br>" + sufixo + "<extra></extra>"
        )
        fig.add_trace(trace)

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox={"center": centro, "zoom": zoom},
        height=altura,
        margin={"t": 10, "l": 0, "r": 0, "b": 0},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.01, "xanchor": "left", "x": 0},
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
            "renda_per_capita": "Renda per capita (R$, Censo 2022)",
            "n_equipamentos": "Nº de equipamentos culturais",
            "mesorregiao": "Mesorregião",
        },
        opacity=0.8,
        color_discrete_sequence=paleta_ativa()["discreta"],
    )
    fig.update_layout(yaxis={"dtick": 1}, height=altura, margin={"t": 10})
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
        color_continuous_scale=paleta_ativa()["sequencial"],
    )
    fig.update_traces(
        textposition="outside",
        textfont={"color": TEXTO_ESCURO, "size": 13},
        cliponaxis=False,
    )
    fig.update_layout(
        coloraxis_showscale=False,
        height=altura,
        margin={"t": 10},
        xaxis={"range": [0, 112]},
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
        color_continuous_scale=paleta_ativa()["sequencial"],
    )
    fig.update_traces(
        textposition="outside",
        textfont={"color": TEXTO_ESCURO, "size": 13},
        cliponaxis=False,
    )
    # Sem isso, o hover mostra a renda média com todas as casas decimais
    # do float bruto (ex: 267.6351086956522) em vez de "267.64"
    for trace in fig.data:
        trace.hovertemplate = trace.hovertemplate.replace(
            "%{marker.color}", "%{marker.color:.2f}"
        )
    fig.update_xaxes(tickangle=-25)
    fig.update_layout(height=altura, margin={"t": 10})
    aplicar_texto_escuro(fig)
    return fig