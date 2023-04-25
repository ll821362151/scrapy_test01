from bs4 import BeautifulSoup
import requests
import re
import json

res = requests.get("https://www.xuexi.cn/89acb6d339cd09d5aaf0c2697b6a3278/data9a3668c13f6e303932b5e0e100fc248b.js")
# res = requests.get("https://www.xuexi.cn/89acb6d339cd09d5aaf0c2697b6a3278/data9a3668c13f6e303932b5e0e100fc248b.js")
# res.encoding = 'utf-8'
# for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
#     if key != 'sysQuery':
#         for item in  value['list']:
#             print(item['static_page_url'], item['frst_name'])
