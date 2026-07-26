"""
Feature 3 (revisada) — Painel de Transparência do Gestor.

Versão pública do Índice de Prioridade: um ranking de fácil leitura de
quais municípios têm o maior "deserto cultural" do Ceará, com cards
prontos pra baixar e compartilhar (formato retrato, estilo rede social).

A ideia: o mesmo dado que já usamos pra planejamento interno (Radar
Cultural) vira também uma ferramenta de cobrança cívica — transparência
pública sobre quem está sendo deixado de fora.

Só usa dados 100% reais já calculados no Radar Cultural (nenhum dado
ilustrativo aqui, ao contrário do Termômetro de Investimento que foi
descartado por depender de uma fonte externa difícil de integrar).
"""

from __future__ import annotations

import io
import os

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Paleta igual ao resto do app (src/theme.py) — repetida aqui pra este
# módulo não depender de Streamlit/Plotly, só de Pillow
_TERRACOTA = "#C1440E"
_TERRACOTA_ESCURO = "#7A2E0E"
_AREIA = "#FBEBD4"
_AREIA_CLARA = "#FFFDF8"
_TEXTO_ESCURO = "#1A0F08"
_VERDE = "#4C6444"

_LARGURA, _ALTURA = 1080, 1350

EQUIPAMENTOS_CARD = {
    "tem_museu": "Museu",
    "tem_teatro_sala_espetaculo": "Teatro / Sala de espetáculo",
    "tem_cinema": "Cinema",
    "tem_biblioteca": "Biblioteca",
}


def montar_ranking_publico(df: pd.DataFrame, n: int = 30) -> pd.DataFrame:
    """Ranking público pelo Índice de Prioridade, com a posição (1º, 2º...)."""
    ranking = df.sort_values("indice_prioridade", ascending=False).head(n).copy()
    ranking.insert(0, "posicao", range(1, len(ranking) + 1))
    return ranking[
        [
            "posicao",
            "municipio",
            "mesorregiao",
            "populacao",
            "renda_per_capita",
            "n_equipamentos_raros",
            "indice_prioridade",
        ]
    ].rename(
        columns={
            "posicao": "#",
            "municipio": "Município",
            "mesorregiao": "Mesorregião",
            "populacao": "População",
            "renda_per_capita": "Renda per capita (R$)",
            "n_equipamentos_raros": "Equipamentos (de 3)",
            "indice_prioridade": "Índice de Prioridade",
        }
    )


# Fonte Inter (variável, licença SIL Open Font License), embutida em
# assets/fonts/ — a fonte padrão do Pillow (ImageFont.load_default) não
# suporta acentuação completa, e "CEARÁ", "Índice", "É" saíam quebrados
# no card gerado (ver assets/fonts/README.md para a fonte/licença).
_CAMINHO_FONTE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "fonts",
    "Inter-Variable.ttf",
)


def _fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    """
    Carrega a Inter no peso Bold ou Regular, no tamanho pedido. Se o
    arquivo da fonte não for encontrado por algum motivo (ex.: alguém
    esqueceu de copiar a pasta assets/ junto do projeto), cai de volta
    pra fonte padrão do Pillow — o card continua funcionando, só sem
    acentuação correta.
    """
    try:
        fonte = ImageFont.truetype(_CAMINHO_FONTE, tamanho)
        fonte.set_variation_by_name("Bold" if negrito else "Regular")
        return fonte
    except (OSError, ValueError):
        return ImageFont.load_default(size=tamanho)


def _texto_centralizado(draw, texto, y, fonte, cor, largura_img=_LARGURA):
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    largura_texto = bbox[2] - bbox[0]
    x = (largura_img - largura_texto) / 2
    draw.text((x, y), texto, font=fonte, fill=cor)
    return bbox[3] - bbox[1]  # altura do texto desenhado


