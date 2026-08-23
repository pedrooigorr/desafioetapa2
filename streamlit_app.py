"""
Radar Cultural — Squad ZeroKai
Desafio dos Dados VIVO 2026 — Etapa 2

Três features num só app:
  - Painel do Gestor: equidade no acesso a equipamentos culturais nos
    184 municípios do Ceará. Fala com quem decide política pública.
  - Demanda Cidadã: o cidadão escolhe seu município, vê o que já existe
    e registra o que mais gostaria de ver entre o que falta — vira
    contador público, peso no Índice de Prioridade e sugestão no
    Simulador.
  - Simulador & Transparência: simula o impacto de instalar um
    equipamento num município, e gera cards públicos de cobrança cívica
    a partir do Índice de Prioridade.

Este arquivo só monta a página. Lógica de dados do Radar está em
src/data_loader.py, gráficos em src/charts.py, paleta em src/theme.py,
demanda cidadã em src/demanda.py, simulador em src/simulador.py e o
painel de transparência em src/transparencia.py.
"""

import pandas as pd
import streamlit as st

from src.acessibilidade import (
    botao_ouvir,
    css_acessibilidade,
    inicializar_preferencias,
    renderizar_controles_topo,
)
from src.charts import (
    grafico_equidade_por_mesorregiao,
    grafico_presenca_equipamentos,
    mapa_municipios,
    mapa_simulador,
)
from src.data_loader import (
    EQUIPAMENTOS,
    aplicar_filtros,
    carregar_dados,
    montar_tabela_prioritarios,
)
from src.demanda import (
    CATEGORIAS_SIMULAVEIS,
    MAPA_CATEGORIA_COLUNA,
    categoria_mais_pedida,
    categorias_existentes,
    categorias_faltantes,
    inicializar_feedbacks,
    inicializar_pedidos,
    ja_votou_no_municipio,
    listar_feedbacks,
    pedidos_do_municipio,
    peso_demanda,
    ranking_pedidos_ceara,
    registrar_feedback,
    registrar_pedido,
    total_feedbacks,
    total_pedidos,
)
from src.gamificacao import (
    AVATARES,
    avaliar_conquistas,
    inicializar_gamificacao,
    nome_exibicao,
    perfil_definido,
    progresso_exploracao,
    registrar_exploracao,
    resumo_conquistas,
)
from src.resumos import (
    resumo_demanda_cidada,
    resumo_equidade_mesorregiao,
    resumo_mapa,
    resumo_municipios_prioritarios,
    resumo_presenca_equipamentos,
    resumo_simulador,
    resumo_transparencia,
    resumo_visao_geral,
)
from src.simulador import (
    TIPOS_EQUIPAMENTO,
    calcular_simulacao,
)
from src.theme import (
    COR_DEMANDA,
    COR_DEMANDA_CLARO,
    COR_GESTOR,
    COR_GESTOR_CLARO,
    COR_NEUTRA,
    COR_SIMULADOR,
    COR_SIMULADOR_CLARO,
    CSS_CUSTOMIZADO,
    barra_secao,
    box_glossario,
    cabecalho_app,
    cartao_conquista,
    cartao_hero,
    cartao_kpi,
    chip_equipamento,
    contador_hero,
    destacar_coluna,
    estado_vazio,
    estilo_texto_tabela,
    marcador,
    rodape_app,
    selo_deserto,
    titulo_secao,
)
from src.transparencia import gerar_card_municipio, montar_ranking_publico

st.set_page_config(
    page_title="Radar Cultural — ZeroKai",
    layout="wide",
)

st.markdown(CSS_CUSTOMIZADO, unsafe_allow_html=True)

inicializar_pedidos()
inicializar_feedbacks()
inicializar_preferencias()
inicializar_gamificacao()

df = carregar_dados()

