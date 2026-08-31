# 🎭 Radar Cultural

**Quem no Ceará tem acesso a museu, teatro ou cinema perto de casa — e quem não tem?**

Um painel de dados que cruza informações oficiais de população, renda e
equipamentos culturais dos 184 municípios do Ceará, pra mostrar onde a
cultura está concentrada e onde ela quase não chega — e transformar isso
em ferramenta de decisão, de voz cidadã e de cobrança pública.

Squad **ZeroKai** · Desafio dos Dados VIVO 2026 · ODS 4, 10 e 11

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://radar-cultural-gzekaz2ty8a.streamlit.app/)

---

## ✨ O projeto

O Ceará tem 184 municípios, mas o acesso à cultura está longe de estar
distribuído de forma equilibrada entre eles. O **Radar Cultural** nasceu
de uma pergunta simples — quem tem acesso a museu, teatro ou cinema perto
de casa, e quem não tem — e virou quatro seções complementares,
construídas em cima do mesmo dado real.

### 👨‍💼 Painel do Gestor
O raio-x da desigualdade cultural: mapa interativo, gráficos de presença
de equipamentos, equidade por mesorregião e um ranking de municípios
prioritários — cruzando dados oficiais de população, renda e
equipamentos culturais. Feito pra quem decide política pública.

### 🗳️ Demanda Cidadã
A voz de quem mora lá: o cidadão escolhe seu município, vê o que já
existe e registra o que mais gostaria de ver. Cada pedido vira contagem
pública, pesa de verdade no ranking de prioridades do Painel do Gestor e
alimenta um mural de feedback (comentário + like/dislike + resposta) por
município.

### 💰 Simulador & Transparência
Simula o impacto de instalar um museu, teatro ou cinema num município
antes de construir — e gera cards prontos (formato Stories/Instagram)
pra baixar e cobrar publicamente investimento nos municípios com maior
deserto cultural.

### 📖 Metodologia
Fontes de dados, a fórmula do Índice de Prioridade e as decisões de
tratamento de dados, tudo num lugar só — pra quem for avaliar o projeto
não precisar garimpar essa informação espalhada pelo app.

## 🕹️ Gamificação e acessibilidade

Duas camadas transversais, presentes nas 4 seções acima:

- **Gamificação** (`src/gamificacao.py`) — perfil leve (apelido + avatar
  ou foto, sem senha), progresso de exploração ("já visitou X de 184
  municípios") e 6 conquistas desbloqueadas por uso do app.
- **Acessibilidade** (`src/acessibilidade.py`) — alto contraste, tamanho
  de texto ajustável, leitura em voz alta (Web Speech API do navegador)
  e **4 modos de cor para daltonismo** (Protanopia/Protanomalia,
  Deuteranopia/Deuteranomalia, Tritanopia/Tritanomalia), que trocam as
  cores das 3 features, do mapa e dos gráficos por paletas seguras pra
  cada tipo — sem precisar recarregar a página.

## 🗺️ Fontes dos dados

- **IBGE** — MUNIC, Suplemento de Cultura 2021 (equipamentos culturais)
- **IBGE** — Censo Demográfico 2022 (população e renda per capita)

Os detalhes de como as bases foram cruzadas, as decisões de tratamento de
dados e um achado interessante (biblioteca existe em 99,5% dos
municípios cearenses, por isso fica de fora do Índice de Prioridade)
estão documentados em [`data/README.md`](data/README.md).

## 🛠️ Stack técnico

- **Python 3.14**
- **uv** — gerenciador de dependências
- **Streamlit** — framework da aplicação
- **Pandas** — carregamento e tratamento dos dados
- **Plotly** (Express + Graph Objects) — todas as visualizações
- **OpenStreetMap** — tiles do mapa interativo
- **Pillow (PIL)** — geração dos cards PNG compartilháveis e das fotos de perfil
- CSS customizado (injetado via Streamlit) — identidade visual própria, com
  paletas alternativas para os 4 modos de acessibilidade a cores

## 🚀 Como rodar localmente

Pré-requisito: ter o [`uv`](https://docs.astral.sh/uv/) instalado.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/pedrooigorr/desafioetapa2.git
   cd desafioetapa2
   ```

2. Sincronize as dependências:

   ```bash
   uv sync
   ```

3. Rode o app:

   ```bash
   uv run streamlit run streamlit_app.py
   ```

O app abre em `http://localhost:8501`.

> Também dá pra abrir o projeto direto no **GitHub Codespaces** — o
> `.devcontainer` já vem configurado pra instalar tudo e subir o app
> automaticamente.

## 📁 Estrutura do projeto

```
.
├── .devcontainer/       # Configuração do GitHub Codespaces
├── .github/             # CODEOWNERS, Dependabot
├── .streamlit/          # Tema visual do app (config.toml)
├── assets/
│   └── fonts/           # Fonte Inter (suporte a acentuação nos cards PNG)
├── data/
│   ├── radar_cultural_ce.csv   # Base de dados combinada (184 municípios)
│   └── README.md               # Como os dados foram cruzados
├── src/
│   ├── acessibilidade.py       # Alto contraste, tamanho de texto, voz, daltonismo
│   ├── ceara_boundary.py       # Contorno geográfico oficial do Ceará
│   ├── charts.py               # Construção dos gráficos Plotly
│   ├── data_loader.py          # Carregamento e cálculo do Índice de Prioridade
│   ├── demanda.py              # Lógica da Demanda Cidadã e do mural de feedback
│   ├── gamificacao.py          # Perfil, progresso de exploração e conquistas
│   ├── geo.py                  # Cálculo de distância (Haversine)
│   ├── icones.py                # Ícones SVG inline (Lucide)
│   ├── mascara_fora_ceara.py   # Máscara visual do mapa
│   ├── resumos.py               # Resumos automáticos (acessibilidade/leitores de tela)
│   ├── simulador.py             # Lógica do Simulador de Investimento
│   ├── theme.py                  # Paleta de cores (inclusive as 4 de daltonismo) e CSS
│   └── transparencia.py          # Geração dos cards PNG do Painel de Transparência
├── streamlit_app.py     # Ponto de entrada da aplicação
└── pyproject.toml       # Dependências do projeto
```

## 🎯 ODS trabalhados

- **ODS 4** — Educação de qualidade
- **ODS 10** — Redução das desigualdades
- **ODS 11** — Cidades e comunidades sustentáveis

## 👥 Squad

**ZeroKai** — Desafio dos Dados VIVO 2026

## 📄 Licença

Ver [`LICENSE`](LICENSE).