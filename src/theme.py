"""
Paleta de cores "Nordeste" do Radar Cultural — terracota (barro), amarelo-sol,
azul-azulejo e verde-cactos — usada nos gráficos Plotly, no destaque das
tabelas e no CSS customizado da interface.
"""

# Paleta qualitativa (uma cor por mesorregião nos gráficos de dispersão/legenda)
NORDESTE_DISCRETA = [
    "#C1440E",  # terracota / barro
    "#F2A93B",  # amareloj-sol
    "#1B7A8C",  # azul-azulejo
    "#4C6444",  # verde-cactos
    "#8C1C13",  # vermelho-tijolo
    "#D9A441",  # dourado-areia
    "#6B4226",  # marrom-couro
]

# Escala contínua (barras/gradientes: dourado → terracota → tijolo escuro)
NORDESTE_SEQUENCIAL = ["#F5C466", "#F2A93B", "#C1440E", "#7A2E0E"]

# ----------------------------------------------------------------------
# Cores "assinatura" de cada feature do app — usadas nos cards de
# apresentação (hero) da tela inicial e como acento visual (barra colorida)
# no topo de cada painel, pra cada seção ter identidade própria em vez de
# tudo ser terracota. Reaproveita tons já usados nos gráficos (NORDESTE_*)
# pra manter consistência com o resto da paleta.
# ----------------------------------------------------------------------
COR_GESTOR = "#1B7A8C"        # azul-azulejo
COR_GESTOR_CLARO = "#E3F0F2"
COR_DEMANDA = "#4C6444"       # verde-cactos
COR_DEMANDA_CLARO = "#EAF0E4"
COR_SIMULADOR = "#B8792A"     # dourado-areia (escurecido p/ contraste de texto)
COR_SIMULADOR_CLARO = "#FBF0DC"

def cabecalho_app() -> str:
    """
    Header do app: barra terracota cheia, contrastando com o fundo claro
    (#FFFDF8) — o oposto do resto da interface, que é predominantemente
    clara. Usar uma vez só, no topo do streamlit_app.py.
    """
    return (
        '<div class="radar-header">'
        '<span class="radar-header-icone">🎭</span>'
        "<div>"
        '<div class="radar-header-titulo">Cultura Ceará</div>'
        '<div class="radar-header-subtitulo">Squad ZeroKai · Desafio dos '
        "Dados VIVO 2026 · ODS 4, 10 e 11</div>"
        "</div>"
        "</div>"
    )


def rodape_app() -> str:
    """
    Footer do app: barra marrom bem escura (contraste diferente do header,
    pra não repetir a mesma cor duas vezes na página), com crédito do
    squad, fontes de dados e os ODS trabalhados. Usar uma vez só, no fim
    do streamlit_app.py — aparece em todos os 3 modos.
    """
    return (
        '<div class="radar-footer">'
        '<div class="radar-footer-col">'
        '<div class="radar-footer-titulo">🎭 Cultura Ceará</div>'
        '<div class="radar-footer-texto">Squad ZeroKai · Desafio dos Dados '
        "VIVO 2026 — protótipo de código aberto.</div>"
        "</div>"
        '<div class="radar-footer-col">'
        '<div class="radar-footer-titulo">Fontes dos dados</div>'
        '<div class="radar-footer-texto">IBGE — MUNIC, Suplemento de '
        "Cultura 2014<br>Atlas Brasil (PNUD/IPEA/FJP) — Censo 2010</div>"
        "</div>"
        '<div class="radar-footer-col">'
        '<div class="radar-footer-titulo">ODS trabalhados</div>'
        '<div class="radar-footer-texto">4 — Educação de qualidade<br>'
        "10 — Redução das desigualdades<br>"
        "11 — Cidades e comunidades sustentáveis</div>"
        "</div>"
        "</div>"
    )


# Cores usadas para colorir a tabela de municípios prioritários
_TABELA_COR_MIN = (251, 235, 212)  # areia clara
_TABELA_COR_MAX = (193, 68, 14)  # terracota

# Texto preto/marrom bem escuro e maior, para dar destaque às tabelas
_TEXTO_DESTAQUE = "color: #1A0F08; font-weight: 700; font-size: 15px;"

# Mesma cor usada para dar destaque ao texto dos gráficos Plotly (eixos,
# rótulos, valores das barras, legendas)
TEXTO_ESCURO = "#1A0F08"


def _interpolar_cor(valor: float, vmin: float, vmax: float) -> str:
    """Interpola entre areia clara e terracota conforme o valor (0 a 1)."""
    t = 0.0 if vmax == vmin else (valor - vmin) / (vmax - vmin)
    r, g, b = (
        int(_TABELA_COR_MIN[i] + t * (_TABELA_COR_MAX[i] - _TABELA_COR_MIN[i]))
        for i in range(3)
    )
    return f"background-color: rgb({r},{g},{b}); {_TEXTO_DESTAQUE}"


def destacar_coluna(serie):
    """
    Função para usar com `DataFrame.style.apply(destacar_coluna, subset=[...])`
    — colore a coluna com gradiente terracota proporcional ao valor, com
    texto preto e maior para dar destaque.
    """
    vmin, vmax = serie.min(), serie.max()
    return [_interpolar_cor(v, vmin, vmax) for v in serie]


def estilo_texto_tabela() -> dict:
    """
    Propriedades CSS para aplicar em `Styler.set_properties(**...)` nas
    demais colunas da tabela (fora do gradiente) — texto preto e maior,
    igual ao das colunas destacadas.
    """
    return {"color": "#1A0F08", "font-weight": "600", "font-size": "15px"}


