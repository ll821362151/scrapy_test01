import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
import re
import os
from test01.spiders.utils.constant import Constants
import requests


class ZcoolSpider(CrawlSpider):
    name = 'zcool_login'
    allowed_domains = ['zcool.com.cn']
    start_urls = ['https://passport.zcool.com.cn/loginApp.do?appId=1006&cback=https://www.zcool.com.cn/']
    # start_urls = ['https://www.zcool.com.cn/']
    index = 0

    rules = (
        Rule(
            LinkExtractor(allow='https://passport.zcool.com.cn/loginApp.do?appId=1006&cback=https://www.zcool.com.cn/'),
            callback='parse1', follow=True),
    )
    lua_source = '''
    function main(splash, args)
        -- 访问登录页面
        splash:go(args.url)
        splash:wait(1)

        -- 输入用户名和密码
        local input_user = splash:select('#input_user')
        input_user:send_text(args.username)
        local input_pass = splash:select('#input_pass')
        input_pass:send_text(args.password)

        -- 点击登录按钮
        local login_button = splash:select('#login_button')
        login_button:mouse_click()
        
        -- 等待页面跳转
        splash:wait(2)

        -- 获取登录后的cookies
        local cookies = splash:get_cookies()
        return {cookies=cookies}
    end
    '''

    def start_requests(self):
        url = 'http://localhost:8050/run'
        args = {
            'lua_source': self.lua_source,
            'url': 'https://example.com/login',
            'username': 'your_username',
            'password': 'your_password'
        }

        response = requests.post(url, json=args)
        print(response.json())
        # splah_args = {
        #     "lua_source": self.lua_source
        # }
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #                   'Chrome/72.0.3626.109 Safari/537.36',
        # }
        # for url in self.start_urls:
        #     print('start_urls:' + url)
        #     yield SplashRequest(url=url, callback=self.parse_item,
        #                         headers=headers,
        #                         endpoint='render.json',
        #                         args={
        #                             'har': 1,
        #                             'html': 1,
        #                         })

    def parse_item(self, response):
        print(response.body)
        pass
