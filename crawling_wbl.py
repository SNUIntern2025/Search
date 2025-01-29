import bs4
from langchain_community.document_loaders import WebBaseLoader
import asyncio

async def crawling(response):
    links = [result['url'] for result in response if 'youtube' not in result['url'].lower()]

    print(links)

    loader = WebBaseLoader(
    web_path=links,
    requests_per_second = 1,
    default_parser='html.parser',
    bs_kwargs={
        'from_encoding': 'utf-8',
        'parse_only': bs4.SoupStrainer(['div', 'main']),
        },
    bs_get_text_kwargs={
        "separator": "",
        "strip": True
        }
    )

    docs = await loader.aload()
    
    return docs

#함수 실행 방법(추후에 합칠 때 사용)
#result = asyncio.run(crawling(response))