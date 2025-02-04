# ---------- import libraries ----------

# http request를 위한 라이브러리
import requests
# 정규식을 사용하기 위한 라이브러리
import re
# arvix element tree를 사용하기 위한 라이브러리
import xml.etree.ElementTree as ET
# 웹페이지 파싱을 위한 라이브러리
from bs4 import BeautifulSoup
# fallback logic을 위한 라이브러리
from readability import Document
# 시간 측정용 라이브러리
import time

# ---------------------------------------


def get_arxiv_abstract(arxiv_id):
    """
    arxvix.org에서 arxiv_id에 해당하는 논문의 초록을 가져오는 함수
    """
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
        abstract = root.find(".//arxiv:summary", ns).text
        return abstract.strip()
    else:
        return "Error fetching data"

def handle_arxiv(url):
    """
    arxiv.org 사이트의 URL을 처리하는 함수
    """
    arxiv_id = url.rstrip('/').split('/')[-1]
    return get_arxiv_abstract(arxiv_id)

def handle_kor_wikipedia(url):
    """
    한국어 위키백과 사이트의 main content를 추출하는 함수
    """
    response = requests.get(url)

    # error handling
    if response.status_code != 200:
        print(f"Error fetching page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # find the main content that holds the article text
    main_content = soup.find('div', class_='mw-parser-output')
    if not main_content:
        # if main content container is not found, return to the fallback_extraction
        print("Main content container not found.")
        return fallback_extraction(url)

    for tag in main_content.find_all(['script', 'style', 'table', 'ul', 'div']):
        tag.decompose()

    # extranct only paragraph <p> tags
    paragraphs = main_content.find_all('p')
    # extract plain text from paragraphs
    plain_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    return plain_text

# --- 현재까지 main content의 위치가 파악된 사이트 모음 ---
KNOWN_SITE_HANDLERS = {
    r"arxiv\.org": handle_arxiv,
    r"ko\.wikipedia\.org": handle_kor_wikipedia,
}

def dispatch_known_site(url):
    """
    URL이 알려진 사이트 패턴과 일치하는지 확인하고 해당되는 웹사이트의 핸들러를 호출하는 함수
    """
    for pattern, handler in KNOWN_SITE_HANDLERS.items():
        if re.search(pattern, url):
            return handler(url)
    return None

def fallback_extraction(url):
    """
    readability 라이브러리를 사용하여 main content를 추출하는 함수 (fallback logic)
    """
    response = requests.get(url)
    start_time = time.time()
    doc = Document(response.text)
    main_content_html = doc.summary()
    soup = BeautifulSoup(main_content_html, 'html.parser')
    filtered_text = soup.get_text(separator='\n', strip=True)
    elapsed_time = time.time() - start_time
    print(filtered_text)
    print(f'Elapsed time: {elapsed_time:.2f} sec')
    return filtered_text


def crawl(url):
    """
    실제 크롤링 함수 - 여기에 로직을 추가할 수 있음
    """
    # check if the URL matches any known site patterns
    result = dispatch_known_site(url)
    if result:
        return result

    # fallback logic (logic2에 해당되는 경우)
    return fallback_extraction(url)

if __name__ == "__main__":
    test_urls = [
        "https://arxiv.org/abs/2401.12345",#arxiv 논문 초록
        "https://ko.wikipedia.org/wiki/데이터_매트릭스",#한국어 위키백과
        "https://www.yna.co.kr/view/AKR20250204076400009?section=international/all&site=topnews01"#연합뉴스 - readability fallback logic 사용해야함
    ]

    #런타임 시간 측정
    overall_start = time.time()
    for url in test_urls:
        print(f"\nExtracting content from: {url}")
        content = crawl(url)
        print(content)
        print("-" * 80)
    overall_elapsed = time.time() - overall_start
    print(f"\nTime taken to crawl {len(test_urls)} websites: {overall_elapsed:.2f} seconds")
