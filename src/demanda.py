"""
Feature 2 (revisada) — Demanda Cidadã.

Substitui o antigo "Cultura Perto de Mim" (feed de eventos). Em vez de um
feed de descoberta, o cidadão escolhe o município dele, vê o que já
existe (dado real do Radar Cultural) e registra, entre o que falta, o que
mais gostaria de ver — uma ação só, sem dois fluxos separados.

Isso alimenta três coisas:
  1. Um contador público por município ("148 pessoas em Granja pedem
     uma biblioteca").
  2. Um peso extra no Índice de Prioridade (ver `indice_prioridade_ajustado`).
  3. Uma sugestão automática de equipamento no Simulador de Investimento.

Persistência: sessão do navegador — os pedidos somem ao recarregar a
página (mesma decisão de escopo usada em todo o protótipo).
"""

from __future__ import annotations

import streamlit as st

# Categorias que já são rastreadas no dataset real do Radar Cultural
MAPA_CATEGORIA_COLUNA = {
    "Biblioteca": "tem_biblioteca",
    "Museu": "tem_museu",
    "Teatro / Sala de espetáculo": "tem_teatro_sala_espetaculo",
    "Cinema": "tem_cinema",
}

# Categorias "aspiracionais" — não têm coluna no dataset (não existe uma
# pesquisa oficial que rastreie isso), então contam sempre como pedido
# possível, em qualquer município
CATEGORIAS_ASPIRACIONAIS = ["Centro Cultural", "Oficina Itinerante Cultural"]

# Categorias que o Simulador de Investimento sabe simular hoje
CATEGORIAS_SIMULAVEIS = {
    "Museu": "tem_museu",
    "Teatro / Sala de espetáculo": "tem_teatro_sala_espetaculo",
    "Cinema": "tem_cinema",
}


def inicializar_pedidos():
    if "pedidos" not in st.session_state:
        st.session_state.pedidos = {}


def categorias_existentes(df, municipio: str) -> list[str]:
    """O que o município JÁ tem, entre as categorias rastreadas."""
    linha = df.loc[df["municipio"] == municipio].iloc[0]
    return [cat for cat, col in MAPA_CATEGORIA_COLUNA.items() if linha[col]]


def categorias_faltantes(df, municipio: str) -> list[str]:
    """O que falta — inclui as categorias aspiracionais, que 'faltam'
    em todo lugar por não termos como confirmar que existem."""
    linha = df.loc[df["municipio"] == municipio].iloc[0]
    faltantes = [cat for cat, col in MAPA_CATEGORIA_COLUNA.items() if not linha[col]]
    return faltantes + CATEGORIAS_ASPIRACIONAIS


def registrar_pedido(municipio: str, categoria: str):
    pedidos_municipio = st.session_state.pedidos.setdefault(municipio, {})
    pedidos_municipio[categoria] = pedidos_municipio.get(categoria, 0) + 1


def pedidos_do_municipio(municipio: str) -> dict:
    return st.session_state.pedidos.get(municipio, {})


def total_pedidos(municipio: str) -> int:
    return sum(pedidos_do_municipio(municipio).values())


def categoria_mais_pedida(municipio: str) -> tuple[str | None, int]:
    pedidos = pedidos_do_municipio(municipio)
    if not pedidos:
        return None, 0
    categoria = max(pedidos, key=pedidos.get)
    return categoria, pedidos[categoria]


def peso_demanda(municipio: str, escala: float = 0.05) -> float:
    """
    Quanto esse município deve pesar a mais no Índice de Prioridade por
    causa da demanda cidadã registrada nesta sessão. Cresce com o total
    de pedidos, mas em raiz quadrada — pra um município com muitos votos
    não dominar sozinho o ranking todo.
    """
    total = total_pedidos(municipio)
    return (total**0.5) * escala


def indice_prioridade_ajustado(df):
    """Série com o Índice de Prioridade original + peso de demanda cidadã."""
    return df["indice_prioridade"] + df["municipio"].map(peso_demanda)


def ranking_pedidos_ceara() -> list[dict]:
    """Ranking de todos os municípios com pelo menos um pedido registrado
    nesta sessão, do mais pedido pro menos pedido."""
    linhas = []
    for municipio, pedidos in st.session_state.get("pedidos", {}).items():
        categoria, votos = categoria_mais_pedida(municipio)
        linhas.append(
            {
                "municipio": municipio,
                "categoria_mais_pedida": categoria,
                "votos_categoria": votos,
                "total_pedidos": sum(pedidos.values()),
            }
        )
    return sorted(linhas, key=lambda x: x["total_pedidos"], reverse=True)