"""
Paleta de cores "Nordeste" do Radar Cultural — terracota (barro), amarelo-sol,
azul-azulejo e verde-cactos — usada nos gráficos Plotly, no destaque das
tabelas e no CSS customizado da interface.

Também concentra os componentes visuais reaproveitados pelo app: header,
footer, cards de apresentação (hero), cards de KPI, chips de status e as
tarjas coloridas que dão identidade a cada seção.

Suporte a daltonismo: as cores que DIFERENCIAM categorias na tela ao mesmo
tempo (as 3 cores das features, o par "Tem/Deserto Cultural" do mapa do
Simulador, e as paletas dos gráficos) trocam de conjunto conforme o modo
escolhido em Acessibilidade — ver `_PALETAS_DALTONISMO` e `paleta_ativa()`
logo abaixo. Cores usadas sozinhas (o terracota do header, botões, links)
não mudam: não há ambiguidade a resolver quando só existe uma cor na tela.
"""

import streamlit as st

from src.icones import icone

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

# Perfil e Metodologia são páginas "de apoio" — não pertencem a nenhuma
# das 3 lentes do projeto, então usam uma cor neutra própria em vez de
# emprestar a cor de um dos 3 modos (evita sugerir que uma delas "é dona"
# dessas páginas transversais)
COR_NEUTRA = "#6B4226"        # marrom-couro
COR_NEUTRA_CLARO = "#EFE6DC"

# ----------------------------------------------------------------------
# Modos de daltonismo — cada um substitui só as cores que competem entre
# si na mesma tela (as 3 cores de feature, o par "Tem"/"Deserto Cultural"
# do Simulador, e as paletas dos gráficos). "Anopia" (ausência total) e
# "anomalia" (percepção reduzida) do mesmo eixo de cor são tratadas pelo
# mesmo conjunto de cores — a correção que ajuda quem não distingue duas
# cores de jeito nenhum também ajuda quem só as distingue com dificuldade.
#
#   - Protanopia/Protanomalia  → eixo do vermelho (cone L) comprometido
#   - Deuteranopia/Deuteranomalia → eixo do verde (cone M) comprometido
#   - Tritanopia/Tritanomalia  → eixo do azul/amarelo (cone S) comprometido
#
# "protan" e "deutan" partem da paleta Okabe–Ito (Color Universal Design),
# uma das poucas paletas qualitativas com segurança documentada para os
# dois tipos de daltonismo vermelho-verde ao mesmo tempo. "tritan" evita
# pares azul/verde e amarelo/violeta (os que se confundem nesse eixo) e
# usa a distinção vermelho-verde, que segue intacta na tritanopia.
# ----------------------------------------------------------------------
_PALETAS_DALTONISMO = {
    "padrao": {
        "gestor": "#1B7A8C", "gestor_claro": "#E3F0F2",
        "demanda": "#4C6444", "demanda_claro": "#EAF0E4",
        "simulador": "#B8792A", "simulador_claro": "#FBF0DC",
        "deserto": "#C1440E", "deserto_claro": "#FBEBD4",
        "tem": "#1B7A8C", "nao_tem": "#C1440E",
        "discreta": [
            "#C1440E", "#F2A93B", "#1B7A8C", "#4C6444",
            "#8C1C13", "#D9A441", "#6B4226",
        ],
        "sequencial": ["#F5C466", "#F2A93B", "#C1440E", "#7A2E0E"],
    },
    "protan": {
        "gestor": "#0072B2", "gestor_claro": "#DCEBF5",
        "demanda": "#009E73", "demanda_claro": "#DAF0E9",
        "simulador": "#E69F00", "simulador_claro": "#FBEBD1",
        "deserto": "#D55E00", "deserto_claro": "#FBE0D1",
        "tem": "#0072B2", "nao_tem": "#D55E00",
        "discreta": [
            "#E69F00", "#56B4E9", "#009E73", "#F0E442",
            "#0072B2", "#D55E00", "#CC79A7",
        ],
        "sequencial": ["#DCEBF5", "#9CC6E5", "#3E86C4", "#0B3D63"],
    },
    "deutan": {
        "gestor": "#0072B2", "gestor_claro": "#DCEBF5",
        "demanda": "#CC79A7", "demanda_claro": "#F3E1EC",
        "simulador": "#E69F00", "simulador_claro": "#FBEBD1",
        "deserto": "#D55E00", "deserto_claro": "#FBE0D1",
        "tem": "#0072B2", "nao_tem": "#D55E00",
        "discreta": [
            "#0072B2", "#E69F00", "#56B4E9", "#CC79A7",
            "#D55E00", "#F0E442", "#009E73",
        ],
        "sequencial": ["#DFF3F0", "#8FD0C5", "#2C9C87", "#0B4F43"],
    },
    "tritan": {
        "gestor": "#2E7D32", "gestor_claro": "#E3F0E3",
        "demanda": "#C62828", "demanda_claro": "#FBE3E3",
        "simulador": "#EF6C00", "simulador_claro": "#FDEBD8",
        "deserto": "#8B3A3A", "deserto_claro": "#F0DCDC",
        "tem": "#2E7D32", "nao_tem": "#8B3A3A",
        "discreta": [
            "#D7263D", "#2E7D32", "#F46036", "#6D4C41",
            "#AD1457", "#7C7C3A", "#4E342E",
        ],
        "sequencial": ["#E8F5E9", "#A5D6A7", "#43A047", "#1B5E20"],
    },
}