def aplicar_texto_escuro(fig, tamanho_fonte: int = 13):
    """
    Deixa o texto de um gráfico Plotly (eixos, rótulos, legendas, valores
    das barras) preto/marrom escuro e em negrito, para dar mais destaque —
    usada em todos os gráficos do app para manter a mesma identidade visual.
    """
    fig.update_layout(
        font=dict(color=TEXTO_ESCURO, size=tamanho_fonte),
        xaxis=dict(
            title_font=dict(color=TEXTO_ESCURO, size=tamanho_fonte + 1),
            tickfont=dict(color=TEXTO_ESCURO, size=tamanho_fonte),
        ),
        yaxis=dict(
            title_font=dict(color=TEXTO_ESCURO, size=tamanho_fonte + 1),
            tickfont=dict(color=TEXTO_ESCURO, size=tamanho_fonte),
        ),
        legend=dict(font=dict(color=TEXTO_ESCURO, size=tamanho_fonte)),
    )
    return fig


def cartao_hero(icone: str, titulo: str, texto: str, cor: str, cor_clara: str) -> str:
    """
    Monta o HTML de um card de apresentação (hero) pra tela inicial —
    ícone grande, título e um parágrafo curto explicando a feature, com
    cor própria por seção. Usar com st.markdown(..., unsafe_allow_html=True),
    seguido do st.button real que leva até a feature.
    """
    return (
        f'<div class="radar-hero-card" '
        f'style="border-top-color:{cor}; background:{cor_clara};">'
        f'<div class="radar-hero-icone">{icone}</div>'
        f'<div class="radar-hero-titulo" style="color:{cor};">{titulo}</div>'
        f'<div class="radar-hero-texto">{texto}</div>'
        f"</div>"
    )


def barra_secao(cor: str) -> str:
    """
    Pequena tarja colorida usada no topo de um painel/gráfico pra dar
    identidade visual própria à seção (em vez de tudo ficar na mesma cor).
    Usar com st.markdown(..., unsafe_allow_html=True) logo antes do título.
    """
    return f'<div class="radar-barra-secao" style="background:{cor};"></div>'


# ----------------------------------------------------------------------
# CSS customizado da interface: cards com borda/sombra terracota,
# métricas (st.metric) com texto maior e mais escuro, e os elementos
# novos do hero (cards de apresentação + tarjas de seção coloridas).
# ----------------------------------------------------------------------
CSS_CUSTOMIZADO = """
<style>
/* Cards com borda (st.container(border=True)) — destaque terracota */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 2px solid #C1440E !important;
    border-radius: 14px !important;
    background-color: #FFFDF8 !important;
    box-shadow: 0 3px 10px rgba(193, 68, 14, 0.18);
    padding: 4px;
}

/* Cards de apresentação (hero) das 3 features na tela inicial */
.radar-hero-card {
    border-top: 6px solid;
    border-radius: 14px;
    padding: 22px 20px 18px 20px;
    min-height: 190px;
    box-shadow: 0 3px 10px rgba(26, 15, 8, 0.10);
    margin-bottom: 10px;
}
.radar-hero-icone {
    font-size: 2.1rem;
    margin-bottom: 6px;
}
.radar-hero-titulo {
    font-size: 1.15rem;
    font-weight: 800;
    margin-bottom: 8px;
}
.radar-hero-texto {
    font-size: 0.95rem;
    color: #3E2723;
    line-height: 1.45;
}

/* Tarja colorida no topo de cada painel/gráfico — dá identidade por seção */
.radar-barra-secao {
    height: 5px;
    width: 56px;
    border-radius: 4px;
    margin-bottom: 10px;
}

/* Títulos dentro dos cards */
div[data-testid="stVerticalBlockBorderWrapper"] h3 {
    color: #C1440E !important;
}

/* Métricas (KPIs) maiores e mais escuras */
div[data-testid="stMetricValue"] {
    font-size: 2.1rem !important;
    color: #1A0F08 !important;
    font-weight: 800 !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.95rem !important;
    color: #6B4226 !important;
    font-weight: 700 !important;
}

/* Botões da navbar */
.stButton button {
    font-weight: 700 !important;
}

/* Header — barra terracota cheia, contrasta com o fundo claro do app */
.radar-header {
    background: #C1440E;
    border-radius: 16px;
    padding: 22px 28px;
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 4px;
    box-shadow: 0 4px 14px rgba(122, 46, 14, 0.28);
}
.radar-header-icone {
    font-size: 2.6rem;
    line-height: 1;
}
.radar-header-titulo {
    color: #FFFDF8;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.15;
}
.radar-header-subtitulo {
    color: #FBEBD4;
    font-size: 0.95rem;
    font-weight: 700;
    margin-top: 2px;
}

/* Footer — marrom bem escuro, contraste diferente do header de propósito */
.radar-footer {
    background: #2C1B12;
    border-radius: 16px;
    padding: 26px 30px;
    margin-top: 40px;
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: space-between;
}
.radar-footer-col {
    flex: 1;
    min-width: 200px;
}
.radar-footer-titulo {
    color: #F2A93B;
    font-weight: 800;
    font-size: 0.95rem;
    margin-bottom: 6px;
}
.radar-footer-texto {
    color: #E8DFD5;
    font-size: 0.85rem;
    line-height: 1.6;
}
</style>
"""