# ----------------------------------------------------------------------
# CSS de acessibilidade — os controles em si aparecem logo abaixo do
# cabeçalho, mais adiante
# ----------------------------------------------------------------------
st.markdown(css_acessibilidade(), unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Cabeçalho + seletor de modo (as três features do projeto)
# ----------------------------------------------------------------------
MODOS = [
    "Painel do Gestor",
    "Demanda Cidadã",
    "Simulador & Transparência",
    "Metodologia",
]
if "modo_app" not in st.session_state:
    st.session_state.modo_app = MODOS[0]


def ir_para_modo(modo: str):
    st.session_state.modo_app = modo


def _render_resumo(texto: str, key: str):
    """Resumo de 1 frase + botão de ouvir — usado no topo de cada painel
    e como resumo automático de cada gráfico principal (acessibilidade)."""
    col_texto, col_botao = st.columns([5, 1])
    with col_texto:
        st.info(texto)
    with col_botao:
        botao_ouvir(texto, key=key)


@st.dialog("Meu Perfil", width="large")
def abrir_perfil():
    """
    Perfil leve — apelido + avatar, sem senha nem conta — e as conquistas
    da sessão. Abre como modal (janela por cima da página) em vez de
    virar uma aba/modo: é conteúdo de apoio, não uma das 3 features do
    projeto, então não compete por espaço com elas na navegação principal.
    """
    st.caption(
        "Um apelido e um avatar — sem senha, sem conta. Só pra dar cara "
        "às suas conquistas nesta sessão. Some tudo ao recarregar a "
        "página, do mesmo jeito que os pedidos da Demanda Cidadã."
    )

    col_avatar, col_dados = st.columns([1, 3])
    with col_avatar:
        st.markdown(
            f'<div style="font-size:56px; text-align:center; '
            f'line-height:1;">{st.session_state.get("perfil_avatar", "🎭")}'
            f"</div>",
            unsafe_allow_html=True,
        )
        st.selectbox(
            "Avatar",
            AVATARES,
            key="perfil_avatar",
            label_visibility="collapsed",
        )
    with col_dados:
        st.text_input(
            "Apelido",
            key="perfil_apelido",
            placeholder="Como quer ser chamado(a)?",
            max_chars=30,
        )
        st.text_input(
            "Seu município (opcional)",
            key="perfil_local",
            placeholder="De onde você é?",
        )

    if not perfil_definido():
        st.info("Escolhe um apelido acima pra personalizar seu perfil.")

    st.divider()
    n_desbloqueadas, n_total_conquistas = resumo_conquistas(df)
    st.markdown(
        titulo_secao(
            "trophy",
            f"Sua jornada ({n_desbloqueadas} de {n_total_conquistas} conquistas)",
            cor=COR_NEUTRA,
        ),
        unsafe_allow_html=True,
    )

    explorados, total_municipios, fracao = progresso_exploracao()
    st.markdown(
        f"**Você já explorou {explorados} de {total_municipios} municípios "
        f"do Ceará** ({fracao * 100:.0f}%)"
    )
    st.progress(fracao)
    st.caption(
        "Conta municípios que você abriu na Demanda Cidadã ou clicou no "
        "mapa do Simulador."
    )
    if total_feedbacks() > 0:
        st.caption(
            f"Você também já deixou {total_feedbacks()} feedback(s) na "
            "Demanda Cidadã."
        )

    st.markdown("##### Conquistas")
    conquistas = avaliar_conquistas(df)
    for i in range(0, len(conquistas), 3):
        for col, conquista in zip(st.columns(3), conquistas[i : i + 3]):
            with col:
                st.markdown(
                    cartao_conquista(
                        icone_nome=conquista["icone"],
                        titulo=conquista["titulo"],
                        descricao=conquista["descricao"],
                        desbloqueada=conquista["desbloqueada"],
                        atual=conquista["atual"],
                        meta=conquista["meta"],
                        cor=COR_NEUTRA,
                    ),
                    unsafe_allow_html=True,
                )


st.markdown(cabecalho_app(), unsafe_allow_html=True)
st.markdown(
    "### Bem-vindo(a) ao Radar Cultural!\n"
    "**Quem no Ceará tem acesso a cultura perto de casa — e quem não "
    "tem?** Cruzamos dados oficiais dos 184 municípios pra mostrar onde "
    "a cultura está concentrada e onde ela quase não chega."
)
renderizar_controles_topo()

# Ícone de acesso ao Perfil — visível pra qualquer pessoa (gestor ou
# cidadão comum), sem login. Abre como modal (janela por cima da
# página), não como aba nova — o projeto continua sendo uma página só.
_col_perfil, _, _ = st.columns([1.2, 1, 1])
with _col_perfil:
    _nome_perfil = nome_exibicao() if perfil_definido() else "Meu Perfil"
    _avatar_atual = st.session_state.get("perfil_avatar", "🎭")
    if st.button(
        f"{_avatar_atual} {_nome_perfil}",
        key="btn_perfil",
        use_container_width=True,
        icon=":material/account_circle:",
    ):
        abrir_perfil()

# ----------------------------------------------------------------------
# Ordem pensada pra contar a história antes de mostrar o dado: primeiro
# explica o conceito central (Deserto Cultural), só depois mostra o
# número de impacto — assim quem chega já sabe o que aquele "81" quer
# dizer antes de ver ele.
# ----------------------------------------------------------------------
st.markdown(
    box_glossario(
        "O que é um Deserto Cultural?",
        "Município que <b>não tem nenhum</b> museu, teatro/sala de "
        "espetáculo ou cinema — mesmo que já tenha biblioteca (que existe "
        "em praticamente todos os municípios cearenses — 99,5%, só Graça "
        "é exceção — e por isso não diferencia quem tem acesso de quem "
        "não tem).",
    ),
    unsafe_allow_html=True,
)

_n_desertos = int((df["n_equipamentos_raros"] == 0).sum())
_pct_desertos = 100 * _n_desertos / len(df)
_pop_desertos = int(df.loc[df["n_equipamentos_raros"] == 0, "populacao"].sum())

st.markdown(
    contador_hero(
        numero=f"{_n_desertos} municípios ({_pct_desertos:.0f}%)",
        complemento="do Ceará são Desertos Culturais",
        subtexto=(
            f"São {_pop_desertos:,}".replace(",", ".")
            + " pessoas que não têm museu, teatro nem cinema na cidade "
            "onde moram."
        ),
    ),
    unsafe_allow_html=True,
)

CARDS_HERO = [
    {
        "modo": MODOS[0],
        "icone": "landmark",
        "titulo": "Painel do Gestor",
        "texto": (
            "O raio-x da desigualdade cultural nos 184 municípios do "
            "Ceará. Pra quem decide política pública."
        ),
        "cor": COR_GESTOR,
        "cor_clara": COR_GESTOR_CLARO,
    },
    {
        "modo": MODOS[1],
        "icone": "vote",
        "titulo": "Demanda Cidadã",
        "texto": (
            "Escolha seu município e registre o que falta. Seu pedido "
            "pesa de verdade no ranking de prioridades."
        ),
        "cor": COR_DEMANDA,
        "cor_clara": COR_DEMANDA_CLARO,
    },
    {
        "modo": MODOS[2],
        "icone": "piggy-bank",
        "titulo": "Simulador & Transparência",
        "texto": (
            "Simule o impacto de um novo equipamento cultural — e cobre "
            "publicamente investimento com cards prontos pra compartilhar."
        ),
        "cor": COR_SIMULADOR,
        "cor_clara": COR_SIMULADOR_CLARO,
    },
]

st.markdown("##### Três jeitos de explorar isso — escolha por onde começar")
hero_cols = st.columns(3)
for col, card in zip(hero_cols, CARDS_HERO):
    with col:
        st.markdown(
            cartao_hero(
                card["icone"], card["titulo"], card["texto"],
                card["cor"], card["cor_clara"],
            ),
            unsafe_allow_html=True,
        )
        esta_aqui = st.session_state.modo_app == card["modo"]
        st.button(
            "Você está aqui" if esta_aqui else f"Abrir {card['titulo']} →",
            key=f"hero_btn_{card['titulo']}",
            use_container_width=True,
            type="primary" if esta_aqui else "secondary",
            on_click=ir_para_modo,
            args=(card["modo"],),
        )

st.divider()

# ========================================================================
# MODO 1 — PAINEL DO GESTOR (Radar Cultural)
# ========================================================================
if st.session_state.modo_app == MODOS[0]:
    PAGINAS = [
        "Visão Geral",
        "Mapa do Ceará",
        "Presença de Equipamentos",
        "Equidade por Mesorregião",
        "Municípios Prioritários",
    ]

    if "pagina" not in st.session_state:
        st.session_state.pagina = PAGINAS[0]

    def ir_para(pagina: str):
        st.session_state.pagina = pagina

    st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
    with st.expander("Sobre os dados exibidos", icon=":material/info:"):
        st.markdown(
            "- **Equipamentos culturais** (museu, teatro/sala de espetáculo, "
            "cinema, biblioteca): IBGE, Pesquisa de Informações Básicas "
            "Municipais (MUNIC), Suplemento de Cultura **2021**.\n"
            "- **População**: IBGE, Censo Demográfico **2022** (resultado do "
            "Universo, definitivo) — tabela SIDRA 4714.\n"
            "- **Renda per capita**: IBGE, Censo Demográfico **2022** "
            "(resultado preliminar da amostra — o IBGE ainda não fechou as "
            "áreas de ponderação definitivas, mas já é o dado mais atual "
            "disponível) — tabela SIDRA 10295.\n\n"
            "Como a MUNIC (2021) e o Censo (2022) são de anos próximos, o "
            "conjunto de dados é bem contemporâneo — bem diferente da "
            "versão anterior deste painel, que cruzava MUNIC 2014 com "
            "Censo 2010. Ver `data/README.md` para detalhes de como as "
            "bases foram cruzadas.\n\n"
            "**Atenção, não confundir:** a 'Renda per capita' usada aqui é a "
            "**renda domiciliar** — quanto cada pessoa recebe, em média, "
            "somando a renda de todo mundo em casa (Censo 2022). É "
            "**diferente** do **PIB per capita** que aparece no IBGE Cidades "
            "(todo o PIB do município — inclusive gastos públicos, "
            "agropecuária, indústria — dividido pela população). São "
            "métricas distintas; não é incomum um município ter PIB per "
            "capita relativamente alto e renda domiciliar baixa, quando boa "
            "parte da economia local vem da administração pública."
        )

    # --------------------------------------------------------------
    # Filtros (expander horizontal, agrupados por categoria)
    # --------------------------------------------------------------
    todas_mesorregioes = sorted(df["mesorregiao"].unique())
    pop_min, pop_max = int(df["populacao"].min()), int(df["populacao"].max())

    def _n_filtros_ativos_gestor() -> int:
        n = 0
        if set(st.session_state.get("filtro_mesorregioes", todas_mesorregioes)) != set(
            todas_mesorregioes
        ):
            n += 1
        if st.session_state.get("filtro_excluir_fortaleza", False):
            n += 1
        if st.session_state.get("filtro_faixa_pop", (pop_min, pop_max)) != (
            pop_min,
            pop_max,
        ):
            n += 1
        if st.session_state.get("filtro_equip", []):
            n += 1
        return n

    def _limpar_filtros_gestor():
        st.session_state.filtro_mesorregioes = todas_mesorregioes
        st.session_state.filtro_excluir_fortaleza = False
        st.session_state.filtro_faixa_pop = (pop_min, pop_max)
        st.session_state.filtro_equip = []

    n_ativos = _n_filtros_ativos_gestor()
    rotulo_filtros = "Filtros" + (
        f" · {n_ativos} ativo{'s' if n_ativos != 1 else ''}" if n_ativos else ""
    )

    with st.expander(rotulo_filtros, expanded=False, icon=":material/filter_alt:"):
        col_titulo, col_limpar = st.columns([4, 1])
        with col_titulo:
            st.caption("Ajuste o recorte de municípios usado em todos os gráficos abaixo.")
        with col_limpar:
            st.button(
                "Limpar filtros",
                icon=":material/filter_alt_off:",
                on_click=_limpar_filtros_gestor,
                use_container_width=True,
                disabled=n_ativos == 0,
            )

        st.markdown("**Localização**")
        col_meso, col_fortaleza = st.columns([3, 1])
        with col_meso:
            mesorregioes_sel = st.pills(
                "Mesorregião",
                todas_mesorregioes,
                selection_mode="multi",
                default=todas_mesorregioes,
                key="filtro_mesorregioes",
                label_visibility="collapsed",
            )
        with col_fortaleza:
            excluir_fortaleza = st.checkbox(
                "Excluir Fortaleza",
                key="filtro_excluir_fortaleza",
                help="Fortaleza concentra grande parte da população e dos "
                "equipamentos — marque para ver só o padrão do interior",
            )

        st.markdown("**População**")
        faixa_pop = st.slider(
            "Faixa de população",
            pop_min,
            pop_max,
            value=(pop_min, pop_max),
            key="filtro_faixa_pop",
            label_visibility="collapsed",
        )

        st.markdown("**Equipamentos**")
        equip_filtro = st.pills(
            "Mostrar apenas municípios SEM:",
            options=list(EQUIPAMENTOS.values()),
            selection_mode="multi",
            default=[],
            key="filtro_equip",
            help="Selecione um ou mais equipamentos para ver só quem não tem",
        )

    df_f = aplicar_filtros(
        df,
        mesorregioes=mesorregioes_sel or [],
        faixa_populacao=faixa_pop,
        excluir_fortaleza=excluir_fortaleza,
        equipamentos_ausentes=equip_filtro or [],
    )

    # --------------------------------------------------------------
    # Navbar
    # --------------------------------------------------------------
    st.markdown(marcador("navbar"), unsafe_allow_html=True)
    nav_cols = st.columns(len(PAGINAS))
    for col, pagina in zip(nav_cols, PAGINAS):
        with col:
            st.button(
                pagina,
                use_container_width=True,
                type="primary" if st.session_state.pagina == pagina else "secondary",
                on_click=ir_para,
                args=(pagina,),
            )

    st.write("")

    # --------------------------------------------------------------
    # KPIs
    # --------------------------------------------------------------
    pct_sem_museu = 100 * (~df_f["tem_museu"]).mean() if len(df_f) else 0
    pop_desassistida = df_f.loc[df_f["n_equipamentos_raros"] == 0, "populacao"].sum()

    KPIS = [
        {
            "icone": "map-pinned",
            "rotulo": "Municípios analisados",
            "valor": f"{len(df_f):,}".replace(",", "."),
            "cor": COR_GESTOR,
            "ajuda": "",
        },
        {
            "icone": "circle-x",
            "rotulo": "Sem museu, teatro nem cinema",
            "valor": f"{(df_f['n_equipamentos_raros'] == 0).sum():,}".replace(",", "."),
            "cor": "#C1440E",
            "ajuda": "Biblioteca não entra aqui — praticamente todos os "
            "municípios do Ceará já têm uma, então ela não ajuda a distinguir "
            "quem tem acesso cultural de quem não tem",
        },
        {
            "icone": "percent",
            "rotulo": "% sem museu",
            "valor": f"{pct_sem_museu:.1f}%",
            "cor": "#F2A93B",
            "ajuda": "",
        },
        {
            "icone": "users",
            "rotulo": "População sem museu, teatro ou cinema por perto",
            "valor": f"{pop_desassistida:,.0f}".replace(",", "."),
            "cor": "#8C1C13",
            "ajuda": "",
        },
    ]
    for col, kpi in zip(st.columns(4), KPIS):
        with col:
            st.markdown(
                cartao_kpi(
                    kpi["icone"], kpi["rotulo"], kpi["valor"],
                    kpi["cor"], kpi["ajuda"],
                ),
                unsafe_allow_html=True,
            )

    st.write("")

    # --------------------------------------------------------------
    # Conteúdo — Visão Geral (painéis compactos) ou página dedicada
    # --------------------------------------------------------------
    pagina_atual = st.session_state.pagina

    if pagina_atual == "Visão Geral":
        st.caption(
            "Prévia de todas as análises abaixo. Clique em um card ou na "
            "navbar acima pra abrir a versão completa de cada uma."
        )
        _render_resumo(resumo_visao_geral(df_f), key="resumo_visao_geral")

        linha1_a, linha1_b = st.columns(2)
        with linha1_a, st.container(border=True):
            st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
            st.markdown(titulo_secao("map", "Mapa do Ceará", COR_GESTOR), unsafe_allow_html=True)
            st.plotly_chart(
                mapa_municipios(df_f, altura=280),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.button(
                "Ver página completa →",
                key="btn_mapa",
                on_click=ir_para,
                args=("Mapa do Ceará",),
            )

        with linha1_b, st.container(border=True):
            st.markdown(barra_secao("#F2A93B"), unsafe_allow_html=True)
            st.markdown(titulo_secao("building-2", "Presença de Equipamentos", "#F2A93B"), unsafe_allow_html=True)
            st.plotly_chart(
                grafico_presenca_equipamentos(df_f, altura=260),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.button(
                "Ver página completa →",
                key="btn_presenca",
                on_click=ir_para,
                args=("Presença de Equipamentos",),
            )

        linha2_a, linha2_b = st.columns(2)
        with linha2_a, st.container(border=True):
            st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
            st.markdown(titulo_secao("trending-up", "Equidade por Mesorregião", COR_DEMANDA), unsafe_allow_html=True)
            st.plotly_chart(
                grafico_equidade_por_mesorregiao(df_f, altura=280),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.button(
                "Ver página completa →",
                key="btn_equidade",
                on_click=ir_para,
                args=("Equidade por Mesorregião",),
            )

        with linha2_b, st.container(border=True):
            st.markdown(barra_secao("#8C1C13"), unsafe_allow_html=True)
            st.markdown(titulo_secao("flag-triangle-right", "Municípios Prioritários", "#8C1C13"), unsafe_allow_html=True)
            tabela_preview = montar_tabela_prioritarios(df_f, n=5)
            st.dataframe(
                tabela_preview.style.set_properties(**estilo_texto_tabela())
                .apply(destacar_coluna, subset=["Índice de Prioridade"])
                .format(
                    {
                        "Índice de Prioridade": "{:.2f}",
                        "Renda per capita (R$, Censo 2022)": "{:.2f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
                height=245,
            )
            st.button(
                "Ver página completa →",
                key="btn_prioritarios",
                on_click=ir_para,
                args=("Municípios Prioritários",),
            )

    elif pagina_atual == "Mapa do Ceará":
        st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
        st.markdown(titulo_secao("map", "Mapa do Ceará — renda e população por município", COR_GESTOR), unsafe_allow_html=True)
        st.caption(
            "Cada ponto é um município — o tamanho indica a população e a cor "
            "indica a renda per capita. Passe o mouse para ver detalhes, "
            "incluindo o número de equipamentos culturais."
        )
        _render_resumo(resumo_mapa(df_f), key="resumo_mapa")
        st.plotly_chart(mapa_municipios(df_f, altura=680), use_container_width=True)

        with st.expander("Como esse mapa foi feito", icon=":material/help:"):
            st.markdown(
                "1. Pegamos o **contorno oficial do Ceará** (fronteira do "
                "estado) e as coordenadas (latitude/longitude) dos 184 "
                "municípios.\n"
                "2. Cobrimos os estados vizinhos com uma máscara na cor de "
                "fundo do app, mantendo o mapa real (OpenStreetMap, com "
                "nomes de cidades e estradas) visível só dentro do "
                "Ceará.\n"
                "3. Cada ponto representa um município — o **tamanho** é "
                "proporcional à **população** e a **cor** é proporcional à "
                "**renda per capita** (quanto mais forte o terracota, maior a "
                "renda).\n\n"
                "**Por que um mapa em vez de uma tabela?** Fica muito mais "
                "fácil enxergar de cara o padrão geográfico: renda mais alta "
                "concentrada perto de Fortaleza e do litoral, caindo conforme "
                "se afasta para o interior/sertão."
            )

    elif pagina_atual == "Presença de Equipamentos":
        st.markdown(barra_secao("#F2A93B"), unsafe_allow_html=True)
        st.markdown(titulo_secao("building-2", "Presença de cada equipamento cultural", "#F2A93B"), unsafe_allow_html=True)
        st.caption(
            "% dos municípios filtrados que possuem cada tipo de equipamento "
            "cultural."
        )
        _render_resumo(resumo_presenca_equipamentos(df_f), key="resumo_presenca")
        st.plotly_chart(
            grafico_presenca_equipamentos(df_f, altura=680), use_container_width=True
        )

        with st.expander("Como esse gráfico foi feito", icon=":material/help:"):
            st.markdown(
                "Para cada um dos 4 equipamentos (museu, teatro/sala de "
                "espetáculo, cinema e biblioteca), calculamos:\n\n"
                "`% = (nº de municípios filtrados que têm o equipamento) "
                "÷ (total de municípios filtrados) × 100`\n\n"
                "Os dados de existência de cada equipamento vêm da MUNIC/IBGE "
                "2021, respondida pela própria prefeitura de cada município. "
                "**Achado curioso:** biblioteca aparece em 99,5% dos "
                "municípios (só Graça é exceção) "
                "— por isso ela não é usada nas análises de equidade e "
                "prioridade mais à frente, já que não ajuda a diferenciar "
                "quem tem acesso cultural de quem não tem."
            )

    elif pagina_atual == "Equidade por Mesorregião":
        st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
        st.markdown(titulo_secao("trending-up", "Equidade cultural por Mesorregião", COR_DEMANDA), unsafe_allow_html=True)
        st.caption(
            "% de municípios sem museu, teatro ou cinema em cada mesorregião — "
            "a cor mostra a renda média per capita da região."
        )
        _render_resumo(resumo_equidade_mesorregiao(df_f), key="resumo_equidade")
        st.plotly_chart(
            grafico_equidade_por_mesorregiao(df_f, altura=680), use_container_width=True
        )

        with st.expander("Como esse gráfico foi feito", icon=":material/help:"):
            st.markdown(
                "1. Agrupamos os municípios filtrados pelas suas 7 "
                "**mesorregiões** oficiais do IBGE (Metropolitana de "
                "Fortaleza, Norte, Noroeste, Sertões, Jaguaribe, Centro-Sul e "
                "Sul Cearense).\n"
                "2. Para cada mesorregião, calculamos o **% de municípios sem "
                "nenhum** dos 3 equipamentos que de fato diferenciam acesso "
                "cultural (museu, teatro ou cinema — biblioteca fica de fora "
                "por ser praticamente universal).\n"
                "3. A cor das barras mostra a **renda média per capita** da "
                "mesorregião, para cruzar as duas informações num só gráfico.\n\n"
                "O resultado mostra o que a intuição já sugere: a "
                "Metropolitana de Fortaleza tem a menor % de municípios "
                "desassistidos e a maior renda — o interior carrega o ônus "
                "duplo de menos renda e menos acesso cultural."
            )

    elif pagina_atual == "Municípios Prioritários":
        st.markdown(barra_secao("#8C1C13"), unsafe_allow_html=True)
        st.markdown(titulo_secao("flag-triangle-right", "Municípios prioritários (baixa renda + pouco acesso)", "#8C1C13"), unsafe_allow_html=True)
        st.caption(
            "Ranking pelo Índice de Prioridade: combina ausência de museu, "
            "teatro ou cinema com baixa renda per capita — quanto maior, mais "
            "urgente a atenção."
        )
        _render_resumo(resumo_municipios_prioritarios(df_f), key="resumo_prioritarios")
        total_filtrado = len(df_f)
        if total_filtrado == 0:
            st.markdown(
                estado_vazio(
                    "circle-x",
                    "Nenhum município corresponde aos filtros escolhidos. "
                    "Ajusta a mesorregião ou a faixa de população na barra "
                    "lateral.",
                    cor="#8C1C13",
                ),
                unsafe_allow_html=True,
            )
        else:
            # min_value não pode ser fixo em 10: se o filtro deixar menos
            # de 10 municípios, min > max e o slider quebra a página
            # inteira (StreamlitAPIException). Se sobrar só 1 município,
            # nem faz sentido mostrar o slider.
            minimo_slider = min(10, total_filtrado)
            if minimo_slider < total_filtrado:
                n_linhas = st.slider(
                    "Quantos municípios mostrar",
                    min_value=minimo_slider,
                    max_value=total_filtrado,
                    value=min(30, total_filtrado),
                )
            else:
                n_linhas = total_filtrado
            tabela_completa = montar_tabela_prioritarios(df_f, n=n_linhas)
            tabela_completa["Pedidos da população"] = tabela_completa["Município"].map(
                total_pedidos
            )
            tabela_completa["Índice Ajustado (c/ demanda)"] = tabela_completa[
                "Município"
            ].map(lambda m: peso_demanda(m)) + tabela_completa["Índice de Prioridade"]

            if tabela_completa["Pedidos da população"].sum() > 0:
                st.caption(
                    "As colunas **Pedidos da população** e **Índice Ajustado** "
                    "vêm dos pedidos registrados em 'Demanda Cidadã' nesta sessão."
                )

            st.dataframe(
                tabela_completa.style.set_properties(**estilo_texto_tabela())
                .apply(destacar_coluna, subset=["Índice de Prioridade"])
                .format(
                    {
                        "Índice de Prioridade": "{:.2f}",
                        "Renda per capita (R$, Censo 2022)": "{:.2f}",
                        "Índice Ajustado (c/ demanda)": "{:.2f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
                height=650,
            )

        with st.expander("Como esse ranking foi feito", icon=":material/help:"):
            st.markdown(
                "Criamos o **Índice de Prioridade** para combinar, num só "
                "número, dois fatores que juntos indicam urgência de "
                "atenção: **falta de equipamento cultural** e **baixa renda**."
                "\n\n"
                "Fórmula:\n\n"
                "`Índice = (3 − nº de equipamentos raros) × "
                "(1 − renda per capita ÷ maior renda per capita do estado)`\n\n"
                "Onde \"equipamentos raros\" conta só museu, teatro e cinema "
                "(de 0 a 3) — biblioteca fica de fora por existir em quase "
                "todo município. Assim, um município **sem nenhum** desses "
                "3 equipamentos e com renda **bem abaixo** da média pontua "
                "alto; um município rico mesmo sem equipamentos, ou um "
                "município pobre mas já bem servido culturalmente, pontua "
                "mais baixo. Quanto maior o índice, mais o município "
                "**merece atenção prioritária**.\n\n"
                "O **Índice Ajustado** soma a esse índice um peso pequeno e "
                "suave (raiz quadrada do total de pedidos, ×0,05) vindo dos "
                "pedidos registrados em 'Demanda Cidadã' — assim a "
                "demanda real da população também conta, sem sozinha virar "
                "o ranking de cabeça pra baixo."
            )

    st.divider()
    st.caption(
        "Fontes: IBGE — Pesquisa de Informações Básicas Municipais (MUNIC), "
        "Suplemento de Cultura 2021 · IBGE — Censo Demográfico 2022 "
        "(população e renda per capita municipal)."
    )

# ========================================================================
# MODO 2 — DEMANDA CIDADÃ
# ========================================================================
elif st.session_state.modo_app == MODOS[1]:
    st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
    st.markdown(
        "### O que falta de cultura na sua cidade?\n"
        "Escolha seu município, veja o que já existe lá — e registre, "
        "entre o que falta, o que você mais gostaria de ver. Seu pedido "
        "entra numa contagem pública e ajuda a apontar pra onde o "
        "investimento deveria ir."
    )
    _render_resumo(resumo_demanda_cidada(), key="resumo_demanda")

    municipio_cidadao = st.selectbox(
        "Meu município", sorted(df["municipio"].unique())
    )
    registrar_exploracao(municipio_cidadao)
    linha_municipio = df.loc[df["municipio"] == municipio_cidadao].iloc[0]

    st.markdown(f"##### O que {municipio_cidadao} já tem")
    existentes = categorias_existentes(df, municipio_cidadao)
    cols_existentes = st.columns(4)
    for col, categoria in zip(cols_existentes, MAPA_CATEGORIA_COLUNA):
        with col:
            st.markdown(
                chip_equipamento(categoria, categoria in existentes),
                unsafe_allow_html=True,
            )

    st.divider()

    st.markdown(f"##### O que você mais gostaria de ver em {municipio_cidadao}?")

    if ja_votou_no_municipio(municipio_cidadao):
        st.info(
            f"Você já registrou um pedido para **{municipio_cidadao}** "
            "nesta sessão — obrigado! Escolha outro município acima pra "
            "votar de novo, ou recarregue a página pra reiniciar."
        )
    else:
        st.caption(
            "As opções abaixo são só o que falta — incluindo tipos que a "
            "gente não tem como confirmar se existem hoje (Centro Cultural, "
            "Oficina Itinerante), mas que valem como pedido de qualquer jeito."
        )
        opcoes_faltantes = categorias_faltantes(df, municipio_cidadao)
        categoria_escolhida = st.radio(
            "Escolha uma opção", opcoes_faltantes, label_visibility="collapsed"
        )

        col_botao, _ = st.columns([1, 3])
        with col_botao:
            se_registrou = st.button(
                "Registrar meu pedido",
                icon=":material/how_to_vote:",
                type="primary",
                use_container_width=True,
            )
        if se_registrou:
            registrar_pedido(municipio_cidadao, categoria_escolhida)
            st.success(
                f"Pedido registrado: {categoria_escolhida} em {municipio_cidadao}!"
            )
            st.rerun()

    st.write("")

    # --------------------------------------------------------------
    # Contador público
    # --------------------------------------------------------------
    total_local = total_pedidos(municipio_cidadao)
    categoria_top, votos_top = categoria_mais_pedida(municipio_cidadao)

    if total_local > 0:
        st.markdown(
            f"### {votos_top} pessoa{'s' if votos_top != 1 else ''} em "
            f"**{municipio_cidadao}** pede{'m' if votos_top != 1 else ''} "
            f"**{categoria_top}**"
        )
        pedidos_municipio = pedidos_do_municipio(municipio_cidadao)
        tabela_pedidos = pd.DataFrame(
            {"Categoria": list(pedidos_municipio.keys()), "Pedidos": list(pedidos_municipio.values())}
        ).sort_values("Pedidos", ascending=False)
        st.dataframe(
            tabela_pedidos.style.set_properties(**estilo_texto_tabela()),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.markdown(
            estado_vazio(
                "inbox",
                f"Ainda não há pedidos registrados pra {municipio_cidadao} "
                "nesta sessão. Seja o primeiro!",
                cor=COR_DEMANDA,
            ),
            unsafe_allow_html=True,
        )

    st.markdown("##### O que o Ceará está pedindo")
    ranking_geral = ranking_pedidos_ceara()
    if ranking_geral:
        st.dataframe(
            pd.DataFrame(ranking_geral)
            .rename(
                columns={
                    "municipio": "Município",
                    "categoria_mais_pedida": "Mais pedido",
                    "votos_categoria": "Votos no mais pedido",
                    "total_pedidos": "Total de pedidos",
                }
            )
            .style.set_properties(**estilo_texto_tabela()),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("Nenhum pedido registrado ainda em nenhum município.")

    # ------------------------------------------------------------------
    # Feedback — o voto mostra O QUE falta, mas sozinho não garante nada.
    # O feedback dá contexto real: um lugar específico, uma sugestão,
    # uma experiência — fica público, junto do pedido.
    # ------------------------------------------------------------------
    st.divider()
    st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
    st.markdown(
        titulo_secao("message-square", "Deixe um feedback", cor=COR_DEMANDA),
        unsafe_allow_html=True,
    )
    st.caption(
        f"O voto mostra o que falta em {municipio_cidadao}. O feedback "
        "explica **por que** isso importa — sugira um lugar, conte uma "
        "experiência, dê contexto. Isso também fica visível pra quem for "
        "decidir onde investir."
    )
    texto_feedback = st.text_area(
        "Seu feedback",
        placeholder="Ex.: minha cidade tem um casarão histórico abandonado "
        "na praça central que daria um museu ótimo...",
        max_chars=400,
        key="input_feedback",
        label_visibility="collapsed",
    )
    if st.button("Enviar feedback", key="btn_enviar_feedback"):
        if texto_feedback.strip():
            registrar_feedback(
                municipio_cidadao, nome_exibicao(), texto_feedback.strip()
            )
            st.success("Feedback registrado — obrigado por contribuir!")
            st.rerun()
        else:
            st.warning("Escreve alguma coisa antes de enviar.")

    feedbacks_municipio = listar_feedbacks(municipio_cidadao)
    if feedbacks_municipio:
        st.markdown(
            f"##### O que já disseram sobre {municipio_cidadao} "
            f"({len(feedbacks_municipio)})"
        )
        for fb in reversed(feedbacks_municipio[-5:]):
            st.markdown(f"> **{fb['apelido']}:** {fb['texto']}")

    # ------------------------------------------------------------------
    # Teaser do Perfil — conquistas e progresso moraram aqui antes, agora
    # ficam no Perfil (acessível a qualquer pessoa, sem senha)
    # ------------------------------------------------------------------
    st.divider()
    st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
    n_desbloqueadas, n_total_conquistas = resumo_conquistas(df)
    explorados, total_municipios, fracao = progresso_exploracao()
    col_teaser, col_btn_perfil = st.columns([3, 1])
    with col_teaser:
        st.markdown(
            f"**{n_desbloqueadas} de {n_total_conquistas} conquistas** "
            f"desbloqueadas · **{explorados} de {total_municipios} "
            "municípios** explorados nesta sessão"
        )
        st.progress(fracao)
    with col_btn_perfil:
        if st.button(
            "Ver meu Perfil →",
            key="btn_ir_perfil_demanda",
            use_container_width=True,
        ):
            abrir_perfil()

    with st.expander("Como esse pedido se conecta com o resto do app", icon=":material/help:"):
        st.markdown(
            "1. **Índice de Prioridade** (Painel do Gestor): cada pedido "
            "adiciona um peso pequeno e suave (raiz quadrada do total de "
            "pedidos) ao índice do município — dá pra ver a versão "
            "ajustada na página 'Municípios Prioritários'.\n"
            "2. **Simulador de Investimento**: ao clicar num município que "
            "já tem pedidos registrados, o simulador sugere automaticamente "
            "simular o tipo de equipamento mais pedido pela população "
            "dali (quando esse tipo for simulável — museu, teatro ou "
            "cinema).\n\n"
            "Tudo isso é calculado só com os pedidos desta sessão do "
            "navegador — reinicia ao recarregar a página, mesma decisão "
            "de escopo do resto do protótipo."
        )


# ========================================================================
# MODO 3 — SIMULADOR DE INVESTIMENTO
# ========================================================================
elif st.session_state.modo_app == MODOS[2]:
    st.markdown(barra_secao(COR_SIMULADOR), unsafe_allow_html=True)
    st.markdown(
        "### Onde investir pra reduzir o deserto cultural?\n"
        "Escolha um tipo de equipamento e um raio de atuação na barra "
        "lateral, depois **clique num município no mapa** — o sistema "
        "calcula quantas pessoas passariam a ter acesso cultural e o "
        "quanto isso reduz o déficit da mesorregião."
    )
    _render_resumo(resumo_simulador(), key="resumo_simulador")

    col_tipo, col_raio = st.columns([1.3, 1])
    with col_tipo:
        tipo_label = st.selectbox(
            "Tipo de equipamento a simular",
            list(TIPOS_EQUIPAMENTO.values()),
            key="sel_tipo_equipamento",
        )
    coluna_equipamento = next(
        k for k, v in TIPOS_EQUIPAMENTO.items() if v == tipo_label
    )
    with col_raio:
        raio_km = st.slider(
            "Raio de atuação (km)",
            min_value=5,
            max_value=100,
            value=20,
            help="Distância que o equipamento consegue atender — quem mora "
            "dentro desse raio passa a ser considerado 'com acesso'",
        )

    st.caption(
        f"Azul = município já tem {tipo_label.lower()} · Terracota = "
        "🏜️ Deserto Cultural para esse equipamento. Clique num ponto do mapa."
    )

    evento_mapa = st.plotly_chart(
        mapa_simulador(
            df, coluna_equipamento, altura=600, rotulo_equipamento=tipo_label
        ),
        on_select="rerun",
        selection_mode="points",
        key="mapa_simulador_plot",
        use_container_width=True,
    )

    municipio_clicado = None
    if evento_mapa and evento_mapa.selection and evento_mapa.selection.points:
        ponto = evento_mapa.selection.points[0]
        customdata = ponto.get("customdata")
        if customdata:
            municipio_clicado = customdata[0]
            registrar_exploracao(municipio_clicado)

    if municipio_clicado:
        categoria_pedida, votos_pedidos = categoria_mais_pedida(municipio_clicado)
        if categoria_pedida and categoria_pedida in CATEGORIAS_SIMULAVEIS:
            if categoria_pedida != tipo_label:
                col_sugestao, col_botao = st.columns([3, 1])
                with col_sugestao:
                    st.info(
                        f"A população de **{municipio_clicado}** pediu "
                        f"**{categoria_pedida}** ({votos_pedidos} "
                        f"pedido{'s' if votos_pedidos != 1 else ''}) em "
                        "'Demanda Cidadã' — quer simular isso?"
                    )
                with col_botao:
                    if st.button(
                        f"Simular {categoria_pedida}", use_container_width=True
                    ):
                        st.session_state["sel_tipo_equipamento"] = categoria_pedida
                        st.rerun()
        elif categoria_pedida:
            st.caption(
                f"A população de {municipio_clicado} pediu mais "
                f"'{categoria_pedida}' em 'Demanda Cidadã', mas esse "
                "tipo ainda não é simulável nesta versão (só museu, "
                "teatro e cinema)."
            )

    st.divider()

    if municipio_clicado:
        resultado = calcular_simulacao(df, municipio_clicado, coluna_equipamento, raio_km)
        with st.container(border=True):
            st.markdown(titulo_secao("piggy-bank", f"Simulação: {tipo_label} em {municipio_clicado}", COR_SIMULADOR), unsafe_allow_html=True)
            populacao_fmt = f"{resultado['populacao_beneficiada']:,}".replace(",", ".")
            st.markdown(
                f"Se um(a) **{tipo_label.lower()}** fosse instalado(a) em "
                f"**{municipio_clicado}**, cerca de **{populacao_fmt} pessoas** "
                f"passariam a ter acesso cultural em menos de **{raio_km} km**, "
                f"reduzindo o déficit de {tipo_label.lower()} na mesorregião "
                f"**{resultado['mesorregiao']}** em "
                f"**{resultado['reducao_relativa']:.0f}%**."
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("População beneficiada", populacao_fmt)
            c2.metric(
                "Municípios que passam a ter acesso",
                resultado["n_municipios_beneficiados"],
            )
            c3.metric(
                "Redução do déficit na mesorregião",
                f"{resultado['reducao_relativa']:.0f}%",
            )
            if resultado["municipios_beneficiados"]:
                st.caption(
                    "Municípios beneficiados: "
                    + ", ".join(resultado["municipios_beneficiados"])
                )
    else:
        st.markdown(
            estado_vazio(
                "mouse-pointer-click",
                "Clique em um ponto do mapa para rodar a simulação.",
                cor=COR_SIMULADOR,
            ),
            unsafe_allow_html=True,
        )

    with st.expander("Como essa simulação é calculada"):
        st.markdown(
            "1. Ao clicar num município, calculamos a **distância real** "
            "(fórmula de haversine, mesma usada no Feed Cultural) entre "
            "ele e todos os outros 183 municípios do Ceará.\n"
            "2. Município **dentro do raio escolhido** e que **hoje não "
            "tem** o equipamento selecionado → conta como **beneficiado** "
            "(passaria a ter acesso).\n"
            "3. A **população beneficiada** soma a população de todos "
            "esses municípios (incluindo o próprio alvo, se ele também "
            "não tinha o equipamento).\n"
            "4. A **redução do déficit da mesorregião** compara o % de "
            "municípios sem o equipamento na mesorregião do alvo, antes e "
            "depois de considerar quem passaria a ter acesso."
        )

    st.divider()

    # --------------------------------------------------------------
    # Painel de Transparência do Gestor
    # --------------------------------------------------------------
    st.markdown(titulo_secao("megaphone", "Painel de Transparência do Gestor", COR_SIMULADOR), unsafe_allow_html=True)
    st.markdown(
        "A versão **pública** do Índice de Prioridade: um ranking de fácil "
        "leitura de quais municípios têm o maior deserto cultural do "
        "Ceará — com cards prontos pra baixar e compartilhar. A ideia é "
        "que o mesmo dado usado pra planejamento também vire "
        "**ferramenta de cobrança cívica**, não só de análise interna."
    )
    st.caption(
        "100% dado real — mesmo Índice de Prioridade do Radar Cultural, "
        "sem nenhum valor ilustrativo aqui."
    )

    ranking_publico = montar_ranking_publico(df, n=30)
    _render_resumo(resumo_transparencia(ranking_publico), key="resumo_transparencia")
    st.dataframe(
        ranking_publico.style.set_properties(**estilo_texto_tabela())
        .apply(destacar_coluna, subset=["Índice de Prioridade"])
        .format(
            {
                "Índice de Prioridade": "{:.2f}",
                "Renda per capita (R$, Censo 2022)": "{:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    st.divider()
    st.markdown(
        box_glossario(
            "Por que baixar e compartilhar esse card?",
            "Uma tabela técnica não sai do gabinete do gestor. Um card "
            "pronto pra WhatsApp, Instagram ou uma matéria de jornal, "
            "sim. É o <b>mesmo dado oficial</b> da tabela acima — só que "
            "em formato feito pra circular e virar cobrança pública de "
            "verdade, não só análise interna.",
            cor=COR_SIMULADOR,
        ),
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(
            titulo_secao("share-2", "Gerar card pra compartilhar", COR_SIMULADOR),
            unsafe_allow_html=True,
        )
        municipio_card = st.selectbox(
            "Escolha um município do ranking acima",
            ranking_publico["Município"].tolist(),
        )
        linha_escolhida = ranking_publico.loc[
            ranking_publico["Município"] == municipio_card
        ].iloc[0]

        col_preview, col_info = st.columns([1, 1.3])
        with col_preview:
            card_png = gerar_card_municipio(linha_escolhida, len(ranking_publico))
            st.image(card_png, width=320)
            st.download_button(
                "Baixar card (PNG)",
                icon=":material/download:",
                data=card_png,
                file_name=f"radar_cultural_{municipio_card.lower().replace(' ', '_')}.png",
                mime="image/png",
                use_container_width=True,
            )
        with col_info:
            st.markdown(
                f"**{municipio_card}** é o **{int(linha_escolhida['#'])}º** "
                f"município com maior déficit cultural do ranking (de "
                f"{len(ranking_publico)} analisados).\n\n"
                f"- Mesorregião: {linha_escolhida['Mesorregião']}\n"
                f"- População: {int(linha_escolhida['População']):,}".replace(",", ".")
                + f"\n- Renda per capita: R$ {linha_escolhida['Renda per capita (R$, Censo 2022)']:.2f}\n"
                f"- Equipamentos culturais (museu/teatro/cinema): "
                f"{int(linha_escolhida['Equipamentos (de 3)'])} de 3\n"
                f"- Índice de Prioridade: {linha_escolhida['Índice de Prioridade']:.2f}"
            )
            st.caption(
                "Formato retrato (1080×1350), pronto pra Stories/Instagram/"
                "WhatsApp — qualquer pessoa, jornalista ou vereador pode "
                "baixar e cobrar publicamente."
            )

    with st.expander("Como esse ranking foi feito", icon=":material/help:"):
        st.markdown(
            "Usa exatamente o mesmo **Índice de Prioridade** calculado no "
            "Radar Cultural (ver a explicação completa na página "
            "'Municípios Prioritários' do Painel do Gestor) — nenhum "
            "dado novo ou estimado entra aqui. A diferença é só de "
            "**formato**: em vez de uma tabela técnica, um card visual "
            "pensado pra circular fora do ambiente de gestão — em redes "
            "sociais, grupos de WhatsApp, matérias de jornal local."
        )

    st.divider()
    st.caption(
        "Simulador & Transparência — protótipo. Fórmulas de distância e "
        "impacto, e o ranking do Painel de Transparência, usam dados "
        "reais do Radar Cultural."
    )

# ========================================================================
# MODO 4 — METODOLOGIA
# ========================================================================
else:
    st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
    st.markdown(
        "### Metodologia\n"
        "Tudo que está por trás dos números do Cultura Ceará, num lugar "
        "só: de onde vêm os dados, como o Índice de Prioridade é "
        "calculado, e quais decisões de tratamento tomamos pelo caminho."
    )

    st.markdown(
        box_glossario(
            "Deserto Cultural",
            "Município que <b>não tem nenhum</b> museu, teatro/sala de "
            "espetáculo ou cinema. Biblioteca fica de fora do conceito: "
            "ela existe em <b>99,5% dos 184 municípios cearenses</b> "
            "(só Graça é exceção), então não diferencia quem tem acesso "
            "de quem não tem.",
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------
    st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
    st.markdown(titulo_secao("book-open-check", "Fontes dos dados"), unsafe_allow_html=True)
    st.markdown(
        "| O quê | Fonte | Ano | Situação |\n"
        "|---|---|---|---|\n"
        "| Equipamentos culturais (museu, teatro, cinema, biblioteca) | "
        "IBGE — MUNIC, Suplemento de Cultura | 2021 | Definitivo |\n"
        "| População | IBGE — Censo Demográfico (tabela SIDRA 4714) | "
        "2022 | Definitivo (Universo) |\n"
        "| Renda per capita domiciliar | IBGE — Censo Demográfico "
        "(tabela SIDRA 10295) | 2022 | Preliminar (amostra) |\n"
        "| Mesorregiões e coordenadas | IBGE — malha municipal | — | "
        "Definitivo |\n"
    )
    st.caption(
        "Os 184 municípios do Ceará bateram 100% em todos os cruzamentos, "
        "sem nenhuma linha perdida. Detalhes completos em `data/README.md`."
    )

    st.warning(
        "**Renda per capita é dado preliminar.** O IBGE ainda não fechou "
        "as áreas de ponderação definitivas desse indicador no Censo "
        "2022 — é o dado municipal mais atual disponível, mas pode ser "
        "revisado. A população, por outro lado, já é definitiva.",
        icon=":material/info:",
    )

    st.info(
        "**Não confundir com PIB per capita.** A renda usada aqui é a "
        "**renda domiciliar** — quanto cada pessoa recebe, em média, "
        "somando o que entra na casa dela. O PIB per capita que aparece "
        "no IBGE Cidades é outra coisa: todo o PIB do município "
        "(inclusive gastos públicos, agropecuária e indústria) dividido "
        "pela população. Não é incomum um município ter PIB per capita "
        "alto e renda domiciliar baixa — o que, aliás, é em si um "
        "indicador de desigualdade.",
        icon=":material/lightbulb:",
    )

    # --------------------------------------------------------------
    st.divider()
    st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
    st.markdown(titulo_secao("scale", "Índice de Prioridade"), unsafe_allow_html=True)
    st.markdown(
        "Combina, num número só, os dois fatores que juntos indicam "
        "urgência de atenção: **falta de equipamento cultural** e "
        "**baixa renda**."
    )
    st.latex(
        r"\text{Índice} = (3 - E) \times \left(1 - \frac{R}{R_{max}}\right)"
    )
    st.markdown(
        "- **E** = número de equipamentos \"raros\" que o município tem "
        "(museu, teatro, cinema — de 0 a 3). Biblioteca fica de fora "
        "porque existe em todos os municípios.\n"
        "- **R** = renda per capita do município.\n"
        "- **R₍max₎** = a maior renda per capita do estado (Fortaleza).\n\n"
        "Assim, um município **sem nenhum** desses equipamentos e com "
        "renda **bem abaixo** da capital pontua alto. Um município rico "
        "mesmo sem equipamentos, ou um município pobre mas já bem servido "
        "culturalmente, pontua mais baixo."
    )
    st.markdown(
        "**Ajuste por demanda cidadã:** na página 'Municípios "
        "Prioritários' existe também uma coluna de *Índice Ajustado*, que "
        "soma um peso pequeno vindo dos pedidos registrados na Demanda "
        "Cidadã (raiz quadrada do total de pedidos × 0,05). O índice "
        "original, calculado só com dado oficial, nunca é sobrescrito."
    )

    # --------------------------------------------------------------
    st.divider()
    st.markdown(barra_secao(COR_SIMULADOR), unsafe_allow_html=True)
    st.markdown(
        titulo_secao("map-pinned", "Simulador de Investimento", cor=COR_SIMULADOR),
        unsafe_allow_html=True,
    )
    st.markdown(
        "1. Ao clicar num município, calculamos a **distância real** "
        "(fórmula de Haversine) entre ele e os outros 183 municípios.\n"
        "2. Município **dentro do raio escolhido** que **hoje não tem** o "
        "equipamento → conta como **beneficiado**.\n"
        "3. A **população beneficiada** soma a população desses "
        "municípios.\n"
        "4. A **redução do déficit** compara o % de municípios sem o "
        "equipamento na mesorregião, antes e depois."
    )

    # --------------------------------------------------------------
    st.divider()
    st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
    st.markdown(
        titulo_secao("scale", "Decisões de tratamento de dados", cor=COR_DEMANDA),
        unsafe_allow_html=True,
    )
    st.markdown(
        "- **Biblioteca fora do índice:** existe em 99,5% dos municípios "
        "cearenses (só Graça é exceção), então incluí-la só achataria as "
        "diferenças entre eles. Foi o primeiro achado relevante do "
        "projeto — e continua valendo mesmo depois de atualizar a fonte "
        "de MUNIC 2014 pra MUNIC 2021.\n"
        "- **Anos-base próximos:** equipamentos são de 2021 e "
        "população/renda de 2022 — só 1 ano de diferença, bem mais "
        "coerente que a versão anterior (2014 x 2010).\n"
        "- **Grafia de municípios:** dois municípios têm nome grafado "
        "diferente entre as bases (Ereré/Ererê e Itapajé/Itapagé) — "
        "foram normalizados pra não perder o cruzamento.\n"
        "- **Dados de sessão:** pedidos da Demanda Cidadã e conquistas "
        "ficam só no navegador e somem ao recarregar. É decisão de "
        "escopo do protótipo, não limitação técnica."
    )

    # --------------------------------------------------------------
    st.divider()
    st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
    st.markdown(titulo_secao("landmark", "ODS trabalhados"), unsafe_allow_html=True)
    ods_cols = st.columns(3)
    ods_lista = [
        ("ODS 4", "Educação de qualidade", COR_GESTOR, COR_GESTOR_CLARO),
        ("ODS 10", "Redução das desigualdades", COR_DEMANDA, COR_DEMANDA_CLARO),
        ("ODS 11", "Cidades e comunidades sustentáveis", COR_SIMULADOR, COR_SIMULADOR_CLARO),
    ]
    for col, (numero, texto, cor, cor_clara) in zip(ods_cols, ods_lista):
        with col:
            st.markdown(
                cartao_hero("landmark", numero, texto, cor, cor_clara),
                unsafe_allow_html=True,
            )

    st.divider()
    st.caption(
        "Fontes: IBGE — Pesquisa de Informações Básicas Municipais (MUNIC), "
        "Suplemento de Cultura 2021 · IBGE — Censo Demográfico 2022 "
        "(população e renda per capita municipal)."
    )

# Link de acesso à Metodologia — fica colado no rodapé de propósito: é
# informação de apoio (fontes, fórmulas), não uma das 3 features
# principais, então não compete por atenção lá em cima com os cards hero.
st.markdown(marcador("link-metodologia"), unsafe_allow_html=True)
_col_esq, _col_meio, _col_dir = st.columns([1, 1, 1])
with _col_meio:
    _na_metodologia = st.session_state.modo_app == MODOS[3]
    st.button(
        "Você está na Metodologia" if _na_metodologia else "Metodologia e fontes dos dados",
        key="btn_metodologia",
        use_container_width=True,
        on_click=ir_para_modo,
        args=(MODOS[3],),
    )

st.markdown(rodape_app(), unsafe_allow_html=True)