import os
import re
import ssl
import json
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()

PAGES_TO_FETCH = {
    "00_genel_ve_kurumsal/ytu_tarihce_ve_genel_bilgiler": "https://yildiz.edu.tr/",
    "02_ogrenci_isleri_ogi/ogi_genel_isleyis": "https://ogi.yildiz.edu.tr/",
    "02_ogrenci_isleri_ogi/sikca_sorulan_sorular": "https://ogi.yildiz.edu.tr/birim-hakkinda/hizli-erisim/sikca-sorulan-sorular",
    "02_ogrenci_isleri_ogi/ogrenci_bilgilendirmeleri": "https://ogi.yildiz.edu.tr/birim-hakkinda/hizli-erisim/bilgilendirmeler",
    "03_yabanci_diller_yuksekokulu_ybd/hakkinda_ve_egitim_yapisi": "https://ybd.yildiz.edu.tr/temel-ingilizce/hakkinda",
    "03_yabanci_diller_yuksekokulu_ybd/kurlar_ders_icerikleri_hedefler": "https://ybd.yildiz.edu.tr/temel-ingilizce/duzeyler-ders-icerikleri-program-amaclari",
    "03_yabanci_diller_yuksekokulu_ybd/sikca_sorulan_sorular": "https://ybd.yildiz.edu.tr/temel-ingilizce/sikca-sorulan-sorular",
    "03_yabanci_diller_yuksekokulu_ybd/sinavlarda_uyulacak_kurallar": "https://ybd.yildiz.edu.tr/ogrenci/sinavlarda-uyulmasi-zorunlu-kurallar",
    "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/README": "https://ehm.yildiz.edu.tr/",
    "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/program_ciktilari": "https://ehm.yildiz.edu.tr/bolum/program-ciktilari",
    "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/tyyc_uyumu": "https://ehm.yildiz.edu.tr/bolum/turkiye-yuksek-ogretim-yeterlilikler-cercevesi",
    "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/lisans_egitim_yapisi": "https://ehm.yildiz.edu.tr/egitim/lisans",
    "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/sinav_kurallari": "https://ehm.yildiz.edu.tr/ogrenci/sinav-kurallari",
    "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/sikca_sorulan_sorular": "https://ehm.yildiz.edu.tr/ogrenci/sikca-sorulan-sorular",
    "04_bologna_ve_not_sistemi/kabul_ve_kayit_kosullari": "https://www.bologna.yildiz.edu.tr/index.php?r=institution/admission",
    "04_bologna_ve_not_sistemi/not_sistemi_ve_harf_notlari": "https://www.bologna.yildiz.edu.tr/index.php?r=institution/grading"
}

def clean_html_to_markdown(soup, base_url):
    for tag in soup(['script', 'style', 'nav', 'footer', 'noscript', 'header']):
        tag.decompose()
        
    main = soup.find('main') or soup.find('div', id='content') or soup.find('div', class_='content') or soup.find('article') or soup.body
    if not main:
        return ""

    lines = []
    for elem in main.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'table', 'blockquote', 'div']):
        if elem.find_parents(['table', 'ul', 'ol', 'p', 'h1', 'h2', 'h3', 'h4']):
            continue

        if elem.name in ['h1', 'h2', 'h3', 'h4']:
            level = int(elem.name[1])
            text = elem.get_text(" ", strip=True)
            if text:
                lines.append(f"\n{'#' * level} {text}\n")
        elif elem.name == 'p':
            text = elem.get_text(" ", strip=True)
            if text:
                lines.append(f"{text}\n")
        elif elem.name in ['ul', 'ol']:
            for li in elem.find_all('li', recursive=False):
                txt = li.get_text(" ", strip=True)
                if txt:
                    lines.append(f"- {txt}")
            lines.append("")
        elif elem.name == 'table':
            rows = elem.find_all('tr')
            if rows:
                headers = [th.get_text(" ", strip=True) for th in rows[0].find_all(['th', 'td'])]
                if headers:
                    lines.append("\n| " + " | ".join(headers) + " |")
                    lines.append("| " + " | ".join(['---'] * len(headers)) + " |")
                    for r in rows[1:]:
                        cols = [td.get_text(" ", strip=True) for td in r.find_all(['td', 'th'])]
                        if cols:
                            while len(cols) < len(headers):
                                cols.append("")
                            lines.append("| " + " | ".join(cols[:len(headers)]) + " |")
                    lines.append("")
        elif elem.name == 'div':
            # check if accordion or card
            classes = elem.get('class', [])
            if any('card' in c or 'panel' in c or 'accordion' in c for c in classes):
                txt = elem.get_text(" ", strip=True)
                if txt and len(txt) > 20:
                    lines.append(f"{txt}\n")

    return "\n".join(lines)

def run():
    results = {}
    for key, url in PAGES_TO_FETCH.items():
        print(f"Scraping {key} from {url}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                soup = BeautifulSoup(resp.read(), 'html.parser')
                title = soup.title.string.strip() if soup.title else key
                body_md = clean_html_to_markdown(soup, url)
                results[key] = {
                    'title': title,
                    'url': url,
                    'content': body_md
                }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            results[key] = {'title': key, 'url': url, 'content': f"Hata: {e}"}

    with open('scripts/scraped_web_pages.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("All pages scraped and saved to scripts/scraped_web_pages.json")

if __name__ == '__main__':
    run()
