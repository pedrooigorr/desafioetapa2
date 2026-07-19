"""
Modelo de dados e lógica da Feature 2 — Feed Cultural: eventos cadastrados
por artistas/produtores locais, mostrados como cards estilo "stories" para
o cidadão descobrir o que está rolando perto dele.

Persistência: só durante a sessão do navegador (st.session_state) — os
dados somem ao recarregar a página. Foi uma escolha de escopo para o
protótipo, documentada em data/README.md.
"""

from __future__ import annotations

import base64
import math
from datetime import date, timedelta

import streamlit as st

# Categoria → cor (reaproveita a paleta Nordeste) e ícone
CATEGORIAS = {
    "Música": {"cor": "#C1440E", "icone": "🎵"},
    "Teatro": {"cor": "#1B7A8C", "icone": "🎭"},
    "Feira": {"cor": "#F2A93B", "icone": "🧺"},
    "Exposição": {"cor": "#4C6444", "icone": "🖼️"},
    "Dança": {"cor": "#8C1C13", "icone": "💃"},
    "Artesanato": {"cor": "#D9A441", "icone": "🏺"},
    "Outro": {"cor": "#6B4226", "icone": "✨"},
}

TIPOS_PRODUTOR = [
    "Artista individual",
    "Banda",
    "Grupo de teatro/dança",
    "Artesão(ã)",
    "Coletivo cultural",
    "Produtora/organização",
]


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Distância em linha reta (km) entre duas coordenadas."""
    raio_terra = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * raio_terra * math.asin(math.sqrt(a))


def calcular_distancia(df_municipios, municipio_origem: str, municipio_destino: str):
    """
    Distância aproximada (km) entre dois municípios do Ceará, usando as
    coordenadas já existentes no dataset do Radar Cultural. Simula a
    "notificação de proximidade" sem precisar de GPS real — o usuário
    escolhe "meu município" nos filtros.
    """
    if municipio_origem == municipio_destino:
        return 0.0
    linha_origem = df_municipios.loc[df_municipios["municipio"] == municipio_origem]
    linha_destino = df_municipios.loc[df_municipios["municipio"] == municipio_destino]
    if linha_origem.empty or linha_destino.empty:
        return None
    o, d = linha_origem.iloc[0], linha_destino.iloc[0]
    return round(_haversine_km(o["lat"], o["lon"], d["lat"], d["lon"]), 1)


def badge_temporal(data_evento: date) -> tuple[str, str]:
    """Texto e cor do selo de urgência temporal (ex: 'Hoje!', 'Em 3 dias')."""
    dias = (data_evento - date.today()).days
    if dias == 0:
        return "🔥 Hoje!", "#C1440E"
    if dias == 1:
        return "⏰ Amanhã!", "#F2A93B"
    if 1 < dias <= 7:
        return f"📅 Em {dias} dias", "#1B7A8C"
    if dias > 7:
        return data_evento.strftime("📆 %d/%m"), "#6B4226"
    return "Encerrado", "#9C9187"


def imagens_para_base64(arquivos_upload) -> list[str]:
    """Converte as imagens enviadas no formulário (uma ou várias) em uma
    lista de base64, para exibir no carrossel do card."""
    if not arquivos_upload:
        return []
    return [base64.b64encode(arq.getvalue()).decode() for arq in arquivos_upload]


def inicializar_estado():
    """Garante que a lista de eventos e o contador de interesses existam
    na sessão, populando com exemplos na primeira vez que o app carrega."""
    if "eventos" not in st.session_state:
        st.session_state.eventos = _eventos_exemplo()
    if "interesses" not in st.session_state:
        st.session_state.interesses = {ev["id"]: 0 for ev in st.session_state.eventos}
    if "proximo_id_evento" not in st.session_state:
        st.session_state.proximo_id_evento = len(st.session_state.eventos) + 1


def adicionar_evento(evento: dict):
    evento["id"] = st.session_state.proximo_id_evento
    st.session_state.eventos.append(evento)
    st.session_state.interesses[evento["id"]] = 0
    st.session_state.proximo_id_evento += 1


def registrar_interesse(evento_id: int):
    st.session_state.interesses[evento_id] = (
        st.session_state.interesses.get(evento_id, 0) + 1
    )


def _eventos_exemplo() -> list[dict]:
    """Eventos de exemplo, pré-carregados só pra o feed não abrir vazio."""
    hoje = date.today()
    return [
        {
            "id": 1,
            "nome_evento": "Forró Pé de Serra na Praça",
            "categoria": "Música",
            "produtor_nome": "Trio Cariri Forrozeiro",
            "produtor_tipo": "Banda",
            "contato": "(88) 99999-0001",
            "municipio": "Juazeiro do Norte",
            "local_nome": "Praça Padre Cícero",
            "data_evento": hoje,
            "horario": "19h",
            "gratuito": True,
            "acessivel": True,
            "transporte_publico": True,
            "descricao": (
                "Roda de forró tradicional com trio pé de serra, celebrando "
                "a cultura junina do Cariri cearense."
            ),
            "imagens_b64": [],
        },
        {
            "id": 2,
            "nome_evento": "Feira do Artesanato de Barro",
            "categoria": "Artesanato",
            "produtor_nome": "Coletivo Alto do Moura",
            "produtor_tipo": "Coletivo cultural",
            "contato": "(88) 99999-0002",
            "municipio": "Caucaia",
            "local_nome": "Centro Cultural",
            "data_evento": hoje + timedelta(days=1),
            "horario": "9h às 17h",
            "gratuito": True,
            "acessivel": False,
            "transporte_publico": True,
            "descricao": (
                "Exposição e venda de peças de cerâmica feitas por artesãos "
                "locais, com técnicas passadas entre gerações."
            ),
            "imagens_b64": [],
        },
        {
            "id": 3,
            "nome_evento": "Sarau Literário Vozes do Sertão",
            "categoria": "Teatro",
            "produtor_nome": "Ana Beatriz Lima",
            "produtor_tipo": "Artista individual",
            "contato": "(85) 99999-0003",
            "municipio": "Sobral",
            "local_nome": "Biblioteca Municipal",
            "data_evento": hoje + timedelta(days=3),
            "horario": "18h30",
            "gratuito": True,
            "acessivel": True,
            "transporte_publico": False,
            "descricao": (
                "Noite de poesia e contação de histórias com autores "
                "locais, aberta para quem quiser declamar."
            ),
            "imagens_b64": [],
        },
        {
            "id": 4,
            "nome_evento": "Exposição Raízes do Cariri",
            "categoria": "Exposição",
            "produtor_nome": "Museu Vivo do Cariri",
            "produtor_tipo": "Produtora/organização",
            "contato": "(88) 99999-0004",
            "municipio": "Crato",
            "local_nome": "Museu Municipal",
            "data_evento": hoje + timedelta(days=7),
            "horario": "8h às 16h",
            "gratuito": False,
            "acessivel": True,
            "transporte_publico": True,
            "descricao": (
                "Fotografias e objetos históricos contando a formação "
                "cultural do Cariri ao longo de 3 séculos."
            ),
            "imagens_b64": [],
        },
        {
            "id": 5,
            "nome_evento": "Festival de Quadrilhas Junina",
            "categoria": "Dança",
            "produtor_nome": "Quadrilha Estrela do Sertão",
            "produtor_tipo": "Grupo de teatro/dança",
            "contato": "(88) 99999-0005",
            "municipio": "Iguatu",
            "local_nome": "Praça da Matriz",
            "data_evento": hoje + timedelta(days=10),
            "horario": "20h",
            "gratuito": True,
            "acessivel": True,
            "transporte_publico": True,
            "descricao": (
                "Disputa entre quadrilhas juninas da região, com comidas "
                "típicas e barracas de artesanato local."
            ),
            "imagens_b64": [],
        },
        {
            "id": 6,
            "nome_evento": "Feira de Trocas e Saberes",
            "categoria": "Feira",
            "produtor_nome": "Rede Sertão Criativo",
            "produtor_tipo": "Coletivo cultural",
            "contato": "(88) 99999-0006",
            "municipio": "Canindé",
            "local_nome": "Terminal de Romeiros",
            "data_evento": hoje + timedelta(days=20),
            "horario": "9h às 15h",
            "gratuito": True,
            "acessivel": False,
            "transporte_publico": True,
            "descricao": (
                "Troca de mudas, sementes e artesanato entre produtores "
                "da região do sertão central."
            ),
            "imagens_b64": [],
        },
    ]