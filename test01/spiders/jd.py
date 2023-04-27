from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
import requests
from test01.spiders.utils.constant import Constants

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
    start_urls = ['http://www.biqugedu.com/49_49836/']

    rules = (
        Rule(LinkExtractor(allow='.*'), callback='parse_item', follow=True),
    )
    index = 0

    def parse_item(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            print(link.url)
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'wait': 30,
                    "lua_source": lua_script,
                    'har': 1,
                    'html': 1,
                }
            )
        print(response.body)

    def parse_link(self, response):
        self.index += 1
        img_url = response.xpath('//div[@id="fmimg"]/img/@src').get()
        title = response.xpath('//div[@id="info"]/h1/text()').get()
        if title:
            pic = requests.get(img_url, timeout=10)
            file_dir = Constants.FILE_PATH + 'pic/' + title + ".jpg"
            fp = open(file_dir, 'wb')
            fp.write(pic.content)
            fp.close()