# Rótulos exibidos no seletor do painel de Acessibilidade
MODOS_DALTONISMO = {
    "padrao": "Padrão",
    "protan": "Protanopia / Protanomalia",
    "deutan": "Deuteranopia / Deuteranomalia",
    "tritan": "Tritanopia / Tritanomalia",
}


def paleta_ativa() -> dict:
    """
    Devolve o conjunto de cores em uso agora, conforme o modo escolhido
    em Acessibilidade (`st.session_state["a11y_daltonismo"]`). Chamada a
    cada rerun do Streamlit, então reflete a escolha mais recente sem
    precisar recarregar a página.
    """
    modo = st.session_state.get("a11y_daltonismo", "padrao")
    return _PALETAS_DALTONISMO.get(modo, _PALETAS_DALTONISMO["padrao"])


def cabecalho_app() -> str:
    """
    Header do app: barra terracota cheia, contrastando com o fundo claro
    (#FFFDF8) — o oposto do resto da interface, que é predominantemente
    clara. Usar uma vez só, no topo do streamlit_app.py.
    """
    return (
        '<div class="radar-header">'
        "<div>"
        '<div class="radar-header-titulo">Radar Cultural</div>'
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
        '<div class="radar-footer-titulo">Radar Cultural</div>'
        '<div class="radar-footer-texto">Squad ZeroKai · Desafio dos Dados '
        "VIVO 2026 — protótipo de código aberto.</div>"
        "</div>"
        '<div class="radar-footer-col">'
        '<div class="radar-footer-titulo">Fontes dos dados</div>'
        '<div class="radar-footer-texto">IBGE — MUNIC, Suplemento de '
        "Cultura 2021<br>IBGE — Censo Demográfico 2022</div>"
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
_TABELA_COR_MIN = (251, 235, 212)  # areia clara — não muda por modo, é só o "vazio"

# Texto preto/marrom bem escuro e maior, para dar destaque às tabelas
_TEXTO_DESTAQUE = "color: #1A0F08; font-weight: 700; font-size: 15px;"

# Mesma cor usada para dar destaque ao texto dos gráficos Plotly (eixos,
# rótulos, valores das barras, legendas)
TEXTO_ESCURO = "#1A0F08"


def _hex_para_rgb(hexadecimal: str) -> tuple[int, int, int]:
    h = hexadecimal.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _escurecer(hexadecimal: str, fator: float = 0.62) -> str:
    """Escurece uma cor hex multiplicando cada canal pelo fator (0 a 1)."""
    r, g, b = _hex_para_rgb(hexadecimal)
    return f"#{int(r * fator):02X}{int(g * fator):02X}{int(b * fator):02X}"


def _interpolar_cor(valor: float, vmin: float, vmax: float) -> str:
    """
    Interpola entre areia clara e a cor de "Deserto Cultural" do modo de
    cores ativo, conforme o valor (0 a 1). O sinal principal do gradiente
    é a luminosidade (claro → escuro), que se mantém legível em qualquer
    tipo de daltonismo — a matiz só reforça, nunca é a única pista.
    """
    cor_max = _hex_para_rgb(paleta_ativa()["deserto"])
    t = 0.0 if vmax == vmin else (valor - vmin) / (vmax - vmin)
    r, g, b = (
        int(_TABELA_COR_MIN[i] + t * (cor_max[i] - _TABELA_COR_MIN[i]))
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
        font={"color": TEXTO_ESCURO, "size": tamanho_fonte, "family": "Inter, sans-serif"},
        xaxis={
            "title_font": {"color": TEXTO_ESCURO, "size": tamanho_fonte + 1},
            "tickfont": {"color": TEXTO_ESCURO, "size": tamanho_fonte},
        },
        yaxis={
            "title_font": {"color": TEXTO_ESCURO, "size": tamanho_fonte + 1},
            "tickfont": {"color": TEXTO_ESCURO, "size": tamanho_fonte},
        },
        legend={"font": {"color": TEXTO_ESCURO, "size": tamanho_fonte}},
    )
    return fig


def cartao_hero(icone_nome: str, titulo: str, texto: str, cor: str, cor_clara: str) -> str:
    """
    Monta o HTML de um card de apresentação (hero) pra tela inicial —
    ícone (Lucide), título e um parágrafo curto explicando a feature, com
    cor própria por seção. Usar com st.markdown(..., unsafe_allow_html=True),
    seguido do st.button real que leva até a feature.
    """
    return (
        f'<div class="radar-hero-card" '
        f'style="border-top-color:{cor}; background:{cor_clara};">'
        f'<div class="radar-hero-icone" style="background:{cor};">'
        f'{icone(icone_nome, cor="#FFFDF8", tamanho=20)}</div>'
        f'<div class="radar-hero-titulo" style="color:{cor};">{titulo}</div>'
        f'<div class="radar-hero-texto">{texto}</div>'
        f"</div>"
    )


def cartao_kpi(icone_nome: str, rotulo: str, valor: str, cor: str, ajuda: str = "") -> str:
    """
    Card de KPI (número grande + rótulo + ícone Lucide), com tarja
    colorida no topo e fundo branco — em vez do st.metric solto sobre o
    fundo da página. `ajuda` vira tooltip nativo do navegador (atributo
    title).
    """
    title_attr = f' title="{ajuda}"' if ajuda else ""
    marca_ajuda = '<span class="radar-kpi-ajuda">?</span>' if ajuda else ""
    return (
        f'<div class="radar-kpi-card"{title_attr}>'
        f'<div class="radar-kpi-tarja" style="background:{cor};"></div>'
        f'<div class="radar-kpi-cabecalho">'
        f'{icone(icone_nome, cor=cor, tamanho=18)}'
        f'<span class="radar-kpi-rotulo">{rotulo}{marca_ajuda}</span>'
        f"</div>"
        f'<div class="radar-kpi-valor">{valor}</div>'
        f"</div>"
    )


ICONE_EQUIPAMENTO = {
    "Biblioteca": "book-open",
    "Museu": "landmark",
    "Teatro / Sala de espetáculo": "drama",
    "Cinema": "clapperboard",
}


def chip_equipamento(nome: str, tem: bool) -> str:
    """
    Chip compacto de status de um equipamento cultural num município —
    ícone do próprio equipamento (Lucide) em vez de um check/x genérico,
    verde-cactos pra "tem" e terracota pra "não tem" (cores que se ajustam
    ao modo de daltonismo ativo). Substitui os blocos grandes e saturados
    da Demanda Cidadã: comunica o mesmo, sem dominar visualmente a página.
    """
    paleta = paleta_ativa()
    cor, fundo = (
        (paleta["demanda"], paleta["demanda_claro"])
        if tem
        else (paleta["deserto"], paleta["deserto_claro"])
    )
    icone_nome = ICONE_EQUIPAMENTO.get(nome, "landmark")
    return (
        f'<div class="radar-chip" style="border-color:{cor}; background:{fundo};">'
        f'<span class="radar-chip-simbolo" style="background:{cor};">'
        f'{icone(icone_nome, cor="#FFFDF8", tamanho=13)}</span>'
        f'<span class="radar-chip-nome" style="color:{cor};">{nome}</span>'
        f"</div>"
    )


def estado_vazio(icone_nome: str, texto: str, cor: str | None = None) -> str:
    """
    Bloco de estado vazio com ícone Lucide grande + texto — usado nos
    dois pontos do app onde "nada aconteceu ainda" (Simulador antes do
    clique no mapa, Demanda Cidadã antes do primeiro pedido) em vez de
    só uma caixa de texto azul (st.info), que fica igual a qualquer
    outro aviso do app e não comunica "está vazio por enquanto".
    """
    cor = cor or paleta_ativa()["simulador"]
    return (
        f'<div class="radar-vazio">'
        f'<div class="radar-vazio-icone" style="color:{cor};">'
        f'{icone(icone_nome, cor="currentColor", tamanho=34)}</div>'
        f'<div class="radar-vazio-texto">{texto}</div>'
        f"</div>"
    )


def titulo_secao(icone_nome: str, texto: str, cor: str | None = None) -> str:
    """
    Título de seção (equivalente a um st.subheader) com ícone Lucide ao
    lado — st.subheader/st.header não aceitam ícone nesta versão do
    Streamlit (só expander/button/download_button aceitam), daí este
    componente HTML próprio pra manter a mesma hierarquia visual do
    resto do app.
    """
    cor = cor or paleta_ativa()["deserto"]
    return (
        f'<div class="radar-titulo-secao">'
        f'<span style="color:{cor};">{icone(icone_nome, cor="currentColor", tamanho=22)}</span>'
        f"<h3>{texto}</h3>"
        f"</div>"
    )


def barra_secao(cor: str) -> str:
    """
    Pequena tarja colorida usada no topo de um painel/gráfico pra dar
    identidade visual própria à seção (em vez de tudo ficar na mesma cor).
    Usar com st.markdown(..., unsafe_allow_html=True) logo antes do título.
    """
    return f'<div class="radar-barra-secao" style="background:{cor};"></div>'


def marcador(nome: str) -> str:
    """
    Marcador invisível usado só como âncora de CSS: o Streamlit não deixa
    colocar classe direta nos containers dele, então soltamos este div
    logo antes do bloco que queremos estilizar e miramos nele com
    `:has()` + seletor de irmão adjacente (ver CSS_CUSTOMIZADO).
    """
    return f'<div class="radar-marcador-{nome}"></div>'


# ----------------------------------------------------------------------
# Componentes do "Deserto Cultural" — o conceito central do projeto
# ----------------------------------------------------------------------
COR_DESERTO = "#C1440E"
COR_DESERTO_CLARO = "#FBEBD4"


def selo_deserto(compacto: bool = False) -> str:
    """
    Selo visual de "Deserto Cultural" — usado em qualquer lugar que
    identifique um município sem museu, teatro nem cinema. Ter um símbolo
    próprio (e não só uma cor) dá peso conceitual ao termo e já funciona
    para quem tem daltonismo mesmo sem trocar de modo — a cor de fundo
    ainda se ajusta ao modo ativo via style inline (sobrepõe o CSS fixo).
    """
    cor = paleta_ativa()["deserto"]
    texto = "" if compacto else '<span class="radar-selo-deserto-texto">Deserto Cultural</span>'
    return (
        f'<span class="radar-selo-deserto" style="background:{cor};">'
        f'{icone("sun-dim", cor="#FFFDF8", tamanho=13)}'
        f"{texto}</span>"
    )


def contador_hero(numero: str, complemento: str, subtexto: str) -> str:
    """
    Número grande de impacto na tela inicial — resume o problema central
    do projeto numa frase só, antes de qualquer navegação.
    """
    cor = paleta_ativa()["deserto"]
    cor_escura = _escurecer(cor)
    return (
        f'<div class="radar-contador-hero" '
        f'style="background:linear-gradient(100deg, {cor} 0%, {cor_escura} 100%);">'
        f'<div class="radar-contador-hero-icone">{icone("sun-dim", cor="#FFFDF8", tamanho=30)}</div>'
        '<div class="radar-contador-hero-conteudo">'
        f'<div class="radar-contador-hero-numero">{numero}</div>'
        f'<div class="radar-contador-hero-complemento">{complemento}</div>'
        f'<div class="radar-contador-hero-subtexto">{subtexto}</div>'
        "</div>"
        "</div>"
    )


def box_glossario(titulo: str, texto: str, cor: str | None = None) -> str:
    """Box de definição fixa — usado pro glossário do 'Deserto Cultural'."""
    cor = cor or paleta_ativa()["deserto"]
    return (
        f'<div class="radar-glossario" style="border-left-color:{cor};">'
        f'<div class="radar-glossario-titulo" style="color:{cor};">'
        f'{icone("book-open-check", cor=cor, tamanho=17)}'
        f"<span>{titulo}</span></div>"
        f'<div class="radar-glossario-texto">{texto}</div>'
        "</div>"
    )


def cartao_conquista(
    icone_nome: str,
    titulo: str,
    descricao: str,
    desbloqueada: bool,
    atual: int,
    meta: int,
    cor: str | None = None,
) -> str:
    """
    Card de conquista (badge) — desbloqueada fica colorida e opaca,
    bloqueada fica esmaecida com o progresso rumo à meta.
    """
    cor = cor or paleta_ativa()["demanda"]
    if desbloqueada:
        classe = "radar-conquista desbloqueada"
        estilo = f"border-color:{cor}; background:#FFFDF8;"
        cor_icone = "#FFFDF8"
        fundo_icone = cor
        rodape = '<div class="radar-conquista-status" style="color:%s;">Desbloqueada</div>' % cor
    else:
        classe = "radar-conquista"
        estilo = "border-color:#E0D5C5; background:#FAF6F0;"
        cor_icone = "#FFFDF8"
        fundo_icone = "#C9BCAC"
        pct = int(100 * atual / meta) if meta else 0
        rodape = (
            '<div class="radar-conquista-barra">'
            f'<div class="radar-conquista-barra-preenchida" style="width:{pct}%;"></div>'
            "</div>"
            f'<div class="radar-conquista-status">{atual} de {meta}</div>'
        )

    return (
        f'<div class="{classe}" style="{estilo}">'
        f'<div class="radar-conquista-icone" style="background:{fundo_icone};">'
        f"{icone(icone_nome, cor=cor_icone, tamanho=18)}</div>"
        f'<div class="radar-conquista-titulo">{titulo}</div>'
        f'<div class="radar-conquista-descricao">{descricao}</div>'
        f"{rodape}"
        "</div>"
    )



# ----------------------------------------------------------------------
# CSS customizado da interface: tipografia própria (Inter em tudo, sem
# serifa), cards com borda/sombra terracota, KPIs em card, navbar em
# formato de segmented control, chips e tarjas de seção coloridas.
# ----------------------------------------------------------------------
CSS_CUSTOMIZADO = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ------------------------------------------------------------------
   TIPOGRAFIA — Inter em tudo (corpo e títulos). Sem serifa: mais neutra,
   mais legível em telas pequenas/baixa visão, e é o padrão mais comum
   pra painéis de dados e produtos públicos.
   ------------------------------------------------------------------ */
html, body, [data-testid="stAppViewContainer"], .stMarkdown, .stButton button,
input, select, textarea, [data-testid="stMetricValue"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
h1, h2, h3, h4,
.radar-header-titulo, .radar-hero-titulo, .radar-kpi-valor {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    letter-spacing: -0.01em;
}
h1, h2, h3 {
    font-weight: 700 !important;
    color: #2C1B12 !important;
}
h3 { font-size: 1.45rem !important; }

/* Cards com borda (st.container(border=True)) — borda mais suave que a
   terracota cheia de antes, que competia com o conteúdo do card */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #E7D5BE !important;
    border-radius: 16px !important;
    background-color: #FFFDF8 !important;
    box-shadow: 0 2px 10px rgba(122, 46, 14, 0.07);
    padding: 6px;
}

/* ------------------------------------------------------------------
   Cards de apresentação (hero) das 3 features na tela inicial.
   Flex + altura 100% iguala a "sola" dos três cards mesmo com textos de
   tamanhos diferentes — antes o min-height fixo deixava sobra embaixo do
   card de texto mais curto.
   ------------------------------------------------------------------ */
.radar-hero-card {
    border-top: 5px solid;
    border-radius: 16px;
    padding: 22px 22px 20px 22px;
    height: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 10px rgba(26, 15, 8, 0.07);
    margin-bottom: 12px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.radar-hero-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(26, 15, 8, 0.13);
}
.radar-hero-icone {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;
}
.radar-hero-titulo {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 10px;
}
.radar-hero-texto {
    font-size: 0.94rem;
    color: #4A3428;
    line-height: 1.55;
}
/* Iguala a altura das colunas do hero pra os cards esticarem juntos */
div[data-testid="stHorizontalBlock"]:has(.radar-hero-card) {
    align-items: stretch;
}
div[data-testid="stHorizontalBlock"]:has(.radar-hero-card)
    > div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
    height: 100%;
}

