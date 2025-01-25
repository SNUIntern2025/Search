from tavily_search import tavily_search

searchAPI_result = []

for query_data in examples:
    if query_data['routing'] == 'web':
        result = tavily_search(query_data['subquery'])

        searchAPI_result.append({
            'query': query_data['subquery'],
            'result': result
        })