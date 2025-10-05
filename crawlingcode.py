import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ✅ 마이너 갤러리 ID
GALLERY_ID = "kica"
BASE_URL = f"https://gall.dcinside.com/mgallery/board/lists/?id={GALLERY_ID}"
POST_BASE = "https://gall.dcinside.com"

# ✅ 수집할 페이지 수
MAX_PAGES = 100
output_file = f"dc_{GALLERY_ID}_sentences.tsv"  # ➜ 탭으로 구분된 텍스트 파일

def get_post_urls(page):
    url = f"{BASE_URL}&page={page}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    urls = []
    rows = soup.select("tr.ub-content")

    for row in rows:
        a_tag = row.select_one("td.gall_tit a")
        if a_tag and "href" in a_tag.attrs:
            href = a_tag["href"]
            if "view" in href:
                full_url = POST_BASE + href
                urls.append(full_url)

    return urls

def get_post_content_and_comments(url):
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # 게시글 본문
        content_tag = soup.select_one("div.write_div")
        content = content_tag.get_text(strip=True) if content_tag else ""

        # 댓글
        comment_tags = soup.select("div.inner_text")
        comments = [c.get_text(strip=True) for c in comment_tags]

        return content, comments
    except Exception as e:
        print(f"❌ Error: {e}")
        return "", []

# 🔽 저장
with open(output_file, "w", encoding="utf-8") as f:
    for page in range(1, MAX_PAGES + 1):
        print(f"📄 페이지 {page} 처리 중...")
        post_urls = get_post_urls(page)

        for post_url in post_urls:
            print(f"  ▶ {post_url}")
            content, comments = get_post_content_and_comments(post_url)

            if content:
                f.write(f"{post_url}\t{content}\n")
            for comment in comments:
                f.write(f"{post_url}\t{comment}\n")

            time.sleep(0.5)