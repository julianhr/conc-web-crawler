import sys
from .blocking.requester import requester
from .async_.crawler import Crawler as CrawlerAsync
from .blocking.crawler import Crawler as CrawlerBlocking


class Welcome:

    def __init__(self, debug=False):
        self.strategies = ['Threads', 'Async']
        self.crawler_args = {}
        self.crawler = None
        self.debug = debug

    @property
    def title(self):
        print('Simple Web Crawler\n')

    def set_url(self):
        while True:
            url = input('URL to crawl> ').strip()

            if self.debug:
                self.crawler_args['init_url'] = url
                break
            else:
                print('checking validity, wait...\n')

                if len(url) > 1 and url[-1] == '/':
                    url = url[:-1]

                try:
                    res = requester.head(url)

                    if res.ok:
                        self.crawler_args['init_url'] = url
                        break
                    else:
                        sys.exit(f"the URL {url} appears to be invald, try again.")
                except:
                    print('Unable to verify URL, try again')
                    continue

    def get_strategy(self):
        strategies = ' '.join([ f"\n{i+1} {s}" for i, s in enumerate(self.strategies) ])
        print(f"crawler strategy:{strategies}")

        while True:
            try:
                strategy = int(input('> '))

                if 1 <= strategy <= 2:
                    return strategy
                else:
                    raise ValueError()
            except:
                print('invalid option, try again.')

    def threads_factory(self):
        self.set_num_threads()
        self.set_time()
        return CrawlerBlocking(**self.crawler_args)

    def async_factory(self):
        self.set_time()
        return CrawlerAsync(**self.crawler_args)

    def set_num_threads(self):
        while True:
            try:
                num_threads = int(input('number of threads> '))

                if num_threads > 0:
                    self.crawler_args['num_threads'] = num_threads
                    break
                else:
                    raise ValueError()
            except Exception as err:
                print(err)
                print('threads must be a number greater than 0.')

    def set_time(self):
        while True:
            try:
                run_for_min = input('run for seconds (blank if forever)> ')

                if run_for_min:
                    self.crawler_args['run_for_sec'] = int(run_for_min)

                break
            except:
                print('enter minutes to run or leave empty if forever.')

    def interactive(self):
        self.title
        self.set_url()
        strategy = self.get_strategy()

        if strategy == 1:
            self.crawler = self.threads_factory()
        elif strategy == 2:
            self.crawler = self.async_factory()

        print()
