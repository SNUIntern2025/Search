from tavily_search import tavily_search

searchAPI_result = []

examples = [
    {
        "subquery": "애플 아이폰 최신모델",
        "routing": True
    },
    {
        "subquery": "아이폰 15 프로 가격",
        "routing": False
    },
    {
        "subquery": "아이폰 15 프로 맥스 스펙",
        "routing": False
    },
    {
        "subquery": "갤럭시 S24 울트라",
        "routing": True
    },
    {
        "subquery": "갤럭시 S24 출시일",
        "routing": False
    }
]

for query_data in examples:
    if query_data['routing'] == 'web':
        result = tavily_search(query_data['subquery'])

        searchAPI_result.append({
            'query': query_data['subquery'],
            'result': result
        })