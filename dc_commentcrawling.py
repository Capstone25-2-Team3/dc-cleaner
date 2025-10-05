import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_article_links(base_url):
    res = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = []

    for a_tag in soup.select('a.main_log'):
        href = a_tag.get('href')
        title_tag = a_tag.select_one('div.box.besttxt p')
        if href and title_tag:
            title = title_tag.text.strip()
            link = "https://gall.dcinside.com" + href if href.startswith("/board") else href
            articles.append((title, link))

    return articles


def get_article_content_and_comments(article_url):
    res = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 본문 가져오기 (구조는 변경될 수 있음)
    content_tag = soup.select_one('div.write_div') or soup.select_one('div.gall_content')
    content = content_tag.text.strip() if content_tag else ""

    # 댓글 가져오기
    comment_tags = soup.select('p.usertxt.ub-word')
    comments = [tag.text.strip() for tag in comment_tags]

    return content, comments


# ✅ 실행 예시
base_url = "https://gall.dcinside.com/board/lists/?id=dcbest"  # 예: 디시 베스트
article_links = get_article_links(base_url)

for i, (title, link) in enumerate(article_links[:5]):  # 앞의 5개만 예시로
    print(f"\n[{i+1}] 제목: {title}")
    print(f"링크: {link}")
    
    content, comments = get_article_content_and_comments(link)
    print(f"본문: {content[:100]}...")
    print(f"댓글 수: {len(comments)}")
    for c in comments[:3]:  # 앞의 3개 댓글만 출력
        print(f"  - {c}")
    
    time.sleep(1)  # 너무 빠르게 요청하지 않도록 대기