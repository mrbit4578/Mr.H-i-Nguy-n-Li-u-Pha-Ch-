#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP Scout Collector — Thu thập tin tức ngành nguyên liệu pha chế theo thời gian thực
====================================================================================
Kéo tin mới từ Google News RSS theo bộ từ khóa ngành, lưu thành file Markdown
trong thư mục data/ để: (1) đọc nhanh, (2) dán cho Agent tóm tắt & cập nhật memory.

Cài đặt (1 lần):   pip install requests
Chạy:              python agent/collector.py
Tự động hằng ngày: dùng cron (Linux/Mac) hoặc Task Scheduler (Windows)
  cron ví dụ:  0 7 * * *  cd /duong/dan/du-an-nguyen-lieu && python agent/collector.py
"""

import os
import re
import sys
import datetime
import urllib.parse
import xml.etree.ElementTree as ET

try:
    import requests
except ImportError:
    sys.exit("Thieu thu vien 'requests'. Chay:  pip install requests")

# ------------------------- CAU HINH -------------------------
KEYWORDS = [
    # Xu huong do uong
    "xu hướng đồ uống trà sữa Việt Nam",
    "món nước hot trend matcha",
    "nguyên liệu trà sữa mới",
    # Gia & nguon hang
    "giá nguyên liệu pha chế bột kem béo",
    "nhà cung cấp nguyên liệu trà sữa TPHCM",
    "nguyên liệu pha chế Đồng Nai Biên Hòa",
    # An toan thuc pham nganh
    "an toàn thực phẩm nguyên liệu trà sữa",
    "thu hồi nguyên liệu thực phẩm đồ uống",
]

MAX_ITEMS_PER_KEYWORD = 8       # so tin toi da moi tu khoa
DAYS_FRESH = 14                 # chi lay tin trong N ngay gan nhat
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TIMEOUT = 15
HEADERS = {"User-Agent": "Mozilla/5.0 (NLP-Scout-Collector/1.0)"}
# -------------------------------------------------------------


def fetch_rss(keyword: str):
    """Lay danh sach tin tu Google News RSS cho 1 tu khoa."""
    q = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={q}&hl=vi&gl=VN&ceid=VN:vi"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        return [], f"Loi tai RSS '{keyword}': {e}"

    items = []
    try:
        root = ET.fromstring(r.content)
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub = (item.findtext("pubDate") or "").strip()
            src_el = item.find("{https://news.google.com/rss}source")
            source = src_el.text.strip() if src_el is not None and src_el.text else ""
            items.append({"title": title, "link": link, "pub": pub, "source": source})
    except ET.ParseError as e:
        return [], f"Loi phan tich RSS '{keyword}': {e}"
    return items, None


def parse_pubdate(pub: str):
    """Chuyen 'Tue, 01 Jul 2026 08:00:00 GMT' -> datetime; loi thi tra None."""
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            return datetime.datetime.strptime(pub, fmt).replace(tzinfo=None)
        except ValueError:
            continue
    return None


def clean_title(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def main():
    today = datetime.date.today()
    cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS_FRESH)
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"news-{today.isoformat()}.md")

    lines = [
        f"# 📰 Tin ngành nguyên liệu pha chế — thu thập {today.isoformat()}",
        f"*Nguồn: Google News RSS · Lọc tin {DAYS_FRESH} ngày gần nhất · "
        f"Dán file này cho Agent NLP Scout để tóm tắt & cập nhật memory.json*",
        "",
    ]
    total = 0
    seen_links = set()

    for kw in KEYWORDS:
        items, err = fetch_rss(kw)
        lines.append(f"## 🔍 {kw}")
        if err:
            lines.append(f"- ⚠️ {err}")
            lines.append("")
            continue

        count = 0
        for it in items:
            if count >= MAX_ITEMS_PER_KEYWORD:
                break
            if it["link"] in seen_links:
                continue
            d = parse_pubdate(it["pub"])
            if d is not None and d < cutoff:
                continue
            seen_links.add(it["link"])
            datestr = d.strftime("%d/%m/%Y") if d else "?"
            src = f" — *{it['source']}*" if it["source"] else ""
            lines.append(f"- **[{datestr}]** [{clean_title(it['title'])}]({it['link']}){src}")
            count += 1
            total += 1

        if count == 0:
            lines.append(f"- (Không có tin mới trong {DAYS_FRESH} ngày)")
        lines.append("")

    lines += [
        "---",
        f"**Tổng: {total} tin.**",
        "",
        "## ➡️ Bước tiếp theo",
        "1. Mở phiên Agent NLP Scout (dán system-prompt.md + memory.json)",
        "2. Dán nội dung file này và ra lệnh: `/tuan` hoặc:",
        "   \"Tóm tắt các tin trên, chỉ ra cái gì ảnh hưởng đến việc nhập hàng của tôi,",
        "    và xuất memory.json bản cập nhật\"",
    ]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Da luu {total} tin vao: {out_path}")


if __name__ == "__main__":
    main()
