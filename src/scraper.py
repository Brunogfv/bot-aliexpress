import requests
import re
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup


@dataclass
class Deal:
    title: str
    price: str
    store: str
    url: str
    category: str


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

SKIP_TITLES = [
    "cupons", "calendario", "calendário", "moedas", "vip",
    "ofertas de combo", "promocoes", "promoções", "paginas",
    "grupos", "canais",
]

CATEGORY_KEYWORDS = {
    "speaker", "caixinha", "fone", "headset", "microfone",
    "smartwatch", "watch", "drone", "smartphone", "celular",
    "tablet", "notebook", "tv ", "projetor", "monitor",
    "gamepad", "console", "controle", "joystick",
    "mouse", "teclado", "keyboard", "webcam", "camera",
    "ssd", "hd ", "nvme", "memoria", "ram", "processador",
    "placa mae", "placa de video", "fonte", "gabinete",
    "cadeira", "mesa", "roteador", "carregador", "power bank",
    "cabo", "adaptador", "cooler", "mouse pad",
}


def fetch_aliexpress_deals(max_deals: int = 15) -> list[Deal]:
    url = "https://www.chinacuponsbr.com/"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return _parse_posts(resp.text, max_deals)


def _parse_posts(html: str, max_deals: int) -> list[Deal]:
    soup = BeautifulSoup(html, "lxml")
    deals = []

    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        if "aliexpress" not in text.lower():
            continue

        raw_title = re.sub(r'\s*\(AliExpress\)\s*', ' ', text)
        raw_title = re.sub(r'[^\x20-\x7E\xC0-\xFF]+', ' ', raw_title)
        raw_title = ' '.join(raw_title.split())
        title = raw_title.strip().rstrip(",").strip()

        if len(title) < 10:
            continue

        skip = False
        for kw in SKIP_TITLES:
            if title.lower().startswith(kw):
                skip = True
                break
        if skip:
            continue

        post = h2.find_parent(["div", "article", "section"])
        if not post:
            post = h2.parent
        post_html = str(post) if post else ""

        price_match = re.search(r'R\$\s*([0-9]+[.,][0-9]+)', post_html)
        if not price_match:
            continue
        price = f"R$ {price_match.group(1).replace('.', ',')}"

        category = _detect_category(title)

        link = post.find("a", href=True) if post else None
        url = link["href"] if link else "https://www.chinacuponsbr.com"

        deals.append(Deal(
            title=title[:120],
            price=price,
            store="aliexpress",
            url=url,
            category=category,
        ))

    seen = set()
    unique = []
    for d in deals:
        key = d.title.lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(d)

    return unique[:max_deals]


def _detect_category(title: str) -> str:
    lower = title.lower()
    for kw in CATEGORY_KEYWORDS:
        if kw in lower:
            return kw.title()
    return ""


def format_telegram(deals: list[Deal]) -> str:
    if not deals:
        return "Nenhuma promocao do AliExpress encontrada."

    now = datetime.now().strftime("%d/%m/%Y")
    lines = [f"*ALIEXPRESS - Promocoes {now}*\n"]
    for d in deals[:8]:
        cat = f" [{d.category}]" if d.category else ""
        lines.append(f"* {d.title[:70]}{cat}\n  {d.price}\n")
    lines.append(f"\nFonte: chinacuponsbr.com - {len(deals)} ofertas")
    return "\n".join(lines)


def format_text(deals: list[Deal]) -> str:
    if not deals:
        return "Nenhuma promocao do AliExpress encontrada."

    now = datetime.now().strftime("%d/%m/%Y")
    lines = ["=" * 60, f"ALIEXPRESS - PROMOCOES {now}", "=" * 60]
    for i, d in enumerate(deals[:10], 1):
        cat = f" [{d.category}]" if d.category else ""
        lines.append(f"\n{i}. {d.title}{cat}")
        lines.append(f"   Preco: {d.price}")
        lines.append(f"   {d.url}")

    lines.append(f"\n{len(deals)} ofertas encontradas em chinacuponsbr.com")
    return "\n".join(lines)
