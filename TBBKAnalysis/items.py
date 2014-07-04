#-*-coding:utf-8-*-

from scrapy.item import Item, Field

class TbbkanalysisItem(Item):
    """存储条目信息"""

    shop_name = Field()
    #是否是天猫店铺
    shop_istmall = Field()
    shop_address = Field()
    goods_name = Field()
    goods_price = Field()
    #是否免邮费
    #goods_free_postage = Field()
    #总价格，默认邮费10元
    #goods_total_price = Field()
    #商品卖出数量
    goods_sale_num = Field()

