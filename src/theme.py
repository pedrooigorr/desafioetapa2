"""
Paleta de cores "Nordeste" do Radar Cultural — terracota (barro), amarelo-sol,
azul-azulejo e verde-cactos — usada nos gráficos Plotly, no destaque das
tabelas e no CSS customizado da interface.
"""

# Paleta qualitativa (uma cor por mesorregião nos gráficos de dispersão/legenda)
NORDESTE_DISCRETA = [
    "#C1440E",  # terracota / barro
    "#F2A93B",  # amarelo-sol
    "#1B7A8C",  # azul-azulejo
    "#4C6444",  # verde-cactos
    "#8C1C13",  # vermelho-tijolo
    "#D9A441",  # dourado-areia
    "#6B4226",  # marrom-couro
]

# Escala contínua (barras/gradientes: dourado → terracota → tijolo escuro)
NORDESTE_SEQUENCIAL = ["#F5C466", "#F2A93B", "#C1440E", "#7A2E0E"]

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


# ----------------------------------------------------------------------
# CSS customizado da interface: cards com borda/sombra terracota e
# métricas (st.metric) com texto maior e mais escuro.
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
</style>
"""