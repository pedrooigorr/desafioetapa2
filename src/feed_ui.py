"""
Interface visual da Feature 2 — Feed Cultural: cards estilo "stories",
linha do tempo horizontal e formulário de cadastro de evento/produtor.

Mantido separado de src/charts.py de propósito: aqui é tudo HTML/CSS
customizado (cartão de evento), não gráficos Plotly.
"""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from src.eventos import (
    CATEGORIAS,
    TIPOS_PRODUTOR,
    adicionar_evento,
    badge_temporal,
    calcular_distancia,
    imagens_para_base64,
    registrar_interesse,
)

CSS_FEED = """
<style>
.evento-card {
    border-radius: 18px;
    overflow: hidden;
    background: #FFFDF8;
    box-shadow: 0 4px 14px rgba(60, 30, 10, 0.15);
    margin-bottom: 22px;
    border: 1px solid #F0DDBE;
}
.evento-card-topo {
    height: 130px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 52px;
    color: #FFFDF8;
    background-size: cover;
    background-position: center;
}
.evento-carrossel {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    height: 100%;
    width: 100%;
    scrollbar-width: thin;
}
.evento-carrossel img {
    flex: 0 0 100%;
    scroll-snap-align: start;
    height: 100%;
    width: 100%;
    object-fit: cover;
}
.evento-carrossel-contador {
    position: absolute;
    top: 8px;
    right: 12px;
    background: rgba(26, 15, 8, 0.6);
    color: #FFFDF8;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 999px;
}
.evento-carrossel-wrap { position: relative; height: 100%; width: 100%; }
.evento-card-corpo {
    padding: 14px 16px 16px 16px;
    display: flex;
    flex-direction: column;
    min-height: 268px;
}
.evento-card-titulo {
    font-size: 17px;
    font-weight: 800;
    color: #1A0F08;
    margin: 0 0 4px 0;
    line-height: 1.25;
    min-height: 43px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.evento-card-info {
    font-size: 13.5px;
    color: #4A342A;
    margin: 1px 0;
    font-weight: 600;
}
.evento-card-desc {
    font-size: 13px;
    color: #5A4438;
    margin-top: 8px;
    line-height: 1.4;
    flex-grow: 1;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.badge-row {
    margin: 8px 0 4px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    min-height: 26px;
}
.badge-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 700;
    color: #FFFDF8;
}
.badge-pill-outline {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 700;
    border: 1.5px solid #C1440E;
    color: #C1440E;
    background: #FFFDF8;
}
.timeline-scroll {
    display: flex;
    overflow-x: auto;
    gap: 10px;
    padding: 6px 2px 14px 2px;
}
.timeline-dia {
    flex: 0 0 auto;
    width: 62px;
    border-radius: 14px;
    text-align: center;
    padding: 8px 4px;
    background: #FBEBD4;
    border: 2px solid transparent;
}
.timeline-dia.hoje {
    background: #C1440E;
    color: #FFFDF8;
    border-color: #7A2E0E;
}
.timeline-dia-numero { font-size: 18px; font-weight: 800; }
.timeline-dia-semana { font-size: 10.5px; font-weight: 700; opacity: 0.8; }
.timeline-dia-pontos { margin-top: 4px; font-size: 13px; }
</style>
"""


def _formatar_data_pt(d: date) -> str:
    dias_semana = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    return f"{d.day:02d}/{d.month:02d} ({dias_semana[d.weekday()]})"


def renderizar_timeline(eventos: list[dict], dias_a_frente: int = 21):
    """Trilha horizontal com um 'chip' por dia — pontos coloridos por
    categoria nos dias que têm evento, no lugar de um gráfico de barras."""
    hoje = date.today()
    eventos_por_dia: dict[date, list[dict]] = {}
    for ev in eventos:
        eventos_por_dia.setdefault(ev["data_evento"], []).append(ev)

    dias_semana = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    chips = []
    for i in range(dias_a_frente):
        d = hoje + timedelta(days=i)
        eh_hoje = d == hoje
        pontos = "".join(
            f'<span style="color:{CATEGORIAS.get(ev["categoria"], {}).get("cor", "#6B4226")}">●</span>'
            for ev in eventos_por_dia.get(d, [])[:4]
        )
        classe = "timeline-dia hoje" if eh_hoje else "timeline-dia"
        chips.append(
            f'<div class="{classe}">'
            f'<div class="timeline-dia-numero">{d.day}</div>'
            f'<div class="timeline-dia-semana">{dias_semana[d.weekday()]}</div>'
            f'<div class="timeline-dia-pontos">{pontos or "&nbsp;"}</div>'
            f"</div>"
        )
    st.markdown(
        f'<div class="timeline-scroll">{"".join(chips)}</div>', unsafe_allow_html=True
    )


