# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#在 item 类 中定义相关属性
class JdProgramItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userId = scrapy.Field()
    userName = scrapy.Field()
    productType = scrapy.Field()
    contentEva = scrapy.Field()
    buyTime = scrapy.Field()
    rankTime = scrapy.Field()
    voteCount = scrapy.Field()
    replyCount = scrapy.Field()
    scoreTotal = scrapy.Field()
    #pass
