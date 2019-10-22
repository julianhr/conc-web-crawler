## Simple Web Scraper

Simple Python web scraper with option to use threads or event loop to fetch URL's.

### URL Requests

The threaded version uses the requests package. The async version uses Puppeteer via the Pyppeteer port to Python.

```zsh
(web_scraper) ➜  web_scraper git:(master) ✗ python main.py
Web Scraper

URL to scrape> https://www.washingtonpost.com/
scraper strategy:
1 Threads
2 Async
> 1
number of threads> 6
run for seconds (blank if forever)> 30

2019-10-21 19:40:13,861 [MainThread] scraper.py:31 Scraper started, initial URL: https://www.washingtonpost.com/
2019-10-21 19:40:13,862 [cons-1] crawler.py:26 thread cons-1 started
2019-10-21 19:40:13,863 [cons-2] crawler.py:26 thread cons-2 started
2019-10-21 19:40:13,863 [cons-1] crawler.py:42 process https://www.washingtonpost.com/
2019-10-21 19:40:13,864 [cons-3] crawler.py:26 thread cons-3 started
2019-10-21 19:40:13,864 [cons-4] crawler.py:26 thread cons-4 started
2019-10-21 19:40:13,865 [cons-5] crawler.py:26 thread cons-5 started
2019-10-21 19:40:13,866 [cons-6] crawler.py:26 thread cons-6 started
2019-10-21 19:40:32,989 [cons-2] crawler.py:42 process https://www.washingtonpost.com
2019-10-21 19:40:33,008 [cons-4] crawler.py:42 process https://www.washingtonpost.com/politics
2019-10-21 19:40:33,008 [cons-3] crawler.py:42 process https://www.washingtonpost.com/opinions
2019-10-21 19:40:33,008 [cons-5] crawler.py:42 process https://www.washingtonpost.com/national/investigations
2019-10-21 19:40:33,008 [cons-6] crawler.py:42 process https://www.washingtonpost.com/impeachment
```
