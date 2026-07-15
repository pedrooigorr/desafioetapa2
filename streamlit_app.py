"""
Radar Cultural — Squad ZeroKai
Desafio dos Dados VIVO 2026 — Etapa 2

Dashboard de equidade no acesso a equipamentos culturais nos 184 municípios
do Ceará, cruzando população, renda per capita e presença de museus,
teatros/salas de espetáculo, cinemas e bibliotecas.

Este arquivo só monta a página. A lógica de dados está em
src/data_loader.py, a lógica de gráficos está em src/charts.py e a paleta
de cores está em src/theme.py.
"""

import streamlit as st

from src.charts import (
    grafico_equidade_por_mesorregiao,
    grafico_presenca_equipamentos,
    mapa_municipios,
)
from src.data_loader import (
    EQUIPAMENTOS,
    aplicar_filtros,
    carregar_dados,
    montar_tabela_prioritarios,
)
from src.theme import CSS_CUSTOMIZADO, destacar_coluna, estilo_texto_tabela

st.set_page_config(
    page_title="Radar Cultural — ZeroKai",
    page_icon="🎭",
    layout="wide",
)

st.markdown(CSS_CUSTOMIZADO, unsafe_allow_html=True)

PAGINAS = [
    "📊 Visão Geral",
    "🗺️ Mapa do Ceará",
    "🏛️ Presença de Equipamentos",
    "📈 Equidade por Mesorregião",
    "🚩 Municípios Prioritários",
]

if "pagina" not in st.session_state:
    st.session_state.pagina = PAGINAS[0]


def ir_para(pagina: str):
    st.session_state.pagina = pagina


df = carregar_dados()

# ----------------------------------------------------------------------
# Cabeçalho
# ----------------------------------------------------------------------
st.title("🎭 Radar Cultural — Ceará")
st.markdown("##### Squad ZeroKai · Desafio dos Dados VIVO 2026 · ODS 10 e ODS 11")

with st.expander("ℹ️ Sobre os dados exibidos"):
    st.markdown(
        "- **Equipamentos culturais** (museu, teatro/sala de espetáculo, "
        "cinema, biblioteca): IBGE, Pesquisa de Informações Básicas "
        "Municipais (MUNIC), Suplemento de Cultura **2014**.\n"
        "- **População e renda per capita**: Atlas Brasil (PNUD/IPEA/FJP), "
        "referentes ao **Censo 2010**.\n\n"
        "Como as duas fontes têm anos-base diferentes, os números "
        "absolutos de população podem estar desatualizados, mas o "
        "**padrão de desigualdade** entre municípios se mantém coerente. "
        "Ver `data/README.md` para detalhes de como as bases foram cruzadas."
    )

# ----------------------------------------------------------------------
# Filtros (sidebar)
# ----------------------------------------------------------------------
st.sidebar.header("Filtros")

mesorregioes_sel = st.sidebar.multiselect(
    "Mesorregião",
    sorted(df["mesorregiao"].unique()),
    default=sorted(df["mesorregiao"].unique()),
)

excluir_fortaleza = st.sidebar.checkbox(
    "Excluir Fortaleza da análise",
    value=False,
    help="Fortaleza concentra grande parte da população e dos equipamentos "
    "— desmarque para ver só o padrão do interior",
)

pop_min, pop_max = int(df["populacao"].min()), int(df["populacao"].max())
faixa_pop = st.sidebar.slider("Faixa de população", pop_min, pop_max, (pop_min, pop_max))

equip_filtro = st.sidebar.multiselect(
    "Mostrar apenas municípios SEM:",
    options=list(EQUIPAMENTOS.values()),
    default=[],
    help="Selecione um ou mais equipamentos para ver só quem não tem",
)

df_f = aplicar_filtros(
    df,
    mesorregioes=mesorregioes_sel,
    faixa_populacao=faixa_pop,
    excluir_fortaleza=excluir_fortaleza,
    equipamentos_ausentes=equip_filtro,
)

# ----------------------------------------------------------------------
# Navbar
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# KPIs (aparecem em todas as páginas, dão contexto rápido)
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Conteúdo — Visão Geral (painéis compactos) ou página dedicada
# ----------------------------------------------------------------------
pagina_atual = st.session_state.pagina

