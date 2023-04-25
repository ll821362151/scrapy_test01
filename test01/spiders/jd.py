import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
import re
import requests

lua_script = '''
function main(splash, args)

local ok, reason = splash:go(args.url)
user_name = args.user_name
user_passwd = args.user_passwd
user_text = splash:select("#email")
pass_text = splash:select("#pass")
login_btn = splash:select("#loginbutton")
if (user_text and pass_text and login_btn) then
    user_text:send_text(user_name)
    pass_text:send_text(user_passwd)
    login_btn:mouse_click({})
end

splash:wait(math.random(5, 10))
return {
    url = splash:url(),
    cookies = splash:get_cookies(),
    headers = splash.args.headers,
 }
end'''



class JdSpider(CrawlSpider):
    name = 'biqugedu'
    allowed_domains = ['biqugedu.com']
    start_urls = ['http://www.biqugedu.com/306_306183/']

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=False),
    )
    index = 0

    def parse_item(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )
        # print(response.url)

    def parse_link(self, response):
        self.index += 1
        img_url = response.xpath('//div[@id="fmimg"]/img/@src').get()
        title = response.xpath('//div[@id="info"]/h1/text()').get()
        if title:
            pic = requests.get(img_url, timeout=10)
            dir = 'E:/pic/' + title + ".jpg"
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()


