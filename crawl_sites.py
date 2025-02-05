
import requests
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from readability import Document
import time


def handle_SOF(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find_all('div', class_ = 's-prose js-post-body')
    extracted_data = []

    if main_content:
        for item in main_content:
            item = item.find_all(["p", "pre"], recursive=False)
            for tag in item: 
                if tag.name == "p":
                    paragraph_text = []
                    for elem in tag.descendants:
                        if elem.name == "a" and elem.get("href"):  
                            paragraph_text.append(f"{elem.get_text(strip=True)} ({elem['href']})")  # Append link with text
                        elif isinstance(elem, str):  
                            paragraph_text.append(elem.strip())  # Append normal text
                    
                    extracted_data.append(" ".join(paragraph_text))


                elif tag.name == "pre":
                    code_tag = tag.find("code")
                    if code_tag:
                        extracted_data.append(code_tag.get_text(strip=True)) 

    else:
        print("Main content container not found.")
        return fallback_extraction(url)
    
    extracted_data = "\n".join(extracted_data)
    return extracted_data

def handle_velog(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.body.find('script')
    if main_content:
        main_content = main_content.get_text(strip=True)
        json_str = main_content.split("window.__APOLLO_STATE__=")[-1].strip()  # Extract JSON part
        match = re.search(r'"body"\s*:\s*"((?:\\.|[^"\\])*)"', json_str)
        if match:
            main_content = match.group(1)
            main_content = main_content.replace(r'\n', '\n').replace(r'\t', '\t')
            return main_content

    else:
        print("Main content container not found.")
        return fallback_extraction(url)


def handle_tistory(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find('div', class_='tt_article_useless_p_margin contents_style')
    if main_content:
        for tag in main_content.find_all(["br"], recursive=False):
            tag.decompose()

    else:
        print("Main content container not found.")
        return fallback_extraction(url)

    for tag in main_content.find_all("pre"): 
        code_tag = tag.find("code")
        if code_tag:
            tag.replace_with(code_tag.get_text(strip=True))
    main_content = main_content.get_text(strip=True)
    
    return main_content  #text 임

def handle_daum_news(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find('div', class_='article_view')
    if main_content:
        for tag in main_content.find_all(["figure"]):
            tag.decompose()
        main_content = main_content.get_text(strip=True)

    else:
        print("Main content container not found.")
        return fallback_extraction(url)
    
    return main_content  #text 임

def handle_naver_news(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # find the main content that holds the article text
    main_content = soup.find('article', class_='go_trans _article_content', id = 'dic_area')
    if main_content:
        for tag in main_content.find_all(["span", "img", "br", "beta"]):
            tag.decompose()
        main_content = main_content.get_text(strip=True)
        

    else:
        print("Main content container not found.")
        return fallback_extraction(url)
    
    return main_content  #text 임

# --- 현재까지 main content의 위치가 파악된 사이트 모음 ---

# 주헌 : 확장성을 고려해서 사이트 패턴과 핸들러를 딕셔너리로 관리하도록 만들어봤습니다.
KNOWN_SITE_HANDLERS = {
    # r"arxiv\.org": handle_arxiv,
    # r"ko\.wikipedia\.org": handle_kor_wikipedia,
    r"n\.news\.naver\.com/article" : handle_naver_news,
    r"v\.daum\.net/v" : handle_daum_news, 
    r"\.tistory\.com": handle_tistory, 
    r"velog\.io/" : handle_velog, 
    r"stackoverflow\.com/": handle_SOF
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
    doc = Document(response.text)
    main_content_html = doc.summary()
    soup = BeautifulSoup(main_content_html, 'html.parser')
    filtered_text = soup.get_text(separator='\n', strip=True)
    print(filtered_text)
    return filtered_text


def crawl(url):
    """
    실제 크롤링 함수 - 여기에 로직을 추가할 수 있음
    주헌 : google search API를 통해 받아온 url을 인자로 사용하면 될 것 같습니다
    """
    # check if the URL matches any known site patterns
    result = dispatch_known_site(url)
    if result:
        return result

    # fallback logic (logic2에 해당되는 경우)
    return fallback_extraction(url)

# -------------- 테스트 코드 -------------------

if __name__ == "__main__":

    # 주헌 : 여기에 테스트 URL을 추가하면 됩니다
    test_urls = [
        "https://stackoverflow.com/questions/79411372/getting-a-2nd-iasyncenumerator-from-the-same-iasyncenumerable-based-on"
        #"https://velog.io/@boseung/velog%EA%B0%9C%EB%B0%9C%EB%B8%94%EB%A1%9C%EA%B7%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EA%B3%BC%EC%A0%95-%EC%82%BD%EC%A7%88%EA%B8%B0%EB%A1%9D"
        #"https://augustfamily.tistory.com/108"
        #"https://v.daum.net/v/20250204175018118"
        #"https://n.news.naver.com/article/003/0013046572?cds=news_media_pc"
    ]

    # 런타임 시간 측정
    start_time = time.time()
    for url in test_urls:
        print(f"\nExtracting content from: {url}")
        content = crawl(url)
        print(content)
        print("-" * 80)

    total_elapsed = time.time() - start_time
    print(f"\nTime taken to crawl {len(test_urls)} websites: {total_elapsed:.2f} seconds")

# --------------------------------------------