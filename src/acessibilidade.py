"""
Acessibilidade — controles e utilitários compartilhados pelos 3 modos do
app: alto contraste, tamanho de texto e leitura em voz alta (Web Speech
API do navegador, sem custo e sem precisar de internet extra).

O painel de controles fica sempre no topo da página principal, em
qualquer modo.
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
    with st.expander("Acessibilidade", expanded=False):
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
            "Cada painel também tem um botão pra ouvir o resumo em voz alta."
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
/* A regra genérica "p, span, div {color: #000000}" acima também pega o
   texto por dentro dos botões (o Streamlit envolve o texto do botão em
   <div>/<p> aninhados) e "vencia" a cor pretendida do botão. Isso força
   o texto interno do botão a sempre herdar a cor do próprio botão. */
.stButton button p,
.stButton button div,
.stButton button span {
    color: inherit !important;
}
a { color: #0000EE !important; text-decoration: underline !important; }

/* Barra de ferramentas do Streamlit (Share, estrela, lápis, GitHub, ⋮) —
   também vira preta no alto contraste, pra combinar com o resto da
   página em vez de continuar na cor terracota do tema normal */
header[data-testid="stHeader"] {
    background: #000000 !important;
}

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

    escala = TAMANHOS_TEXTO[st.session_state.get("a11y_tamanho_texto", "Normal")]
    if escala != 1.0:
        # font-size na raiz, não "zoom": a maioria dos textos do Streamlit
        # (e os nossos, em src/theme.py) usa unidades relativas (rem), que
        # escalam com isso — cresce só a tipografia, sem inflar junto
        # imagens, ícones e espaçamentos como o "zoom" fazia.
        partes.append(
            f"<style>html {{ font-size: {escala * 100:.0f}% !important; }}</style>"
        )

    if st.session_state.get("a11y_alto_contraste", False):
        partes.append(CSS_ALTO_CONTRASTE)

    return "".join(partes)


def _escapar_para_js(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def botao_ouvir(texto: str, key: str, rotulo: str = "Ouvir este resumo"):
    """
    Botão que lê `texto` em voz alta com a Web Speech API do navegador —
    nativa, sem custo, sem precisar de internet extra nem API paga.
    Clicar de novo interrompe e recomeça a leitura.
    """
    texto_js = _escapar_para_js(texto)
    components.html(
        f"""
        <style>
        /* Sem isso, o <body> padrão do iframe do componente tem uma margem
           própria (tipicamente 8px) que empurra o botão pra baixo e o
           desalinha verticalmente da caixa de resumo ao lado — zerando a
           margem, o botão ocupa a altura inteira do iframe (height=44 no
           components.html abaixo) e fica centralizado de verdade. */
        html, body {{
            margin: 0;
            padding: 0;
            height: 100%;
        }}
        .btn-ouvir-{key} {{
            background:#FFFDF8;
            color:#C1440E;
            border:2px solid #C1440E;
            border-radius:8px;
            padding:6px 16px;
            font-weight:700;
            font-size:14px;
            cursor:pointer;
            font-family:sans-serif;
            width:100%;
            height:100%;
            box-sizing:border-box;
            transition: background-color 0.15s ease, color 0.15s ease;
        }}
        .btn-ouvir-{key}:hover {{
            background:#C1440E;
            color:#FFFDF8;
        }}
        </style>
        <button id="btn-{key}" class="btn-ouvir-{key}">{rotulo}</button>
        <script>
        document.getElementById('btn-{key}').addEventListener('click', function() {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{texto_js}");
            msg.lang = 'pt-BR';
            window.speechSynthesis.speak(msg);
        }});
        </script>
        """,
        height=44,
    )