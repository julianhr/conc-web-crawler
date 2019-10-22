## Simple Web Crawler

Simple Python web crawler with option to use threads or event loop to fetch URL's.

### URL Requests

The threaded version uses the requests package. The async version uses Puppeteer via the Pyppeteer port to Python.

### Installation

```python
cd /path/to/crawler
pip install pipenv
pipenv install
pipenv shell
```

### Launching app

```log
(web_crawler) ➜  web_crawler git:(master) ✗ python main.py
Simple Web Crawler

URL to crawl> https://www.nytimes.com/
crawler strategy:
1 Threads
2 Async
> 1
number of threads> 4
run for seconds (blank if forever)> 20

2019-10-21 21:34:51,368 [MainThread] crawler.py:31 Crawler started, initial URL: https://www.nytimes.com/
2019-10-21 21:34:51,368 [cons-1] scraper.py:26 thread cons-1 started
2019-10-21 21:34:51,368 [cons-1] scraper.py:42 process https://www.nytimes.com/
2019-10-21 21:34:51,369 [cons-2] scraper.py:26 thread cons-2 started
2019-10-21 21:34:51,369 [cons-3] scraper.py:26 thread cons-3 started
2019-10-21 21:34:51,369 [cons-4] scraper.py:26 thread cons-4 started
2019-10-21 21:34:51,871 [cons-2] scraper.py:42 process https://www.nytimes.com/
2019-10-21 21:34:51,872 [cons-2] scraper.py:42 process https://www.nytimes.com/
2019-10-21 21:34:52,379 [cons-2] scraper.py:42 process https://www.nytimes.com/es
2019-10-21 21:34:52,379 [cons-3] scraper.py:42 process https://cn.nytimes.com
2019-10-21 21:34:52,662 [cons-2] requester.py:36 <urllib3.response.HTTPResponse object at 0x10f6c5a50>
2019-10-21 21:34:52,836 [cons-2] requester.py:36 <urllib3.response.HTTPResponse object at 0x10fa96c10>
2019-10-21 21:34:52,882 [cons-4] scraper.py:42 process https://myaccount.nytimes.com/auth/login
2019-10-21 21:34:53,025 [cons-2] requester.py:36 <urllib3.response.HTTPResponse object at 0x10fb99110>
2019-10-21 21:34:53,025 [cons-2] page_processor.py:27 <urllib3.response.HTTPResponse object at 0x10fb99110>
2019-10-21 21:34:53,026 [cons-2] scraper.py:42 process https://myaccount.nytimes.com/auth/login
2019-10-21 21:34:53,026 [cons-2] scraper.py:42 process https://www.nytimes.com/section/todayspaper
2019-10-21 21:34:53,164 [cons-4] scraper.py:42 process https://www.nytimes.com/
2019-10-21 21:34:53,164 [cons-4] scraper.py:42 process https://www.nytimes.com/
2019-10-21 21:34:53,164 [cons-4] scraper.py:42 process https://www.nytimes.com/section/world
2019-10-21 21:34:53,455 [cons-3] scraper.py:42 process https://www.nytimes.com/section/us
2019-10-21 21:34:54,611 [cons-1] scraper.py:42 process https://www.nytimes.com/section/politics
2019-10-21 21:34:54,611 [cons-3] scraper.py:42 process https://www.nytimes.com/section/nyregion
2019-10-21 21:34:54,613 [cons-4] scraper.py:42 process https://www.nytimes.com/section/business
2019-10-21 21:34:54,618 [cons-2] scraper.py:42 process https://www.nytimes.com/section/opinion
2019-10-21 21:34:55,154 [cons-2] scraper.py:42 process https://www.nytimes.com/section/technology
2019-10-21 21:34:55,159 [cons-1] scraper.py:42 process https://www.nytimes.com/section/science
2019-10-21 21:34:55,160 [cons-3] scraper.py:42 process https://www.nytimes.com/section/health
2019-10-21 21:34:55,165 [cons-4] scraper.py:42 process https://www.nytimes.com/section/sports
2019-10-21 21:34:55,631 [cons-1] scraper.py:42 process https://www.nytimes.com/section/arts
2019-10-21 21:34:55,632 [cons-3] scraper.py:42 process https://www.nytimes.com/section/books
2019-10-21 21:34:55,638 [cons-4] scraper.py:42 process https://www.nytimes.com/section/style
2019-10-21 21:34:56,071 [cons-4] scraper.py:42 process https://www.nytimes.com/section/food
2019-10-21 21:34:56,174 [cons-1] scraper.py:42 process https://www.nytimes.com/section/travel
2019-10-21 21:34:56,219 [cons-3] scraper.py:42 process https://www.nytimes.com/section/magazine
2019-10-21 21:34:56,371 [cons-4] scraper.py:42 process https://www.nytimes.com/section/t-magazine
2019-10-21 21:34:56,384 [cons-2] scraper.py:42 process https://www.nytimes.com/section/realestate
2019-10-21 21:34:56,610 [cons-1] scraper.py:42 process https://www.nytimes.com/video
2019-10-21 21:34:56,610 [cons-1] scraper.py:63 Queue size: 3650
2019-10-21 21:34:56,626 [cons-3] scraper.py:42 process https://www.nytimes.com/section/world
2019-10-21 21:34:56,626 [cons-3] scraper.py:42 process https://www.nytimes.com/section/us
...
```
