"""
Acessibilidade — controles e utilitários compartilhados pelos 3 modos do
app: alto contraste, tamanho de texto, VLibras (Libras) e leitura em voz
alta (Web Speech API do navegador, sem custo e sem precisar de internet
extra).

O painel de controles fica sempre no topo da sidebar, em qualquer modo.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

TAMANHOS_TEXTO = {
    "Normal": 1.0,
    "Grande": 1.15,
    "Muito grande": 1.3,
}


def inicializar_preferencias():
    st.session_state.setdefault("a11y_alto_contraste", False)
    st.session_state.setdefault("a11y_tamanho_texto", "Normal")


def renderizar_controles_topo():
    """
    Painel de acessibilidade — igual em todos os modos, sempre no topo da
    página principal (não na sidebar). Ficar na sidebar exige clicar no
    botão de abrir/fechar a barra lateral, que depende de o navegador
    conseguir clicar nele — colocando aqui, o controle sempre aparece
    sem precisar abrir nada.
    """
    with st.expander("♿ Acessibilidade", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox(
                "Modo alto contraste",
                key="a11y_alto_contraste",
                help="Troca a paleta por uma versão em preto/branco/amarelo, "
                "com contraste bem mais forte",
            )
        with col2:
            st.select_slider(
                "Tamanho do texto",
                options=list(TAMANHOS_TEXTO.keys()),
                key="a11y_tamanho_texto",
            )
        st.caption(
            "O botão 🤟 no canto da tela abre o VLibras (tradutor de "
            "Libras do governo federal). Cada painel também tem um "
            "botão 🔊 pra ouvir o resumo em voz alta."
        )


CSS_ALTO_CONTRASTE = """
<style>
/* Modo alto contraste — sobrescreve a paleta terracota por preto/branco/
   amarelo puros, com bordas mais grossas, para contraste máximo */
[data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}
p, li, span, div, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}
.radar-header, .radar-footer {
    background: #000000 !important;
}
.radar-header-titulo, .radar-header-subtitulo,
.radar-footer-titulo, .radar-footer-texto {
    color: #FFFF00 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 3px solid #000000 !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important;
}
div[data-testid="stMetricValue"] {
    color: #000000 !important;
}
.stButton button {
    border: 2px solid #000000 !important;
    color: #000000 !important;
    background-color: #FFFFFF !important;
}
.stButton button[kind="primary"] {
    background-color: #000000 !important;
    color: #FFFF00 !important;
}
a { color: #0000EE !important; text-decoration: underline !important; }

/* Reforça contraste/saturação dos gráficos Plotly — não muda as cores
   de cada categoria (isso exigiria mudar o Python), só intensifica */
.js-plotly-plot {
    filter: contrast(1.35) saturate(1.3);
}
</style>
"""


def css_acessibilidade() -> str:
    """Monta o CSS a injetar com base nas preferências atuais da sessão."""
    partes = []

    zoom = TAMANHOS_TEXTO[st.session_state.get("a11y_tamanho_texto", "Normal")]
    if zoom != 1.0:
        partes.append(
            f'<style>[data-testid="stAppViewContainer"] {{ zoom: {zoom}; }}</style>'
        )

    if st.session_state.get("a11y_alto_contraste", False):
        partes.append(CSS_ALTO_CONTRASTE)

    return "".join(partes)


def widget_vlibras():
    """
    Injeta o widget oficial do governo federal (VLibras) — avatar 3D que
    traduz o texto da página pra Libras. O Streamlit isola componentes
    num iframe próprio, então o script precisa alcançar o documento PAI
    (window.parent) pra aparecer flutuando sobre a página inteira, e não
    só dentro da caixinha do componente. Roda só uma vez (checa se já
    foi injetado antes de adicionar de novo).
    """
    components.html(
        """
        <script>
        (function() {
            var doc = window.parent.document;
            if (doc.getElementById('vlibras-injetado')) { return; }

            var wrapper = doc.createElement('div');
            wrapper.setAttribute('vw', '');
            wrapper.className = 'enabled';
            wrapper.id = 'vlibras-injetado';
            wrapper.innerHTML =
                '<div vw-access-button class="active"></div>' +
                '<div vw-plugin-wrapper><div class="vw-plugin-top-wrapper">' +
                '</div></div>';
            doc.body.appendChild(wrapper);

            var script = doc.createElement('script');
            script.src = 'https://vlibras.gov.br/app/vlibras-plugin.js';
            script.onload = function() {
                new doc.defaultView.VLibras.Widget('https://vlibras.gov.br/app');
            };
            doc.body.appendChild(script);
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _escapar_para_js(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def botao_ouvir(texto: str, key: str, rotulo: str = "🔊 Ouvir este resumo"):
    """
    Botão que lê `texto` em voz alta com a Web Speech API do navegador —
    nativa, sem custo, sem precisar de internet extra nem API paga.
    Clicar de novo interrompe e recomeça a leitura.
    """
    texto_js = _escapar_para_js(texto)
    components.html(
        f"""
        <button id="btn-{key}" style="
            background:#C1440E; color:#FFFDF8; border:none;
            border-radius:8px; padding:8px 16px; font-weight:700;
            font-size:14px; cursor:pointer; font-family:sans-serif;
            width:100%;
        ">{rotulo}</button>
        <script>
        document.getElementById('btn-{key}').addEventListener('click', function() {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{texto_js}");
            msg.lang = 'pt-BR';
            window.speechSynthesis.speak(msg);
        }});
        </script>
        """,
        height=48,
    )