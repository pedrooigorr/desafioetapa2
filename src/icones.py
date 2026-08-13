"""
Ícones SVG inline usados no app — conjunto Lucide (lucide.dev),
licença ISC, mesmo padrão já usado no botão de ouvir
(src/acessibilidade.py). Ficam centralizados aqui pra qualquer
função em src/theme.py poder pedir um ícone pelo nome, sem
precisar colar o SVG inteiro toda vez.
"""

from __future__ import annotations

# Miolo de cada ícone (sem a tag <svg> externa, que é montada em
# icone() com a cor e o tamanho pedidos) — path data original do
# Lucide, viewBox 0 0 24 24.
_ICONES: dict[str, str] = {
    "landmark": "<path d=\"M10 18v-7\" /> <path d=\"M11.119 2.205a2 2 0 0 1 1.762 0l7.84 3.846A.5.5 0 0 1 20.5 7h-17a.5.5 0 0 1-.22-.949z\" /> <path d=\"M14 18v-7\" /> <path d=\"M18 18v-7\" /> <path d=\"M3 22h18\" /> <path d=\"M6 18v-7\" />",
    "vote": "<path d=\"m9 12 2 2 4-4\" /> <path d=\"M5 7c0-1.1.9-2 2-2h10a2 2 0 0 1 2 2v12H5V7Z\" /> <path d=\"M22 19H2\" />",
    "piggy-bank": "<path d=\"M11 17h3v2a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-3a3.16 3.16 0 0 0 2-2h1a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1h-1a5 5 0 0 0-2-4V3a4 4 0 0 0-3.2 1.6l-.3.4H11a6 6 0 0 0-6 6v1a5 5 0 0 0 2 4v3a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1z\" /> <path d=\"M16 10h.01\" /> <path d=\"M2 8v1a2 2 0 0 0 2 2h1\" />",
    "map": "<path d=\"M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z\" /> <path d=\"M15 5.764v15\" /> <path d=\"M9 3.236v15\" />",
    "building-2": "<path d=\"M10 12h4\" /> <path d=\"M10 8h4\" /> <path d=\"M14 21v-3a2 2 0 0 0-4 0v3\" /> <path d=\"M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2\" /> <path d=\"M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16\" />",
    "trending-up": "<path d=\"M16 7h6v6\" /> <path d=\"m22 7-8.5 8.5-5-5L2 17\" />",
    "flag-triangle-right": "<path d=\"M6 22V2.8a.8.8 0 0 1 1.17-.71l11.38 5.69a.8.8 0 0 1 0 1.44L6 15.5\" />",
    "megaphone": "<path d=\"M11 6a13 13 0 0 0 8.4-2.8A1 1 0 0 1 21 4v12a1 1 0 0 1-1.6.8A13 13 0 0 0 11 14H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z\" /> <path d=\"M6 14a12 12 0 0 0 2.4 7.2 2 2 0 0 0 3.2-2.4A8 8 0 0 1 10 14\" /> <path d=\"M8 6v8\" />",
    "map-pinned": "<path d=\"M18 8c0 3.613-3.869 7.429-5.393 8.795a1 1 0 0 1-1.214 0C9.87 15.429 6 11.613 6 8a6 6 0 0 1 12 0\" /> <circle cx=\"12\" cy=\"8\" r=\"2\" /> <path d=\"M8.714 14h-3.71a1 1 0 0 0-.948.683l-2.004 6A1 1 0 0 0 3 22h18a1 1 0 0 0 .948-1.316l-2-6a1 1 0 0 0-.949-.684h-3.712\" />",
    "circle-x": "<circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"m15 9-6 6\" /> <path d=\"m9 9 6 6\" />",
    "percent": "<line x1=\"19\" x2=\"5\" y1=\"5\" y2=\"19\" /> <circle cx=\"6.5\" cy=\"6.5\" r=\"2.5\" /> <circle cx=\"17.5\" cy=\"17.5\" r=\"2.5\" />",
    "users": "<path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /> <path d=\"M16 3.128a4 4 0 0 1 0 7.744\" /> <path d=\"M22 21v-2a4 4 0 0 0-3-3.87\" /> <circle cx=\"9\" cy=\"7\" r=\"4\" />",
    "inbox": "<polyline points=\"22 12 16 12 14 15 10 15 8 12 2 12\" /> <path d=\"M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z\" />",
    "mouse-pointer-click": "<path d=\"M14 4.1 12 6\" /> <path d=\"m5.1 8-2.9-.8\" /> <path d=\"m6 12-1.9 2\" /> <path d=\"M7.2 2.2 8 5.1\" /> <path d=\"M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z\" />",
    "book-open": "<path d=\"M12 5v16\" /> <path d=\"M20.001 19A2 2 0 0022 17V5a2 2 0 00-1.999-2L16 3.002A5 5 0 0012 5a5 5 0 00-4-2H4a2 2 0 00-2 2v12a2 2 0 001.999 2H8a5 5 0 014 2 5 5 0 014-2z\" />",
    "drama": "<path d=\"M10 11h.01\" /> <path d=\"M14 6h.01\" /> <path d=\"M18 6h.01\" /> <path d=\"M6.5 13.1h.01\" /> <path d=\"M22 5c0 9-4 12-6 12s-6-3-6-12c0-2 2-3 6-3s6 1 6 3\" /> <path d=\"M17.4 9.9c-.8.8-2 .8-2.8 0\" /> <path d=\"M10.1 7.1C9 7.2 7.7 7.7 6 8.6c-3.5 2-4.7 3.9-3.7 5.6 4.5 7.8 9.5 8.4 11.2 7.4.9-.5 1.9-2.1 1.9-4.7\" /> <path d=\"M9.1 16.5c.3-1.1 1.4-1.7 2.4-1.4\" />",
    "clapperboard": "<path d=\"m12.296 3.464 3.02 3.956\" /> <path d=\"M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3z\" /> <path d=\"M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\" /> <path d=\"m6.18 5.276 3.1 3.899\" />",
    "accessibility": "<circle cx=\"16\" cy=\"4\" r=\"1\" /> <path d=\"m18 19 1-7-6 1\" /> <path d=\"m5 8 3-3 5.5 3-2.36 3.5\" /> <path d=\"M4.24 14.5a5 5 0 0 0 6.88 6\" /> <path d=\"M13.76 17.5a5 5 0 0 0-6.88-6\" />",
}


def icone(nome: str, cor: str = "currentColor", tamanho: int = 20) -> str:
    """
    Devolve o HTML de um ícone SVG inline (Lucide), pronto pra ir
    dentro de um f-string de outro componente (cartao_hero,
    cartao_kpi, chip_equipamento, estado_vazio, titulo_secao...).

    Se o nome não existir no conjunto (erro de digitação, ícone
    novo que ainda não foi baixado), cai num "ponto de
    interrogação" simples em vez de quebrar a página inteira.
    """
    miolo = _ICONES.get(nome)
    if miolo is None:
        miolo = (
            '<circle cx="12" cy="12" r="10" />'
            '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />'
            '<path d="M12 17h.01" />'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tamanho}" '
        f'height="{tamanho}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{cor}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" '
        f'style="display:inline-block; vertical-align:middle;">'
        f"{miolo}</svg>"
    )