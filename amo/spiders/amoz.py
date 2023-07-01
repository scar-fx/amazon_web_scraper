import scrapy
from time import sleep
from amo.items import product_items

class AmozSpider(scrapy.Spider):
    name = "amoz"
    allowed_domains = ["www.amazon.com"]
    #start_urls = ["https://www.amazon.com/s?k=t-shirt"]
    page = 1

    def start_requests(self):
        word = 'gaming mouse'
        word = word.replace(' ', '+')
        full_url = "https://www.amazon.com/s?k=" + word + '&page=1'
        page = 1
        yield scrapy.Request(full_url, callback=self.parse,cb_kwargs={'page_number': page,
                                                                      'word': word}, dont_filter=True)

    def parse(self, response, page_number, word):
        items = response.css('div [data-component-type="s-search-result"]')
        # next_page = response.css('span .s-pagination-strip a ::attr(href)').get()
        page_number += 1
        for item in items:
            sleep(2)
            n = {}
            # url
            nex = item.css('h2 a ::attr(href)').get()
            next_url = "https://www.amazon.com" + nex
            # text
            n['name'] = item.css('h2 a span ::text').get()
            # rating
            n['rating'] = item.css('div .a-row span ::attr(aria-label)').get()
            # num of ratings
            n['number_of_ratings'] = item.css('div .a-row span ::attr(aria-label)')[1].get()

            yield response.follow(next_url, callback=self.parse_page, cb_kwargs={'pd': n,
                                                                                 'link': next_url}, dont_filter=True)

        if page_number <= 20:
            sleep(2)
            next_page_url = "https://www.amazon.com/s?k=" + word + f'&page={page_number}'
            yield response.follow(next_page_url, callback=self.parse, cb_kwargs={'page_number': page_number,
                                                                                 'word': word},
                                  dont_filter=True)
        else:
            print(" the end")

    def parse_page(self, response, pd, link):

        products = product_items()

        products['name'] = pd['name']
        products['rating'] = pd['rating']
        products['price'] = response.css('span .a-offscreen ::text').get()
        products['number_of_ratings'] = pd['number_of_ratings']
        products['url'] = link

        yield products