def _ajustar_fonte_para_largura(draw, texto, largura_max, tamanho_inicial, negrito=False):
    tamanho = tamanho_inicial
    while tamanho > 28:
        fonte = _fonte(tamanho, negrito=negrito)
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        if (bbox[2] - bbox[0]) <= largura_max:
            return fonte
        tamanho -= 4
    return _fonte(28, negrito=negrito)


def gerar_card_municipio(linha_ranking: pd.Series, total_no_ranking: int) -> bytes:
    """
    Gera um card retrato (1080x1350, formato Stories/Instagram) pronto
    pra baixar e compartilhar, com o Índice de Prioridade daquele
    município — a versão "pública" do Radar Cultural.
    Retorna os bytes do PNG.
    """
    img = Image.new("RGB", (_LARGURA, _ALTURA), _AREIA)
    draw = ImageDraw.Draw(img)

    margem = 70

    # Faixa do topo
    draw.rectangle([0, 0, _LARGURA, 190], fill=_TERRACOTA)
    _texto_centralizado(
        draw, "RADAR CULTURAL · CEARÁ", 55, _fonte(38, negrito=True), _AREIA_CLARA
    )
    _texto_centralizado(
        draw, "Painel de Transparência", 110, _fonte(30), _AREIA_CLARA
    )

    # Selo de posição no ranking
    posicao = int(linha_ranking["#"])
    texto_posicao = f"Nº {posicao} EM DÉFICIT CULTURAL NO CEARÁ"
    draw.rounded_rectangle(
        [margem, 235, _LARGURA - margem, 320], radius=22, fill=_TERRACOTA_ESCURO
    )
    fonte_posicao = _ajustar_fonte_para_largura(
        draw, texto_posicao, _LARGURA - 2 * margem - 40, 34, negrito=True
    )
    _texto_centralizado(draw, texto_posicao, 262, fonte_posicao, _AREIA_CLARA)

    # Nome do município
    nome = linha_ranking["Município"]
    fonte_nome = _ajustar_fonte_para_largura(
        draw, nome, _LARGURA - 2 * margem, 86, negrito=True
    )
    _texto_centralizado(draw, nome, 365, fonte_nome, _TEXTO_ESCURO)

    # Mesorregião
    _texto_centralizado(
        draw,
        linha_ranking["Mesorregião"],
        480,
        _fonte(32),
        "#6B4226",
    )

    # Linha divisória
    draw.line([margem, 545, _LARGURA - margem, 545], fill=_TERRACOTA, width=4)

    # Estatísticas
    y = 590
    linhas_stats = [
        ("POPULAÇÃO", f"{int(linha_ranking['População']):,}".replace(",", ".")),
        (
            "RENDA PER CAPITA",
            f"R$ {linha_ranking['Renda per capita (R$)']:.2f}".replace(".", ","),
        ),
        (
            "EQUIPAMENTOS CULTURAIS",
            (f"{int(linha_ranking['Equipamentos (de 3)'])} de 3 "
            "(museu, teatro, cinema)"),
        ),
        ("ÍNDICE DE PRIORIDADE", f"{linha_ranking['Índice de Prioridade']:.2f}"),
    ]
    for rotulo, valor in linhas_stats:
        draw.text((margem, y), rotulo, font=_fonte(26), fill="#6B4226")
        draw.text(
            (margem, y + 40), valor, font=_fonte(44, negrito=True), fill=_TEXTO_ESCURO
        )
        y += 130

    # Rodapé
    draw.rectangle([0, _ALTURA - 130, _LARGURA, _ALTURA], fill=_TERRACOTA)
    _texto_centralizado(
        draw,
        "Squad ZeroKai · Desafio dos Dados VIVO 2026",
        _ALTURA - 105,
        _fonte(26),
        _AREIA_CLARA,
    )
    _texto_centralizado(
        draw,
        "Fonte: IBGE/MUNIC 2014 · Atlas Brasil (Censo 2010)",
        _ALTURA - 65,
        _fonte(22),
        _AREIA_CLARA,
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()