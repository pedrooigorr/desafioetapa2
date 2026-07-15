"""
Paleta de cores "Nordeste" do Radar Cultural — terracota (barro), amarelo-sol,
azul-azulejo e verde-cactos — usada nos gráficos Plotly e no destaque das
tabelas.
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

# Escala contínua (barras/gradientes: areia clara → terracota → tijolo escuro)
NORDESTE_SEQUENCIAL = ["#FBEBD4", "#F2A93B", "#C1440E", "#7A2E0E"]

# Cores usadas para colorir a tabela de municípios prioritários
_TABELA_COR_MIN = (251, 235, 212)  # areia clara
_TABELA_COR_MAX = (193, 68, 14)  # terracota


def _interpolar_cor(valor: float, vmin: float, vmax: float) -> str:
    """Interpola entre areia clara e terracota conforme o valor (0 a 1)."""
    t = 0.0 if vmax == vmin else (valor - vmin) / (vmax - vmin)
    r, g, b = (
        int(_TABELA_COR_MIN[i] + t * (_TABELA_COR_MAX[i] - _TABELA_COR_MIN[i]))
        for i in range(3)
    )
    return f"background-color: rgb({r},{g},{b}); color: #3E2723; font-weight: 600"


def destacar_coluna(serie):
    """
    Função para usar com `DataFrame.style.apply(destacar_coluna, subset=[...])`
    — colore a coluna com gradiente terracota proporcional ao valor.
    """
    vmin, vmax = serie.min(), serie.max()
    return [_interpolar_cor(v, vmin, vmax) for v in serie]