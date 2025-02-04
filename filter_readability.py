import requests
from readability import Document
from bs4 import BeautifulSoup

import time


url = 'https://ko.wikipedia.org/wiki/데이터_매트릭스'
response = requests.get(url)

start_time = time.time()

doc = Document(response.text)
main_content_html = doc.summary()

soup = BeautifulSoup(main_content_html, 'html.parser')
filtered_text = soup.get_text(separator='\n', strip=True)

end_time = time.time()

elapsed_time = end_time - start_time

print(filtered_text)
print(f'Elapsed time: {elapsed_time:.2f} sec')
