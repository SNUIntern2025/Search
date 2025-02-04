# Search

## 1. Website Content Extractor

crawl_pipline.py is a web content extractor that retrieves the main textual content from various websites, such as arXiv abstracts and Korean Wikipedia articles. If a website is not recognized, it uses a fallback method with the Readability library to extract the most relevant text.

### Installation

Ensure you have Python installed, then install dependencies using:

```sh
pip install -r requirements.txt
```

#### Usage

Run the script with test URLs:

```sh
python crawl_pipeline.py
```

It will extract content from predefined test URLs(if not, uses a fallback method) and display the extracted text.

### How to Add Support for New Websites

To add a new website, follow these steps:

1. **Define a handler function**: Create a function that takes a URL and returns the extracted content. For example:

   ```python
   def handle_example(url):
        #handling logic

        return text
   ```

2. **Register the new handler**: Add an entry to the `KNOWN_SITE_HANDLERS` dictionary:
   ```python
   KNOWN_SITE_HANDLERS[r"example\.com"] = handler_example
   ```
3. **Test the handler**: Add a test URL in the `test_urls` list and run the script.

### Example Output

```
Extracting content from: https://arxiv.org/abs/2401.12345
(Abstract text displayed)

Extracting content from: https://ko.wikipedia.org/wiki/데이터_매트릭스
(Wikipedia article text displayed)

Extracting content from: https://www.yna.co.kr/view/AKR20250204076400009
(Fallback extraction text displayed)
```

### Performance

The script measures execution time to evaluate crawling efficiency:

```
Time taken to crawl 3 websites: 0.9 seconds
```
