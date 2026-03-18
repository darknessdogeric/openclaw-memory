from scrapling.fetchers import Fetcher

url = 'https://www.mafengwo.cn/gonglve/'
print(f'Fetching: {url}')
fetcher = Fetcher()
page = fetcher.get(url)
print(f'Type: {type(page)}')
methods = [m for m in dir(page) if not m.startswith('_')][:20]
print(f'Methods: {methods}')