/* ------------------------------------------------------------------
   Cards de KPI — antes os números grandes flutuavam soltos no fundo da
   página, sem bloco visual que os agrupasse.
   ------------------------------------------------------------------ */
.radar-kpi-card {
    background: #FFFFFF;
    border: 1px solid #E7D5BE;
    border-radius: 14px;
    padding: 16px 18px 18px 18px;
    height: 100%;
    box-shadow: 0 2px 8px rgba(122, 46, 14, 0.06);
}
.radar-kpi-tarja {
    height: 4px;
    width: 34px;
    border-radius: 3px;
    margin-bottom: 12px;
}
.radar-kpi-cabecalho {
    display: flex;
    align-items: flex-start;
    gap: 8px;
}
.radar-kpi-rotulo {
    font-size: 0.82rem;
    font-weight: 600;
    color: #6B4226;
    line-height: 1.35;
    min-height: 2.7em;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}
.radar-kpi-valor {
    font-size: 2.1rem;
    font-weight: 800;
    color: #1A0F08;
    line-height: 1.1;
    margin-top: 4px;
}
.radar-kpi-ajuda {
    display: inline-block;
    margin-left: 6px;
    width: 15px;
    height: 15px;
    line-height: 15px;
    text-align: center;
    border-radius: 50%;
    background: #E7D5BE;
    color: #6B4226;
    font-size: 0.68rem;
    cursor: help;
    vertical-align: middle;
}