def _montar_badges(evento: dict) -> list[str]:
    cat = CATEGORIAS.get(evento["categoria"], CATEGORIAS["Outro"])
    texto_badge, cor_badge = badge_temporal(evento["data_evento"])
    badges = [f'<span class="badge-pill" style="background:{cor_badge};">{texto_badge}</span>']
    badges.append(
        f'<span class="badge-pill" style="background:{cat["cor"]};">{cat["icone"]} {evento["categoria"]}</span>'
    )
    if evento.get("gratuito"):
        badges.append('<span class="badge-pill-outline">Gratuito</span>')
    if evento.get("acessivel"):
        badges.append('<span class="badge-pill-outline">♿ Acessível</span>')
    if evento.get("transporte_publico"):
        badges.append('<span class="badge-pill-outline">🚌 Transporte perto</span>')
    return badges


def _html_topo(evento: dict, altura_px: int, tamanho_fonte: int = 52, arredondado: bool = False) -> str:
    """HTML do topo do card/modal: carrossel com scroll (se houver fotos)
    ou ícone colorido da categoria (se não houver nenhuma)."""
    imagens = evento.get("imagens_b64") or []
    cat = CATEGORIAS.get(evento["categoria"], CATEGORIAS["Outro"])
    raio = "border-radius:16px;" if arredondado else ""

    if imagens:
        imgs_html = "".join(
            f'<img src="data:image/png;base64,{img}" alt="Foto do evento">'
            for img in imagens
        )
        contador = (
            f'<div class="evento-carrossel-contador">📷 {len(imagens)} fotos</div>'
            if len(imagens) > 1
            else ""
        )
        return (
            f'<div class="evento-carrossel-wrap" style="height:{altura_px}px; {raio} overflow:hidden;">'
            f'<div class="evento-carrossel">{imgs_html}</div>'
            f"{contador}"
            f"</div>"
        )

    return (
        f'<div style="height:{altura_px}px; display:flex; align-items:center; '
        f"justify-content:center; font-size:{tamanho_fonte}px; color:#FFFDF8; "
        f'background-color:{cat["cor"]}; {raio}">{cat["icone"]}</div>'
    )


def _distancia_texto(evento: dict, df_municipios, municipio_usuario: str | None) -> str:
    if not municipio_usuario:
        return ""
    dist = calcular_distancia(df_municipios, municipio_usuario, evento["municipio"])
    if dist is None:
        return ""
    return "📍 no seu município" if dist == 0 else f"📍 a {dist:g} km de você"


def renderizar_card(evento: dict, df_municipios, municipio_usuario: str | None):
    html_topo = _html_topo(evento, altura_px=130)
    badges = _montar_badges(evento)
    distancia_txt = _distancia_texto(evento, df_municipios, municipio_usuario)
    html_distancia = (
        f'<p class="evento-card-info">{distancia_txt}</p>' if distancia_txt else ""
    )

    partes_html = [
        '<div class="evento-card">',
        html_topo,
        '<div class="evento-card-corpo">',
        f'<p class="evento-card-titulo">{evento["nome_evento"]}</p>',
        f'<p class="evento-card-info">📅 {_formatar_data_pt(evento["data_evento"])} · {evento.get("horario", "")}</p>',
        f'<p class="evento-card-info">📌 {evento["local_nome"]}, {evento["municipio"]}</p>',
        html_distancia,
        f'<div class="badge-row">{"".join(badges)}</div>',
        f'<p class="evento-card-desc">{evento["descricao"]}</p>',
        f'<p class="evento-card-info" style="margin-top:8px; opacity:0.75;">🎤 {evento["produtor_nome"]} · {evento["produtor_tipo"]}</p>',
        "</div>",
        "</div>",
    ]
    st.markdown("".join(partes_html), unsafe_allow_html=True)

    col_detalhe, col_interesse = st.columns(2)
    with col_detalhe:
        if st.button("🔍 Ver detalhes", key=f"detalhe_{evento['id']}", use_container_width=True):
            _abrir_dialogo_detalhe(evento, df_municipios, municipio_usuario)
    with col_interesse:
        n = st.session_state.interesses.get(evento["id"], 0)
        if st.button(f"🙋 Tenho interesse ({n})", key=f"interesse_{evento['id']}", use_container_width=True):
            registrar_interesse(evento["id"])
            st.rerun()


