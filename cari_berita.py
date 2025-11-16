import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re
import html

#  FUNGSI BERSIHKAN DESKRIPSI
def clean_description(raw):
    if not raw:
        return "-"

    # Hapus tag <img>
    raw = re.sub(r"<img[^>]+>", "", raw)

    # Hapus tag HTML lainnya
    raw = re.sub(r"<[^>]+>", "", raw)

    # Decode entitas HTML (&amp; dsb)
    raw = html.unescape(raw)

    return raw.strip()

#   FUNGSI AMBIL RSS

def fetch_rss(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        items = root.findall(".//item")
        news_list = []

        for item in items:
            title = item.findtext("title", "-")
            link = item.findtext("link", "-")
            pubDate = item.findtext("pubDate", "-")

            # Deskripsi
            desc = clean_description(item.findtext("description", ""))

            # content:encoded (lebih lengkap)
            content_encoded = item.find(".//{http://purl.org/rss/1.0/modules/content/}encoded")
            if content_encoded is not None:
                long_desc = clean_description(content_encoded.text)
                if len(long_desc) > len(desc):
                    desc = long_desc

            # Minimal 20 huruf agar tidak kosong
            if len(desc) < 20:
                desc += "..."

            # Ambil gambar
            image_url = None

            # media:thumbnail
            thumb = item.find(".//{http://search.yahoo.com/mrss/}thumbnail")
            if thumb is not None and "url" in thumb.attrib:
                image_url = thumb.attrib["url"]

            # media:content
            content = item.find(".//{http://search.yahoo.com/mrss/}content")
            if image_url is None and content is not None and "url" in content.attrib:
                image_url = content.attrib["url"]

            # enclosure
            enclosure = item.find("enclosure")
            if enclosure is not None and enclosure.attrib.get("type", "").startswith("image"):
                image_url = enclosure.attrib.get("url")

            news_list.append({
                "title": title,
                "link": link,
                "pubDate": pubDate,
                "description": desc,
                "image": image_url
            })

        return news_list

    except Exception:
        return []


#     HALAMAN STREAMLIT
def show():
    st.title("📰 Beberapa Berita Indonesia Terbaru")
    st.write ("Cari berita dengan ketik kata kunci anda, Contoh : Prabowo")

    # Hanya keyword
    keyword = st.text_input("Cari berita :")

    # Daftar media Indonesia
    sources = {
        "CNN Indonesia": "https://www.cnnindonesia.com/nasional/rss",
        "Detik": "http://rss.detik.com/index.php/detikcom",
        "Kompas": "https://www.kompas.com/rss/nasional",
        "CNBC Indonesia": "https://www.cnbcindonesia.com/news/rss",
        "Liputan6": "https://www.liputan6.com/rss",
        "Tempo": "https://rss.tempo.co/nasional",
        "Antara News": "https://www.antaranews.com/rss/terkini",
    }

    all_news = []

    # Gabungkan berita
    for name, url in sources.items():
        data = fetch_rss(url)
        for item in data:
            item["source"] = name
        all_news.extend(data)

    # Filter keyword
    if keyword:
        all_news = [
            n for n in all_news
            if keyword.lower() in n["title"].lower()
        ]

    # Tombol tampilkan berita
    if st.button("🔍 Tampilkan Berita"):
        if not all_news:
            st.warning("Tidak ada berita ditemukan.")
        else:
            for news in all_news:
                st.markdown("---")

                # Gambar
                if news["image"]:
                    st.image(news["image"], use_container_width=True)

                st.subheader(news["title"])
                st.write(f"🗞 Sumber: **{news['source']}**")
                st.write(f"📅 {news['pubDate']}")
                st.write(news["description"])


                st.markdown(f"[🔗 Baca Selengkapnya]({news['link']})")