if pagina_atual == "📊 Visão Geral":
    st.markdown(
        "### Bem-vindo(a) ao Radar Cultural! 👋\n"
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

    linha1_a, linha1_b = st.columns(2)
    with linha1_a:
        with st.container(border=True):
            st.subheader("🗺️ Mapa do Ceará")
            st.plotly_chart(
                mapa_municipios(df_f, altura=280),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.button(
                "Ver página completa →",
                key="btn_mapa",
                on_click=ir_para,
                args=("🗺️ Mapa do Ceará",),
            )

    with linha1_b:
        with st.container(border=True):
            st.subheader("🏛️ Presença de Equipamentos")
            st.plotly_chart(
                grafico_presenca_equipamentos(df_f, altura=260),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.button(
                "Ver página completa →",
                key="btn_presenca",
                on_click=ir_para,
                args=("🏛️ Presença de Equipamentos",),
            )

    linha2_a, linha2_b = st.columns(2)
    with linha2_a:
        with st.container(border=True):
            st.subheader("📈 Equidade por Mesorregião")
            st.plotly_chart(
                grafico_equidade_por_mesorregiao(df_f, altura=280),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.button(
                "Ver página completa →",
                key="btn_equidade",
                on_click=ir_para,
                args=("📈 Equidade por Mesorregião",),
            )

    with linha2_b:
        with st.container(border=True):
            st.subheader("🚩 Municípios Prioritários")
            tabela_preview = montar_tabela_prioritarios(df_f, n=5)
            st.dataframe(
                tabela_preview.style.set_properties(**estilo_texto_tabela())
                .apply(destacar_coluna, subset=["Índice de Prioridade"])
                .format(
                    {
                        "Índice de Prioridade": "{:.2f}",
                        "Renda per capita (R$)": "{:.2f}",
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
                args=("🚩 Municípios Prioritários",),
            )

elif pagina_atual == "🗺️ Mapa do Ceará":
    st.subheader("🗺️ Mapa do Ceará — renda e população por município")
    st.caption(
        "Cada ponto é um município — o tamanho indica a população e a cor "
        "indica a renda per capita. Passe o mouse para ver detalhes, "
        "incluindo o número de equipamentos culturais."
    )
    st.plotly_chart(mapa_municipios(df_f, altura=680), use_container_width=True)

    with st.expander("🔍 Como esse mapa foi feito"):
        st.markdown(
            "1. Pegamos o **contorno oficial do Ceará** (fronteira do "
            "estado) e as coordenadas (latitude/longitude) dos 184 "
            "municípios.\n"
            "2. Em vez de usar um mapa de fundo tradicional (que sempre "
            "mostraria os estados vizinhos), desenhamos **só a forma do "
            "Ceará** preenchida, com o restante do mundo em branco — assim "
            "o foco fica 100% no estado.\n"
            "3. Cada ponto representa um município — o **tamanho** é "
            "proporcional à **população** e a **cor** é proporcional à "
            "**renda per capita** (quanto mais forte o terracota, maior a "
            "renda).\n\n"
            "**Por que um mapa em vez de uma tabela?** Fica muito mais "
            "fácil enxergar de cara o padrão geográfico: renda mais alta "
            "concentrada perto de Fortaleza e do litoral, caindo conforme "
            "se afasta para o interior/sertão."
        )

elif pagina_atual == "🏛️ Presença de Equipamentos":
    st.subheader("🏛️ Presença de cada equipamento cultural")
    st.caption(
        "% dos municípios filtrados que possuem cada tipo de equipamento "
        "cultural."
    )
    st.plotly_chart(
        grafico_presenca_equipamentos(df_f, altura=680), use_container_width=True
    )

    with st.expander("🔍 Como esse gráfico foi feito"):
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

elif pagina_atual == "📈 Equidade por Mesorregião":
    st.subheader("🗺️ Equidade cultural por Mesorregião")
    st.caption(
        "% de municípios sem museu, teatro ou cinema em cada mesorregião — "
        "a cor mostra a renda média per capita da região."
    )
    st.plotly_chart(
        grafico_equidade_por_mesorregiao(df_f, altura=680), use_container_width=True
    )

    with st.expander("🔍 Como esse gráfico foi feito"):
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

elif pagina_atual == "🚩 Municípios Prioritários":
    st.subheader("🚩 Municípios prioritários (baixa renda + pouco acesso)")
    st.caption(
        "Ranking pelo Índice de Prioridade: combina ausência de museu, "
        "teatro ou cinema com baixa renda per capita — quanto maior, mais "
        "urgente a atenção."
    )
    n_linhas = st.slider(
        "Quantos municípios mostrar", min_value=10, max_value=len(df_f), value=min(30, len(df_f))
    )
    tabela_completa = montar_tabela_prioritarios(df_f, n=n_linhas)
    st.dataframe(
        tabela_completa.style.set_properties(**estilo_texto_tabela())
        .apply(destacar_coluna, subset=["Índice de Prioridade"])
        .format(
            {"Índice de Prioridade": "{:.2f}", "Renda per capita (R$)": "{:.2f}"}
        ),
        use_container_width=True,
        hide_index=True,
        height=650,
    )

    with st.expander("🔍 Como esse ranking foi feito"):
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
            "**merece atenção prioritária**."
        )

st.divider()
st.caption(
    "Fontes: IBGE — Pesquisa de Informações Básicas Municipais (MUNIC), "
    "Suplemento de Cultura 2014 · Atlas Brasil (PNUD/IPEA/FJP) — "
    "população e renda per capita municipal, Censo 2010."
)