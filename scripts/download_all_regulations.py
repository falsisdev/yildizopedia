import os
import re
import ssl
import urllib.request
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()

def get_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return BeautifulSoup(resp.read(), 'html.parser')

def sanitize_filename(name):
    name = unquote(name)
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    name = re.sub(r'\s+', '_', name).strip('._')
    return name

def download_file(url, target_folder, custom_name=None):
    os.makedirs(target_folder, exist_ok=True)
    try:
        url_clean = url.replace(' ', '%20')
        req = urllib.request.Request(url_clean, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            content = resp.read()
            ext = os.path.splitext(url.split('?')[0])[1].lower()
            if not ext:
                content_type = resp.headers.get('Content-Type', '')
                if 'pdf' in content_type:
                    ext = '.pdf'
                elif 'word' in content_type or 'officedocument' in content_type:
                    ext = '.docx'
                elif 'excel' in content_type:
                    ext = '.xlsx'
                else:
                    ext = '.bin'
            
            if custom_name:
                filename = sanitize_filename(custom_name)
                if not filename.lower().endswith(ext):
                    filename += ext
            else:
                raw_filename = os.path.basename(url.split('?')[0])
                filename = sanitize_filename(raw_filename)

            target_path = os.path.join(target_folder, filename)
            with open(target_path, 'wb') as f:
                f.write(content)
            print(f"Downloaded: {filename} ({len(content)} bytes) to {target_folder}")
            return target_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_ogi_mevzuat():
    print("\n--- Processing OGİ Mevzuat & Yönergeler ---")
    urls = [
        "https://ogi.yildiz.edu.tr/mevzuat",
        "https://ogi.yildiz.edu.tr/iletisim/hizli-erisim/yonetmelik-ve-yonergeler"
    ]
    seen_urls = set()
    for base_url in urls:
        try:
            soup = get_soup(base_url)
            for a in soup.find_all('a', href=True):
                href = urljoin(base_url, a['href'])
                text = a.get_text(strip=True)
                # check parent text for directive title
                p_text = a.parent.get_text(strip=True) if a.parent else text
                
                lower_href = href.lower()
                if any(ext in lower_href for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                    if href not in seen_urls:
                        seen_urls.add(href)
                        title = p_text if len(p_text) > 5 and len(p_text) < 150 else text
                        if 'tıklayınız' in title.lower():
                            title = title.replace('tıklayınız.', '').replace('tıklayınız', '').strip(' :-\t')
                        print(f"Found doc: {title} -> {href}")
                        download_file(href, "arsiv/mevzuat_ve_yonergeler", custom_name=title)
        except Exception as e:
            print(f"Error reading {base_url}: {e}")

def process_ybd_exams():
    print("\n--- Processing YBD Sınav Örnekleri ---")
    url = "https://ybd.yildiz.edu.tr/ogrenci/sinav-ornekleri"
    try:
        soup = get_soup(url)
        for a in soup.find_all('a', href=True):
            href = urljoin(url, a['href'])
            text = a.get_text(strip=True)
            if href.lower().endswith('.pdf'):
                print(f"Found YBD exam PDF: {text} -> {href}")
                download_file(href, "arsiv/ybd_belgeleri", custom_name=text)
    except Exception as e:
        print(f"Error reading YBD: {e}")

def process_ehm_regulations():
    print("\n--- Processing EHM Yönetmelik ve Belgeler ---")
    url = "https://ehm.yildiz.edu.tr/egitim/yonetmelik-ve-yonergeler"
    try:
        soup = get_soup(url)
        for a in soup.find_all('a', href=True):
            href = urljoin(url, a['href'])
            text = a.get_text(strip=True)
            if any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx']):
                print(f"Found EHM Doc: {text} -> {href}")
                download_file(href, "arsiv/ehm_belgeleri", custom_name=text)
    except Exception as e:
        print(f"Error reading EHM: {e}")

if __name__ == '__main__':
    process_ogi_mevzuat()
    process_ybd_exams()
    process_ehm_regulations()
    print("\nAll downloads finished!")
