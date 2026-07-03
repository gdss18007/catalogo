import csv
from pathlib import Path
from html import escape

ARQUIVO_HTML = "vitrine.html"
ARQUIVO_CSV = "produtos.csv"


def limpar_texto(valor):
    return (valor or "").strip()


def slugify_categoria(valor):
    return limpar_texto(valor).lower().replace(" ", "-")


def parse_imagens(texto):
    return [img.strip() for img in limpar_texto(texto).split(",") if img.strip()]


def montar_badge(row):
    badge_text = escape(limpar_texto(row.get("badge_text")))
    badge_tipo = slugify_categoria(row.get("badge_tipo"))

    if not badge_text:
        return ""

    classe = f"product-badge {badge_tipo}".strip()
    return f'<span class="{classe}">{badge_text}</span>'


def montar_preco(row):
    preco = escape(limpar_texto(row.get("preco")))
    preco_antigo = escape(limpar_texto(row.get("preco_antigo")))

    if not preco:
        preco = "Sob consulta"

    preco_antigo_html = (
        f'<span class="old-price">R$ {preco_antigo}</span>'
        if preco_antigo else ""
    )

    preco_atual_html = (
        f'<span class="current-price">R$ {preco}</span>'
        if preco != "Sob consulta" else f'<span class="current-price">{preco}</span>'
    )

    return f"""
            <div class="product-price">
              {preco_antigo_html}
              {preco_atual_html}
            </div>
    """


def montar_slides(produto_id, nome, imagens):
    slides = []

    for i, img in enumerate(imagens, start=1):
        img_esc = escape(img, quote=True)
        nome_esc = escape(nome)
        slides.append(f"""
                <a href="{img_esc}"
                   class="carousel-slide glightbox"
                   data-gallery="produto-{produto_id}"
                   data-glightbox="title: {nome_esc}">
                  <img src="{img_esc}"
                       alt="{nome_esc} - imagem {i}"
                       width="400"
                       height="400"
                       loading="lazy" />
                </a>
        """)

    return "\n".join(slides)


def montar_controles(imagens):
    if len(imagens) <= 1:
        return ""

    return """
              <button class="carousel-arrow prev" type="button" aria-label="Imagem anterior">‹</button>
              <button class="carousel-arrow next" type="button" aria-label="Próxima imagem">›</button>
              <div class="carousel-dots" aria-label="Selecionar imagem"></div>
    """


def montar_acoes(row):
    whatsapp_url = escape(limpar_texto(row.get("whatsapp_url")), quote=True)
    marketplace_url = escape(limpar_texto(row.get("marketplace_url")), quote=True)

    if not whatsapp_url:
        whatsapp_url = "https://wa.me/5500000000000"

    marketplace_html = ""
    if marketplace_url:
        marketplace_html = f'''
            <a href="{marketplace_url}" target="_blank" rel="noopener noreferrer" class="btn-marketplace">
              Ver no Marketplace
            </a>
        '''

    return f"""
          <div class="product-actions">
            <a href="{whatsapp_url}" target="_blank" rel="noopener noreferrer" class="btn-wpp">
              Comprar pelo WhatsApp
            </a>
            {marketplace_html}
          </div>
    """


def gerar_card(row):
    produto_id = escape(limpar_texto(row.get("id")))
    nome = limpar_texto(row.get("nome"))
    descricao = escape(limpar_texto(row.get("descricao")))
    categoria = slugify_categoria(row.get("categoria"))
    imagens = parse_imagens(row.get("imagens"))

    if not produto_id or not nome or not imagens:
        return ""

    nome_esc = escape(nome)
    badge_html = montar_badge(row)
    preco_html = montar_preco(row)
    slides_html = montar_slides(produto_id, nome, imagens)
    controles_html = montar_controles(imagens)
    acoes_html = montar_acoes(row)

    return f"""
        <article class="product-card" data-cat="{categoria}" data-product-id="{produto_id}">
          <div class="product-media">
            {badge_html}
            <div class="product-carousel" data-carousel>
              {controles_html}
              <div class="carousel-track">
                {slides_html}
              </div>
            </div>
          </div>

          <div class="product-body">
            <h3 class="product-name">{nome_esc}</h3>
            <p class="product-desc">{descricao}</p>
            {preco_html}
          </div>

          {acoes_html}
        </article>
    """


def atualizar_html(cards_html):
    caminho = Path(ARQUIVO_HTML)
    html = caminho.read_text(encoding="utf-8")

    inicio = "<!-- INICIO_PRODUTOS -->"
    fim = "<!-- FIM_PRODUTOS -->"

    pos_inicio = html.find(inicio)
    pos_fim = html.find(fim)

    if pos_inicio == -1 or pos_fim == -1 or pos_fim <= pos_inicio:
        raise ValueError("Marcadores <!-- INICIO_PRODUTOS --> e <!-- FIM_PRODUTOS --> não encontrados corretamente.")

    antes = html[:pos_inicio + len(inicio)]
    depois = html[pos_fim:]

    novo_html = f"{antes}\n{cards_html}\n        {depois}"
    caminho.write_text(novo_html, encoding="utf-8")


def gerar_cards():
    cards = []

    with open(ARQUIVO_CSV, mode="r", encoding="utf-8") as arquivo:
        reader = csv.DictReader(arquivo, delimiter=";")
        for row in reader:
            card_html = gerar_card(row)
            if card_html:
                cards.append(card_html)

    atualizar_html("\n".join(cards))
    print(f"{len(cards)} produtos gerados com sucesso.")


if __name__ == "__main__":
    gerar_cards()