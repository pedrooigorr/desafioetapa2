"""
Gamificação e Perfil — conquistas (badges), progresso de exploração e o
perfil leve do usuário (apelido + avatar, sem senha).

Três mecânicas, todas em cima do que a pessoa já faz naturalmente no app:

  1. **Conquistas**: desbloqueadas conforme a pessoa registra pedidos na
     Demanda Cidadã (primeiro pedido, pedidos em várias mesorregiões...).
  2. **Progresso de exploração**: conta quantos dos 184 municípios a
     pessoa já "visitou" — seja abrindo na Demanda Cidadã, seja clicando
     num ponto do mapa do Simulador.
  3. **Perfil**: apelido + avatar (emoji) escolhidos pela pessoa, sem
     senha nem conta — é só pra dar identidade ao "Meu Perfil", não é
     autenticação de verdade.

Persistência: sessão do navegador, como o resto do protótipo — zera ao
recarregar a página. É de propósito: sem infraestrutura externa (banco
de dados, login), o app continua de custo e manutenção zero.
"""

from __future__ import annotations

import streamlit as st

TOTAL_MUNICIPIOS_CE = 184

AVATARES = ["🎭", "🎨", "📚", "🎬", "🎪", "🎵", "🖼️", "🏛️", "🌵", "☀️"]


# ----------------------------------------------------------------------
# Perfil (apelido + avatar — sem senha, sem conta)
# ----------------------------------------------------------------------
def inicializar_perfil():
    st.session_state.setdefault("perfil_apelido", "")
    st.session_state.setdefault("perfil_local", "")
    st.session_state.setdefault("perfil_avatar", AVATARES[0])


def perfil_definido() -> bool:
    return bool(st.session_state.get("perfil_apelido", "").strip())


def nome_exibicao() -> str:
    return st.session_state.get("perfil_apelido", "").strip() or "Visitante"


# ----------------------------------------------------------------------
# Estado
# ----------------------------------------------------------------------
def inicializar_gamificacao():
    st.session_state.setdefault("municipios_explorados", set())
    st.session_state.setdefault("conquistas_vistas", set())
    inicializar_perfil()


def registrar_exploracao(municipio: str):
    """Marca um município como explorado. Chamado quando a pessoa abre o
    município na Demanda Cidadã ou clica nele no mapa do Simulador."""
    if not municipio:
        return
    st.session_state.setdefault("municipios_explorados", set()).add(municipio)


def total_explorados() -> int:
    return len(st.session_state.get("municipios_explorados", set()))


def progresso_exploracao() -> tuple[int, int, float]:
    """(explorados, total, fração de 0 a 1) — pronto pra st.progress."""
    explorados = total_explorados()
    return explorados, TOTAL_MUNICIPIOS_CE, explorados / TOTAL_MUNICIPIOS_CE


# ----------------------------------------------------------------------
# Conquistas
# ----------------------------------------------------------------------
# Cada conquista tem: id, ícone (nome Lucide), título, descrição e uma
# função que recebe o "contexto" (dados agregados da sessão) e diz se
# está desbloqueada.
CONQUISTAS = [
    {
        "id": "primeiro_pedido",
        "icone": "award",
        "titulo": "Primeiro Pedido",
        "descricao": "Registrou seu primeiro pedido cultural.",
        "meta": 1,
        "criterio": lambda ctx: ctx["n_pedidos"] >= 1,
        "progresso": lambda ctx: min(ctx["n_pedidos"], 1),
    },
    {
        "id": "explorador",
        "icone": "map",
        "titulo": "Explorador",
        "descricao": "Explorou 5 municípios diferentes.",
        "meta": 5,
        "criterio": lambda ctx: ctx["n_explorados"] >= 5,
        "progresso": lambda ctx: min(ctx["n_explorados"], 5),
    },
    {
        "id": "voz_ativa",
        "icone": "megaphone",
        "titulo": "Voz Ativa",
        "descricao": "Registrou pedidos em 3 mesorregiões diferentes.",
        "meta": 3,
        "criterio": lambda ctx: ctx["n_mesorregioes"] >= 3,
        "progresso": lambda ctx: min(ctx["n_mesorregioes"], 3),
    },
    {
        "id": "cartografo",
        "icone": "map-pinned",
        "titulo": "Cartógrafo",
        "descricao": "Explorou 20 municípios diferentes.",
        "meta": 20,
        "criterio": lambda ctx: ctx["n_explorados"] >= 20,
        "progresso": lambda ctx: min(ctx["n_explorados"], 20),
    },
    {
        "id": "atento_ao_deserto",
        "icone": "sun",
        "titulo": "Atento ao Deserto",
        "descricao": "Registrou um pedido num município que é Deserto Cultural.",
        "meta": 1,
        "criterio": lambda ctx: ctx["pediu_em_deserto"],
        "progresso": lambda ctx: 1 if ctx["pediu_em_deserto"] else 0,
    },
    {
        "id": "mobilizador",
        "icone": "users",
        "titulo": "Mobilizador",
        "descricao": "Registrou pedidos em 10 municípios diferentes.",
        "meta": 10,
        "criterio": lambda ctx: ctx["n_pedidos"] >= 10,
        "progresso": lambda ctx: min(ctx["n_pedidos"], 10),
    },
]


def _montar_contexto(df) -> dict:
    """Junta os números da sessão que as conquistas usam como critério."""
    pedidos = st.session_state.get("pedidos", {})
    municipios_com_pedido = list(pedidos.keys())

    if municipios_com_pedido:
        recorte = df[df["municipio"].isin(municipios_com_pedido)]
        n_mesorregioes = recorte["mesorregiao"].nunique()
        pediu_em_deserto = bool((recorte["n_equipamentos_raros"] == 0).any())
    else:
        n_mesorregioes = 0
        pediu_em_deserto = False

    return {
        "n_pedidos": len(municipios_com_pedido),
        "n_explorados": total_explorados(),
        "n_mesorregioes": n_mesorregioes,
        "pediu_em_deserto": pediu_em_deserto,
    }


def avaliar_conquistas(df) -> list[dict]:
    """
    Devolve a lista de conquistas com o estado atual de cada uma:
    desbloqueada ou não, e o progresso rumo à meta.
    """
    ctx = _montar_contexto(df)
    resultado = []
    for c in CONQUISTAS:
        atual = c["progresso"](ctx)
        resultado.append(
            {
                "id": c["id"],
                "icone": c["icone"],
                "titulo": c["titulo"],
                "descricao": c["descricao"],
                "desbloqueada": bool(c["criterio"](ctx)),
                "atual": atual,
                "meta": c["meta"],
            }
        )
    return resultado


def conquistas_desbloqueadas(df) -> list[dict]:
    return [c for c in avaliar_conquistas(df) if c["desbloqueada"]]


def resumo_conquistas(df) -> tuple[int, int]:
    """(quantas desbloqueadas, total de conquistas)."""
    todas = avaliar_conquistas(df)
    return sum(1 for c in todas if c["desbloqueada"]), len(todas)