@st.dialog("Detalhes do evento", width="large")
def _abrir_dialogo_detalhe(evento: dict, df_municipios, municipio_usuario: str | None):
    html_topo = _html_topo(evento, altura_px=260, tamanho_fonte=90, arredondado=True)
    badges = _montar_badges(evento)
    distancia_txt = _distancia_texto(evento, df_municipios, municipio_usuario)

    st.markdown(
        f'<div style="margin-bottom:14px;">{html_topo}</div>', unsafe_allow_html=True
    )

    st.markdown(f"## {evento['nome_evento']}")
    st.markdown(f'<div class="badge-row">{"".join(badges)}</div>', unsafe_allow_html=True)

    st.markdown(
        f"📅 **{_formatar_data_pt(evento['data_evento'])}** · {evento.get('horario', '')}  \n"
        f"📌 **{evento['local_nome']}**, {evento['municipio']}"
        + (f"  \n{distancia_txt}" if distancia_txt else "")
    )

    st.divider()
    st.markdown("**Sobre o evento**")
    st.write(evento["descricao"])

    st.divider()
    st.markdown("**Quem está organizando**")
    st.write(f"🎤 {evento['produtor_nome']} · {evento['produtor_tipo']}")
    st.write(f"💬 Contato: {evento['contato']}")

    st.divider()
    n = st.session_state.interesses.get(evento["id"], 0)
    if st.button(f"🙋 Tenho interesse ({n})", key=f"interesse_dialogo_{evento['id']}", use_container_width=True):
        registrar_interesse(evento["id"])
        st.rerun()




def renderizar_formulario_cadastro(df_municipios):
    st.subheader("🎨 Divulgue seu evento")
    st.caption(
        "Preencha os dados do evento e de quem está organizando. Ele "
        "aparece na hora no Feed Cultural, pra galera descobrir."
    )

    with st.form("form_cadastro_evento", clear_on_submit=True):
        st.markdown("**Sobre o evento**")
        c1, c2 = st.columns(2)
        nome_evento = c1.text_input("Nome do evento *")
        categoria = c2.selectbox("Categoria *", list(CATEGORIAS.keys()))

        c3, c4 = st.columns(2)
        municipio = c3.selectbox(
            "Município *", sorted(df_municipios["municipio"].unique())
        )
        local_nome = c4.text_input("Local (praça, centro cultural...) *")

        c5, c6 = st.columns(2)
        data_evento = c5.date_input("Data *", min_value=date.today(), value=date.today())
        horario = c6.text_input("Horário (ex: 19h, 9h às 17h)")

        descricao = st.text_area(
            "Descrição curta *", max_chars=220,
            placeholder="Em 2-3 frases, conte do que se trata o evento.",
        )
        imagens = st.file_uploader(
            "Fotos do evento (opcional, pode escolher várias)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Se enviar mais de uma foto, elas aparecem como um carrossel no card",
        )

        st.markdown("**Selos** (ajudam quem tem restrição de custo ou mobilidade)")
        c7, c8, c9 = st.columns(3)
        gratuito = c7.checkbox("Gratuito")
        acessivel = c8.checkbox("Acessível (cadeirante)")
        transporte_publico = c9.checkbox("Transporte público por perto")

        st.markdown("**Sobre você / seu grupo**")
        c10, c11 = st.columns(2)
        produtor_nome = c10.text_input("Nome do artista, grupo ou produtora *")
        produtor_tipo = c11.selectbox("Tipo *", TIPOS_PRODUTOR)
        contato = st.text_input("Contato (WhatsApp, Instagram...) *")

        enviado = st.form_submit_button("📣 Publicar evento", use_container_width=True)

        if enviado:
            obrigatorios = [
                nome_evento, municipio, local_nome, descricao,
                produtor_nome, contato,
            ]
            if not all(obrigatorios):
                st.error("Preenche os campos marcados com * antes de publicar.")
            else:
                adicionar_evento(
                    {
                        "nome_evento": nome_evento,
                        "categoria": categoria,
                        "produtor_nome": produtor_nome,
                        "produtor_tipo": produtor_tipo,
                        "contato": contato,
                        "municipio": municipio,
                        "local_nome": local_nome,
                        "data_evento": data_evento,
                        "horario": horario,
                        "gratuito": gratuito,
                        "acessivel": acessivel,
                        "transporte_publico": transporte_publico,
                        "descricao": descricao,
                        "imagens_b64": imagens_para_base64(imagens),
                    }
                )
                st.success(
                    f"✅ '{nome_evento}' publicado! Já aparece no Feed Cultural."
                )