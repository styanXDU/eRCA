import requests
import json


class DoubanSpider():
    def __init__(self, url):
        self.start_url = url

    def get_content(self, url):
        c = []
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        html_str = response.content.decode()
        json_str = json.loads(html_str)
        print(json_str)
        for i in range(len(json_str.get('subjects'))):
            a = json_str.get('subjects')[i]
            b = a.get('absolute-link')
            c.append(b)
        print(c)
        return c

    def save_content(self, c):
        with open('doubanriju.json', 'a', encoding='utf_8') as f:
            f.write(json.dumps(c, ensure_ascii=False))
        print('写入成功')

    def run(self):
        url = self.start_url
        c = self.get_content(url)
        self.save_content(c)


if __name__ == '__main__':
    douban = DoubanSpider('https://bbs.sangfor.com.cn/plugin.php?id=case_databases:index&cpid=4')
    douban.run()
