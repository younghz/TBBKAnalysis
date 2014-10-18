#/usr/bin/python
#-*-coding:utf-8-*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

from TBBKAnalysis.items import TbbkanalysisItem

class TBBKSpider(Spider):
    """淘宝爆款爬虫。"""

    name = "TBBKSpider"
    download_delay = 4
    allowed_domains = ["taobao.com"]
    start_urls = [
        "http://s.taobao.com"
        ]

    def parse(self, response):
        """override parse()."""
        #由于不能直接进入搜索页，这里先到首页然后进入搜索页
        if response.url == "http://s.taobao.com":
            print "********************response url:%s******************" %response.url
            #“连衣裙 女”的搜索页第一页
            url = "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&" \
                  "initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1#J_relative"
            log.msg("Page 1",level=log.INFO)
            yield Request(url,callback=self.parse)

        else:
            sel = Selector(response)
            #sel.remove_namespaces()
            #提取所有店铺
            shops = sel.xpath('//div[@class="tb-content"]/div[@class="row grid-view newsrp-gridcontent-el"]/div')
            print "*************response url:%s******************" %response.url
            #print "*************Find shops:******************"

            #逐一提取
            for shop in shops:
                item = TbbkanalysisItem()
                print "*************shop in shops******************"
                shop_name = shop.xpath('div[@class="item-box st-itembox"]/div[@class="row"]/div[1]/a/text()').extract()
                shop_address = \
                    shop.xpath('div[@class="item-box st-itembox"]/div[@class="row"]/div[2]/text()').extract()
                #最初的提取结果是list
                shop_istmall = \
                    shop.xpath('div[@class="item-box st-itembox"]/div[@class="row"]/div/@data-param').extract()
                #转换为dict类型
                shop_istmall = eval(shop_istmall[0])

                #提取isTmall元素判断是否是Tmall
                if shop_istmall["isTmall"] == 1:
                    shop_istmall = "is_tmall"
                else:
                    shop_istmall = "not_tmall"

                goods_price = \
                    shop.xpath('div[@class="item-box st-itembox"]/div/div[@class="col price"]/text()').extract()
                #取出其中的空格
                goods_price = goods_price[0].strip()
                goods_sale_num = \
                    shop.xpath('div[@class="item-box st-itembox"]/div/div[@class="col end dealing"]/text()').extract()
                #提取其中的数字
                goods_sale_num = "".join([s for s in goods_sale_num[0] if s.isdigit()])

                goods_name = shop.xpath('div[@class="item-box st-itembox"]/h3/a/@title').extract()
                #print "*************Find end******************"

                #编码
                item["shop_name"] = [n.encode("utf-8") for n in shop_name]
                item["shop_address"] = [a.encode("utf-8") for a in shop_address]
                #非list类型
                item["shop_istmall"] = shop_istmall
                item["goods_price"] = goods_price
                item["goods_sale_num"] = goods_sale_num
                item["goods_name"] = [na.encode("utf-8") for na in goods_name]

                yield item

            #其中遇到的问题：下一页以及第×页的链接和当前页链接相同，如果使用“复制链接地址”，并复制到地址栏中得到的还是当前页
            #所以这里采用的是直接拿到下一页地址

            #注：这里分析前5页，大概是销量大于3000的卖家
            #这里还可以使用另一种方式获取url，每个url的不同只体现在最后的数字，每页有44个商品，所以链接中数字代表当前页的地一个商品
            next_page_urls = [
                "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22"\
                            "initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=176",
                "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22"\
                            "initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=132",
                "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22"\
                            "initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=88",
                "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22"\
                            "initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=44"

            ]
            print "*******************next page**********************"
            log.msg("Next page", level=log.INFO)

            
            for next_page_url in next_page_urls:
                yield Request(next_page_url, callback=self.parse)