/* ------------------------------------------------------------------
   Chips de status (Demanda Cidadã) — substituem os blocos grandes e
   saturados: mesma informação, peso visual muito menor.
   ------------------------------------------------------------------ */
.radar-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    border: 1.5px solid;
    border-radius: 999px;
    padding: 8px 16px 8px 8px;
    font-size: 0.9rem;
    font-weight: 600;
}
.radar-chip-simbolo {
    flex: 0 0 auto;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.radar-chip-nome { line-height: 1.25; }

/* ------------------------------------------------------------------
   Estado vazio (Simulador antes do clique, Demanda Cidadã antes do
   primeiro pedido) — ícone grande + texto centralizados, em vez de uma
   caixa de aviso azul igual a qualquer outro st.info do app.
   ------------------------------------------------------------------ */
.radar-vazio {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 10px;
    padding: 36px 24px;
    background: #FBF5EC;
    border: 1.5px dashed #E0CBB0;
    border-radius: 16px;
}
.radar-vazio-icone {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(122, 46, 14, 0.08);
}
.radar-vazio-texto {
    font-size: 0.95rem;
    font-weight: 500;
    color: #6B4226;
    max-width: 360px;
    line-height: 1.5;
}

/* Título de seção com ícone (substitui st.subheader nos pontos em que
   queremos um ícone Lucide ao lado — ver titulo_secao() em theme.py) */
.radar-titulo-secao {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 4px 0 2px 0;
}
.radar-titulo-secao h3 {
    margin: 0 !important;
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

/* Métricas nativas (st.metric) — mantidas para telas que ainda as usam */
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

/* Botões em geral */
.stButton button {
    font-weight: 600 !important;
    border-radius: 10px !important;
    border-color: #E0CBB0 !important;
    transition: background-color 0.15s ease, border-color 0.15s ease,
                transform 0.1s ease;
}
.stButton button:hover {
    border-color: #C1440E !important;
    color: #C1440E !important;
}
.stButton button[kind="primary"] {
    box-shadow: 0 2px 8px rgba(193, 68, 14, 0.28);
}
.stButton button[kind="primary"]:hover {
    color: #FFFDF8 !important;
}

/* ------------------------------------------------------------------
   Navbar do Painel do Gestor em formato "segmented control": o bloco de
   colunas logo depois do marcador vira um trilho areia, e cada botão uma
   pílula dentro dele — deixa explícito que são abas, não ações soltas.
   ------------------------------------------------------------------ */
div[data-testid="stElementContainer"]:has(.radar-marcador-navbar)
    + div[data-testid="stHorizontalBlock"] {
    background: #F6EADA;
    border: 1px solid #E7D5BE;
    border-radius: 14px;
    padding: 6px;
    gap: 4px !important;
}
div[data-testid="stElementContainer"]:has(.radar-marcador-navbar)
    + div[data-testid="stHorizontalBlock"] .stButton button {
    background: transparent !important;
    border: none !important;
    color: #6B4226 !important;
    box-shadow: none !important;
    border-radius: 10px !important;
}
div[data-testid="stElementContainer"]:has(.radar-marcador-navbar)
    + div[data-testid="stHorizontalBlock"] .stButton button:hover {
    background: #EADCC6 !important;
    color: #7A2E0E !important;
}
div[data-testid="stElementContainer"]:has(.radar-marcador-navbar)
    + div[data-testid="stHorizontalBlock"] .stButton button[kind="primary"] {
    background: #FFFDF8 !important;
    color: #C1440E !important;
    box-shadow: 0 2px 6px rgba(122, 46, 14, 0.18) !important;
}

/* ------------------------------------------------------------------
   Expanders — antes eram barras brancas de largura total, quase
   invisíveis sobre o fundo claro da página.
   ------------------------------------------------------------------ */
div[data-testid="stExpander"] details {
    background: #FBF5EC !important;
    border: 1px solid #E7D5BE !important;
    border-radius: 12px !important;
}
div[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #6B4226 !important;
}
div[data-testid="stExpander"] summary:hover {
    color: #C1440E !important;
}

/* ------------------------------------------------------------------
   Opções da Demanda Cidadã (st.radio) como cartões clicáveis, em vez de
   uma lista apertada de bolinhas.
   ------------------------------------------------------------------ */
div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 8px;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label {
    background: #FFFFFF;
    border: 1.5px solid #E7D5BE;
    border-radius: 12px;
    padding: 10px 14px;
    margin: 0 !important;
    transition: border-color 0.15s ease, background-color 0.15s ease;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    border-color: #C1440E;
    background: #FFFDF8;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    border-color: #C1440E;
    background: #FBEBD4;
}

/* Tabelas (st.dataframe) — cabeçalho em areia e cantos arredondados */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E7D5BE;
}
div[data-testid="stDataFrame"] thead tr th {
    background: #FBEBD4 !important;
    color: #6B4226 !important;
    font-weight: 700 !important;
}

/* Caixas de mensagem (st.info) mais integradas à paleta */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Alinhamento vertical do botão "Ouvir" (componente em iframe, usado em
   src/acessibilidade.py) com o elemento ao lado dele na mesma linha de
   colunas. Por padrão um <iframe> é "display: inline", o que sozinho já
   cria um pequeno espaço fantasma abaixo dele; center garante que ele
   fique centralizado mesmo quando a linha é mais alta que o iframe. */
iframe {
    display: block;
}
div[data-testid="stHorizontalBlock"]:has(iframe) {
    align-items: center;
}

/* O Streamlit limita o conteúdo a uma coluna central e alguns dos
   contêineres pai cortam (overflow-x: hidden) qualquer coisa que tente
   vazar pra fora dessa coluna — isso libera esse corte especificamente
   pros elementos que precisam ser full-bleed (header/footer).
   IMPORTANTE: só o eixo X — mexer no Y quebra o scroll vertical da página,
   que o Streamlit implementa via overflow-y nesses mesmos containers. */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
[data-testid="stMainBlockContainer"],
.block-container,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"] {
    overflow-x: visible !important;
}
html, body {
    overflow-x: hidden !important;
}

