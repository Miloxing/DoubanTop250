import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import re
import json


def get_one_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<li>.*?em.*?>(\d+)</em>.*?src="(.*?)".*?info'
                         + '.*?title">(.*?)</span>.*?<p.*?>(.*?)<br>(.*?)</p>'
                         + '.*?star.*?average">(.*?)</span>.*?inq">(.*?)<.*?</p>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'director': item[3].strip().split('&nbsp;')[0][3:],
            'actor': item[3].strip().split('&nbsp;')[-1][3:],
            'time': item[4].strip().split('&nbsp;')[0],
            'country': item[4].strip().split('&nbsp;')[2],
            'type': item[4].strip().split('&nbsp;')[4],
            'star': item[5],
            'quote': item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(start):
    url = 'https://movie.douban.com/top250?start=' + str(start)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*25 for i in range(10)])
