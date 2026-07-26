# Fonte Inter

Arquivo: `Inter-Variable.ttf`
Fonte: Google Fonts (repositório oficial google/fonts, pasta `ofl/inter`)
Licença: SIL Open Font License 1.1 (livre para uso comercial e redistribuição)

Usada em `src/transparencia.py` pra gerar os cards PNG do Painel de
Transparência — substitui a fonte padrão do Pillow, que não renderiza
corretamente caracteres acentuados (á, é, í, ó, ú, ã, õ, ç), essenciais
pra textos em português.

É uma fonte variável (variable font): um único arquivo contém todos os
pesos, de Thin a Black. O código seleciona "Regular" ou "Bold" via
`fonte.set_variation_by_name(...)`.