/* Barra de ferramentas fixa do Streamlit (Share, estrela, lápis, GitHub) —
   pinta de laranja igual ao header, pra virar uma continuação dele em vez
   de ficar cortando o título por cima */
header[data-testid="stHeader"] {
    background: #C1440E !important;
}
header[data-testid="stHeader"] svg,
header[data-testid="stHeader"] button {
    filter: brightness(0) invert(1);
}

/* Reduz o respiro padrão do Streamlit acima e abaixo do conteúdo — em
   cima pra o header ficar rente à barra de ferramentas, embaixo pra o
   footer ficar colado no final da página. O padding lateral fica no
   padrão do Streamlit (é ele que a JS mede em sincronizar_padding_
   header, pra header/footer escaparem com a margem negativa certa). */
div[data-testid="stMainBlockContainer"],
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* Header — bloco terracota alinhado com o conteúdo (mesma largura e
   margem do resto da página). Não usa mais margem negativa nem 100vw
   pra "escapar" do container: aquilo brigava com a barra lateral (com
   vw, ficava escondido atrás dela; com margem negativa em rem, sobrava
   faixa branca porque o padding do Streamlit é responsivo). Alinhado,
   funciona com a sidebar aberta ou fechada, sem depender de acertar
   nenhum valor de padding. */
