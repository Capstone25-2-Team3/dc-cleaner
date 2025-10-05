import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 크롤링 대상 갤러리 ID 입력
GALLERY_ID = "baseball_new"  # 예: 야구 갤러리

# 수집할 게시글 페이지 수 (한 페이지당 약 20개 글)
MAX_PAGES = 170

output_file = "dc_output.txt"

def get_post_urls(page):
    url = f"https://gall.dcinside.com/board/lists/?id={GALLERY_ID}&page={page}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    urls = []
    rows = soup.select("tr.ub-content")

    for row in rows:
        a_tag = row.select_one("td.gall_tit a")
        if a_tag and "href" in a_tag.attrs:
            href = a_tag["href"]
            if "view" in href:
                full_url = "https://gall.dcinside.com" + href
                urls.append(full_url)

    return urls

def get_post_content_and_comments(url):
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # 게시글 본문
        content = soup.select_one("div.write_div").get_text(strip=True)

        # 댓글
        comment_tags = soup.select("div.inner_text")
        comments = [c.get_text(strip=True) for c in comment_tags]

        return content, comments
    except Exception as e:
        print(f"Error: {e}")
        return "", []

# 🔽 본문과 댓글 저장 시작
with open(output_file, "w", encoding="utf-8") as f:
    for page in range(1, MAX_PAGES + 1):
        print(f"페이지 {page} 처리 중...")
        post_urls = get_post_urls(page)
        for post_url in post_urls:
            print(f"  ▶ {post_url}")
            content, comments = get_post_content_and_comments(post_url)

            if content:
                f.write("[본문]\n")
                f.write(content + "\n")

            for comment in comments:
                f.write("[댓글]\n")
                f.write(comment + "\n")

            f.write("-----\n")  # 구분선

            time.sleep(0.5)  # 서버 부하 방지