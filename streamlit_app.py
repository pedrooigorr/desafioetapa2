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
    inicializar_pedidos,
    ja_votou_no_municipio,
    pedidos_do_municipio,
    peso_demanda,
    ranking_pedidos_ceara,
    registrar_pedido,
    total_pedidos,
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
    COR_SIMULADOR,
    COR_SIMULADOR_CLARO,
    CSS_CUSTOMIZADO,
    barra_secao,
    cabecalho_app,
    cartao_hero,
    destacar_coluna,
    estilo_texto_tabela,
    rodape_app,
)
from src.transparencia import gerar_card_municipio, montar_ranking_publico

st.set_page_config(
    page_title="Radar Cultural — ZeroKai",
    layout="wide",
)

st.markdown(CSS_CUSTOMIZADO, unsafe_allow_html=True)

inicializar_pedidos()
inicializar_preferencias()

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


st.markdown(cabecalho_app(), unsafe_allow_html=True)
st.markdown(
    "Três jeitos de olhar pra um mesmo problema: **quem no Ceará tem acesso "
    "a cultura perto de casa — e quem não tem.** Escolha por onde começar"
)
renderizar_controles_topo()

CARDS_HERO = [
    {
        "modo": MODOS[0],
        "titulo": "Painel do Gestor",
        "texto": (
            "O raio-x da desigualdade cultural: cruza dados oficiais de "
            "população, renda e equipamentos culturais nos 184 municípios "
            "pra mostrar onde a cultura está concentrada e onde ela quase "
            "não chega. Feito pra quem decide política pública."
        ),
        "cor": COR_GESTOR,
        "cor_clara": COR_GESTOR_CLARO,
    },
    {
        "modo": MODOS[1],
        "titulo": "Demanda Cidadã",
        "texto": (
            "A voz de quem mora lá: escolha seu município, veja o que já "
            "existe e registre o que mais falta. Seu pedido vira contagem "
            "pública e pesa de verdade no ranking de prioridades."
        ),
        "cor": COR_DEMANDA,
        "cor_clara": COR_DEMANDA_CLARO,
    },
    {
        "modo": MODOS[2],
        "titulo": "Simulador & Transparência",
        "texto": (
            "Simule o impacto de instalar um museu, teatro ou cinema antes "
            "de construir — e gere cards prontos pra baixar e cobrar "
            "publicamente investimento nos municípios mais esquecidos."
        ),
        "cor": COR_SIMULADOR,
        "cor_clara": COR_SIMULADOR_CLARO,
    },
]

