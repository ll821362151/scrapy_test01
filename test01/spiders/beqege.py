from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest


class BeqegeSpider(CrawlSpider):
    name = 'beqege'
    allowed_domains = ['localhost:8080']
    start_urls = ['http://localhost:8080/']

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

    rules = (
        Rule(LinkExtractor(allow='.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)

    def parse_content(self, response):
        print(response.text)