:root {
    /* Valor de segurança até o JS (sincronizar_padding_header) medir o
       padding real do container e substituir esse número — evita um
       "pulo" visual grande caso o JS demore uma fração de segundo. */
    --radar-padding-lateral: 4rem;
}
.radar-header {
    background: linear-gradient(120deg, #C1440E 0%, #A83A0C 100%) !important;
    border-radius: 0;
    padding-block: 30px 26px;
    padding-inline: var(--radar-padding-lateral);
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 4px 14px rgba(122, 46, 14, 0.28);
    width: auto;
    margin-inline: calc(-1 * var(--radar-padding-lateral));
    margin-bottom: 22px;
}
.radar-header-titulo {
    color: #FFFDF8 !important;
    font-size: 2.15rem;
    font-weight: 800;
    line-height: 1.15;
}
.radar-header-subtitulo {
    color: #FBEBD4 !important;
    font-size: 0.9rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    margin-top: 4px;
}

/* Footer — marrom bem escuro, contraste diferente do header de propósito.
   Alinhado com o conteúdo, igual ao header. */
.radar-footer {
    background: #2C1B12 !important;
    border-radius: 0;
    padding-block: 30px;
    padding-inline: var(--radar-padding-lateral);
    margin-top: 44px;
    margin-bottom: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: space-between;
    width: auto;
    margin-inline: calc(-1 * var(--radar-padding-lateral));
}
.radar-footer-col {
    flex: 1;
    min-width: 200px;
}
.radar-footer-titulo {
    color: #F2A93B !important;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.radar-footer-texto {
    color: #E8DFD5 !important;
    font-size: 0.85rem;
    line-height: 1.65;
}
/* ------------------------------------------------------------------
   DESERTO CULTURAL — selo, contador hero e box de glossário.
   O conceito central do projeto ganha identidade visual própria (ícone
   + cor + formato), em vez de ser só uma cor no mapa.
   ------------------------------------------------------------------ */
.radar-selo-deserto {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #C1440E;
    color: #FFFDF8;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 700;
    line-height: 1.3;
    white-space: nowrap;
    vertical-align: middle;
}
.radar-selo-deserto-texto { letter-spacing: 0.01em; }

.radar-contador-hero {
    display: flex;
    align-items: center;
    gap: 18px;
    background: linear-gradient(100deg, #C1440E 0%, #7A2E0E 100%);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 6px 0 18px 0;
    box-shadow: 0 4px 16px rgba(122, 46, 14, 0.22);
}
.radar-contador-hero-icone {
    flex: 0 0 auto;
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: rgba(255, 253, 248, 0.16);
    display: flex;
    align-items: center;
    justify-content: center;
}
.radar-contador-hero-conteudo { flex: 1 1 auto; min-width: 0; }
.radar-contador-hero-numero {
    color: #FFFDF8;
    font-size: 2.3rem;
    font-weight: 800;
    line-height: 1.05;
}
.radar-contador-hero-complemento {
    color: #FBEBD4;
    font-size: 1.02rem;
    font-weight: 700;
    margin-top: 2px;
}
.radar-contador-hero-subtexto {
    color: rgba(251, 235, 212, 0.82);
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 6px;
    line-height: 1.45;
}

.radar-glossario {
    background: #FFFDF8;
    border: 1px solid #EFE3D2;
    border-left: 5px solid #C1440E;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 4px 0 16px 0;
}
.radar-glossario-titulo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 800;
    font-size: 0.98rem;
    margin-bottom: 6px;
}
.radar-glossario-texto {
    color: #3E2723;
    font-size: 0.92rem;
    line-height: 1.55;
}

/* ------------------------------------------------------------------
   GAMIFICAÇÃO — cards de conquista (badges).
   ------------------------------------------------------------------ */
.radar-conquista {
    border: 2px solid;
    border-radius: 14px;
    padding: 14px 16px 12px 16px;
    min-height: 168px;
    display: flex;
    flex-direction: column;
    transition: transform 0.15s ease;
}
.radar-conquista.desbloqueada { box-shadow: 0 3px 10px rgba(76, 100, 68, 0.16); }
.radar-conquista-icone {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 9px;
}
.radar-conquista-titulo {
    font-weight: 800;
    font-size: 0.95rem;
    color: #1A0F08;
    margin-bottom: 3px;
}
.radar-conquista-descricao {
    font-size: 0.82rem;
    color: #5A4438;
    line-height: 1.4;
    flex: 1 1 auto;
}
.radar-conquista-status {
    font-size: 0.76rem;
    font-weight: 700;
    color: #6B4226;
    margin-top: 7px;
}
.radar-conquista-barra {
    height: 6px;
    border-radius: 999px;
    background: #E7DCCC;
    overflow: hidden;
    margin-top: 9px;
}
.radar-conquista-barra-preenchida {
    height: 100%;
    background: #B8792A;
    border-radius: 999px;
}

/* Link de acesso à Metodologia — colado no rodapé, estilizado discreto
   (sem fundo/borda chamativos) pra não competir com os cards hero */
div[data-testid="stElementContainer"]:has(.radar-marcador-link-metodologia)
    + div[data-testid="stHorizontalBlock"] .stButton button {
    background: transparent !important;
    border: none !important;
    color: #8A6A50 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    box-shadow: none !important;
    text-decoration: underline;
    text-decoration-color: transparent;
    transition: text-decoration-color 0.15s ease, color 0.15s ease;
}
div[data-testid="stElementContainer"]:has(.radar-marcador-link-metodologia)
    + div[data-testid="stHorizontalBlock"] .stButton button:hover {
    color: #C1440E !important;
    text-decoration-color: #C1440E;
}

/* ------------------------------------------------------------------
   CARD DE FEEDBACK — autor/texto com hierarquia própria e botões
   compactos (like/dislike/responder). O avatar (foto ou emoji) é
   gerado inline pelo helper _avatar_html no streamlit_app.py, não por
   uma classe CSS fixa — foto e emoji precisam de estilos diferentes
   (img recortada vs. div com fundo), então o HTML já sai pronto.
   Usado nas 3 features que exibem feedback.
   ------------------------------------------------------------------ */
.radar-feedback-autor {
    font-weight: 700;
    font-size: 0.94rem;
    color: #1A0F08;
    margin-top: 2px;
}
.radar-feedback-local {
    font-weight: 500;
    color: #8A6A50;
}
.radar-feedback-texto {
    color: #3E2723;
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 4px 0 2px 0;
}
.radar-feedback-resposta {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    background: #FAF6F0;
    border-left: 3px solid #E0CDB0;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 6px 0 0 20px;
    font-size: 0.87rem;
    color: #3E2723;
    line-height: 1.45;
}
/* Botões de ação do card mais compactos que o padrão do Streamlit */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.radar-marcador-feedback-card)
    .stButton button {
    padding: 2px 12px !important;
    min-height: 32px !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
}

</style>
"""