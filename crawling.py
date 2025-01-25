import re
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import asyncio

def crawling(response, max_length = 20000):
    links = [result['url'] for result in response if 'youtube' not in result['url'].lower()]

    print(links)

    loop = asyncio.get_event_loop()
    loader = AsyncHtmlLoader(links)
    docs = loop.run_until_complete(loader.aload())

    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs,
        unwanted_tags=[
            "script", "style", "nav", "footer", "header",
            "aside", "button", "form", "input", "iframe",
            "noscript", "img", "svg", "path"
            ],
        tags_to_extract=["div.content","main.content","p"],
        unwanted_classnames=[
            "advertisement", "sidebar", "menu", "navigation",
            "footer", "header", "social", "comments"
            ],
        remove_lines=True,
        remove_comments=True
        )

    cleaned_texts = []

    # 주헌 : 여기 부분부터 수정..

    for doc in docs_transformed:
        text = doc.page_content
        text = re.sub(r'\(https?://[^)]+\)', "", text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        if len(text) > 100:
            cleaned_texts.append(text)

        combined_text = ' '.join(cleaned_texts)

        if len(combined_text) > max_length:
            final_text = combined_text[:max_length].rsplit('.', 1)[0] + '.'
        else:
            final_text = combined_text

    return final_text