hero_cols = st.columns(3)
for col, card in zip(hero_cols, CARDS_HERO):
    with col:
        st.markdown(
            cartao_hero(
                card["titulo"], card["texto"], card["cor"], card["cor_clara"],
            ),
            unsafe_allow_html=True,
        )
        esta_aqui = st.session_state.modo_app == card["modo"]
        col_btn, col_ouvir = st.columns([5, 1])
        with col_btn:
            st.button(
                "✓ Você está aqui" if esta_aqui else f"Abrir {card['titulo']} →",
                key=f"hero_btn_{card['titulo']}",
                use_container_width=True,
                type="primary" if esta_aqui else "secondary",
                on_click=ir_para_modo,
                args=(card["modo"],),
            )
        with col_ouvir:
            botao_ouvir(
                f"{card['titulo']}. {card['texto']}",
                key=f"hero_ouvir_{card['titulo']}",
                rotulo="Ouvir",
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
    with st.expander("Sobre os dados exibidos"):
        st.markdown(
            "- **Equipamentos culturais** (museu, teatro/sala de espetáculo, "
            "cinema, biblioteca): IBGE, Pesquisa de Informações Básicas "
            "Municipais (MUNIC), Suplemento de Cultura **2014**.\n"
            "- **População e renda per capita**: Atlas Brasil (PNUD/IPEA/FJP), "
            "referentes ao **Censo 2010**.\n\n"
            "Como as duas fontes têm anos-base diferentes, os números "
            "absolutos de população podem estar desatualizados, mas o "
            "**padrão de desigualdade** entre municípios se mantém coerente. "
            "Ver `data/README.md` para detalhes de como as bases foram cruzadas.\n\n"
            "**Atenção, não confundir:** a 'Renda per capita' usada aqui é a "
            "**renda domiciliar** — quanto cada pessoa recebe, em média, "
            "somando a renda de todo mundo em casa (Censo 2010). É **diferente** "
            "do **PIB per capita** que aparece no IBGE Cidades (todo o "
            "PIB do município — inclusive gastos públicos, agropecuária, "
            "indústria — dividido pela população, ano mais recente). São "
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

    with st.expander(rotulo_filtros, expanded=False):
        col_titulo, col_limpar = st.columns([4, 1])
        with col_titulo:
            st.caption("Ajuste o recorte de municípios usado em todos os gráficos abaixo.")
        with col_limpar:
            st.button(
                "Limpar filtros",
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

    st.divider()

    # --------------------------------------------------------------
    # KPIs
    # --------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Municípios analisados", f"{len(df_f):,}".replace(",", "."))
    c2.metric(
        "Sem museu, teatro nem cinema",
        f"{(df_f['n_equipamentos_raros'] == 0).sum():,}".replace(",", "."),
        help="Biblioteca não entra aqui — praticamente todos os municípios do "
        "Ceará já têm uma, então ela não ajuda a distinguir quem tem acesso "
        "cultural de quem não tem",
    )
    pct_sem_museu = 100 * (~df_f["tem_museu"]).mean() if len(df_f) else 0
    c3.metric("% sem museu", f"{pct_sem_museu:.1f}%")
    pop_desassistida = df_f.loc[df_f["n_equipamentos_raros"] == 0, "populacao"].sum()
    c4.metric(
        "População sem museu, teatro ou cinema por perto",
        f"{pop_desassistida:,.0f}".replace(",", "."),
    )

    st.divider()

    # --------------------------------------------------------------
    # Conteúdo — Visão Geral (painéis compactos) ou página dedicada
    # --------------------------------------------------------------
    pagina_atual = st.session_state.pagina

    if pagina_atual == "Visão Geral":
        st.markdown(
            "### Bem-vindo(a) ao Radar Cultural!\n"
            "Este painel nasceu de uma pergunta simples: **quem no Ceará tem "
            "acesso a museu, teatro ou cinema perto de casa — e quem não tem?** "
            "Cruzamos dados oficiais de população, renda e equipamentos "
            "culturais dos 184 municípios cearenses para mostrar, de forma "
            "visual, onde a cultura está concentrada e onde ela quase não "
            "chega.\n\n"
            "A ideia é ajudar gestores públicos, organizações culturais e "
            "qualquer pessoa curiosa a **enxergar essa desigualdade e decidir "
            "com mais clareza onde investir**. Use os filtros à esquerda para "
            "explorar por mesorregião, faixa de população ou tipo de "
            "equipamento — e navegue pelas abas acima para se aprofundar em "
            "cada análise."
        )
        st.caption(
            "Prévia de todas as análises abaixo. Clique em um card ou na "
            "navbar acima para abrir a visão completa e maior de cada uma — "
            "lá você também encontra a explicação de como cada uma foi feita."
        )
        _render_resumo(resumo_visao_geral(df_f), key="resumo_visao_geral")

        linha1_a, linha1_b = st.columns(2)
        with linha1_a, st.container(border=True):
            st.markdown(barra_secao(COR_GESTOR), unsafe_allow_html=True)
            st.subheader("Mapa do Ceará")
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
            st.subheader("Presença de Equipamentos")
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
            st.subheader("Equidade por Mesorregião")
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
            st.subheader("Municípios Prioritários")
            tabela_preview = montar_tabela_prioritarios(df_f, n=5)
            st.dataframe(
                tabela_preview.style.set_properties(**estilo_texto_tabela())
                .apply(destacar_coluna, subset=["Índice de Prioridade"])
                .format(
                    {
                        "Índice de Prioridade": "{:.2f}",
                        "Renda per capita (R$, Censo 2010)": "{:.2f}",
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
        st.subheader("Mapa do Ceará — renda e população por município")
        st.caption(
            "Cada ponto é um município — o tamanho indica a população e a cor "
            "indica a renda per capita. Passe o mouse para ver detalhes, "
            "incluindo o número de equipamentos culturais."
        )
        _render_resumo(resumo_mapa(df_f), key="resumo_mapa")
        st.plotly_chart(mapa_municipios(df_f, altura=680), use_container_width=True)

        with st.expander("Como esse mapa foi feito"):
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
        st.subheader("Presença de cada equipamento cultural")
        st.caption(
            "% dos municípios filtrados que possuem cada tipo de equipamento "
            "cultural."
        )
        _render_resumo(resumo_presenca_equipamentos(df_f), key="resumo_presenca")
        st.plotly_chart(
            grafico_presenca_equipamentos(df_f, altura=680), use_container_width=True
        )

        with st.expander("Como esse gráfico foi feito"):
            st.markdown(
                "Para cada um dos 4 equipamentos (museu, teatro/sala de "
                "espetáculo, cinema e biblioteca), calculamos:\n\n"
                "`% = (nº de municípios filtrados que têm o equipamento) "
                "÷ (total de municípios filtrados) × 100`\n\n"
                "Os dados de existência de cada equipamento vêm da MUNIC/IBGE "
                "2014, respondida pela própria prefeitura de cada município. "
                "**Achado curioso:** biblioteca aparece em 100% dos municípios "
                "— por isso ela não é usada nas análises de equidade e "
                "prioridade mais à frente, já que não ajuda a diferenciar "
                "quem tem acesso cultural de quem não tem."
            )

    elif pagina_atual == "Equidade por Mesorregião":
        st.markdown(barra_secao(COR_DEMANDA), unsafe_allow_html=True)
        st.subheader("Equidade cultural por Mesorregião")
        st.caption(
            "% de municípios sem museu, teatro ou cinema em cada mesorregião — "
            "a cor mostra a renda média per capita da região."
        )
        _render_resumo(resumo_equidade_mesorregiao(df_f), key="resumo_equidade")
        st.plotly_chart(
            grafico_equidade_por_mesorregiao(df_f, altura=680), use_container_width=True
        )

        with st.expander("Como esse gráfico foi feito"):
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
        st.subheader("Municípios prioritários (baixa renda + pouco acesso)")
        st.caption(
            "Ranking pelo Índice de Prioridade: combina ausência de museu, "
            "teatro ou cinema com baixa renda per capita — quanto maior, mais "
            "urgente a atenção."
        )
        _render_resumo(resumo_municipios_prioritarios(df_f), key="resumo_prioritarios")
        n_linhas = st.slider(
            "Quantos municípios mostrar",
            min_value=10,
            max_value=len(df_f),
            value=min(30, len(df_f)),
        )
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
                    "Renda per capita (R$, Censo 2010)": "{:.2f}",
                    "Índice Ajustado (c/ demanda)": "{:.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
            height=650,
        )

        with st.expander("Como esse ranking foi feito"):
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
        "Suplemento de Cultura 2014 · Atlas Brasil (PNUD/IPEA/FJP) — "
        "população e renda per capita municipal, Censo 2010."
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
    linha_municipio = df.loc[df["municipio"] == municipio_cidadao].iloc[0]

    st.markdown(f"##### O que {municipio_cidadao} já tem")
    existentes = categorias_existentes(df, municipio_cidadao)
    cols_existentes = st.columns(4)
    for col, (categoria, _coluna) in zip(cols_existentes, MAPA_CATEGORIA_COLUNA.items()):
        with col:
            tem = categoria in existentes
            cor = "#4C6444" if tem else "#C1440E"
            simbolo = "✓" if tem else "✗"
            st.markdown(
                f'<div style="text-align:center; padding:14px; border-radius:12px; '
                f'background:{cor}; color:#FFFDF8; font-weight:700;">'
                f"{simbolo}<br>{categoria}</div>",
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
                "Registrar meu pedido", type="primary", use_container_width=True
            )
        if se_registrou:
            registrar_pedido(municipio_cidadao, categoria_escolhida)
            st.success(
                f"Pedido registrado: {categoria_escolhida} em {municipio_cidadao}!"
            )
            st.rerun()

    st.divider()

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
        st.info(
            f"Ainda não há pedidos registrados pra {municipio_cidadao} "
            "nesta sessão. Seja o primeiro!"
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

    with st.expander("Como esse pedido se conecta com o resto do app"):
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
else:
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
        f"verde = município já tem {tipo_label.lower()} · terracota = "
        "deserto cultural para esse equipamento. Clique num ponto do mapa."
    )

    evento_mapa = st.plotly_chart(
        mapa_simulador(df, coluna_equipamento, altura=600),
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
            st.subheader(f"Simulação: {tipo_label} em {municipio_clicado}")
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
        st.info("Clique em um ponto do mapa para rodar a simulação.")

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
    st.subheader("Painel de Transparência do Gestor")
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
                "Renda per capita (R$, Censo 2010)": "{:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    st.markdown("##### Gerar card pra compartilhar")
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
            + f"\n- Renda per capita: R$ {linha_escolhida['Renda per capita (R$, Censo 2010)']:.2f}\n"
            f"- Equipamentos culturais (museu/teatro/cinema): "
            f"{int(linha_escolhida['Equipamentos (de 3)'])} de 3\n"
            f"- Índice de Prioridade: {linha_escolhida['Índice de Prioridade']:.2f}"
        )
        st.caption(
            "Formato retrato (1080×1350), pronto pra Stories/Instagram/"
            "WhatsApp — o objetivo é que qualquer pessoa, jornalista ou "
            "vereador possa baixar e cobrar publicamente."
        )

    with st.expander("Como esse ranking foi feito"):
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

st.markdown(rodape_app(), unsafe_allow_html=True)