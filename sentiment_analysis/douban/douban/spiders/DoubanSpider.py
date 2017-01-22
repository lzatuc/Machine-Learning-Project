from scrapy import Selector
from scrapy import Spider

from ..items import DoubanItem
import scrapy
from scrapy import Request
from scrapy import FormRequest

class DoubanSpider(Spider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/subject/26879060/comments?start=0&limit=20&sort=new_score&status=P']
    douban_login_url = 'https://accounts.douban.com/login?source=movie'
    user_account = '719807680@qq.com'
    user_password = '123456ab'

    def start_requests(self):
        yield Request(url=self.douban_login_url, meta={'cookiejar': 1}, callback=self.post_login)

    def post_login(self, response):
        print('Preparing login')
        sel = Selector(response)
        nodes = sel.xpath("//*[@class='captcha_image']/@src").extract()
        if nodes:
            print('nodes = ', nodes)
            xerf = input()
            return FormRequest.from_response \
                    (
                    response,
                    formdata={
                        'captcha-solution': xerf,
                        'form_email': self.user_account,
                        'form_password': self.user_password
                    },
                    callback=self.after_login
                )
        return FormRequest.from_response(
                response,
                formdata={
                    'form_email': self.user_account,
                    'form_password': self.user_password
                },
                callback = self.after_login
        )

    def after_login(self, response):
        # if "个性域名格式不正确" in response.content:
        #     self.log("login failed")
        for url in self.start_urls:
            print(url)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        selector = Selector(response)
        movie_name = selector.xpath('//title/text()').extract_first().split()[0]

        comment_infos = selector.xpath('//span[@class="comment-info"]')
        comments = selector.xpath('//p[@class=""]/text()[1]')

        for comment_info, commentSection in zip(comment_infos, comments):
            commenter = comment_info.xpath('./a/text()').extract_first()
            starOption = comment_info.xpath('./span[starts-with(@class, "allstar")]/@class').extract_first()
            if starOption:
                star = int(starOption.split()[0][7:9]) / 10
            else:
                star = 3.0  # neutral attitude

            comment_time = comment_info.xpath('./span[@class="comment-time "]/text()').extract_first()
            comment = commentSection.extract()

            item = DoubanItem()
            item['movie_name'] = movie_name.strip()
            item['comment'] = comment.strip()
            item['star'] = star
            item['commenter'] = commenter.strip()
            item['comment_time'] = comment_time.strip()
            yield item

        next_page = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
