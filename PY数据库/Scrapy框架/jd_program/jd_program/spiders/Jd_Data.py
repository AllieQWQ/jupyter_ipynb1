import scrapy
import json
from ..items import JdProgramItem

class JdDataSpider(scrapy.Spider):
    name = "Jd_Data1"
    allowed_domains = ["www.jd.com"]
    start_urls = ["https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100110745685&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"]

    def parse(self, response):
        content = response.text
        #print(response.text)
        start_local = content.find('{')
        end_local = -2
        json_data = content[start_local:end_local]
        data = json.loads(json_data)

        for i in data['comments']:
            #遍历每一行的商品评论数据
            userId = i['id']
            userName = i['nickname']
            productType = i['productColor']
            contentEva = i['content']
            buyTime = i['referenceTime']
            rankTime = i['creationTime']
            voteCount = i['usefulVoteCount']
            replyCount = i['replyCount']
            scoreTotal = i['score']

            print(userId,userName,productType,contentEva,buyTime,rankTime,voteCount
                  ,replyCount,scoreTotal)

            # 返回上一级的文件并导入类名 若item实例化改变 则item里属性也要改变
            item = JdProgramItem()
            item['userId'] = userId
            item['userName'] = userName
            item['productType'] = productType
            item['contentEva'] = contentEva
            item['buyTime'] = buyTime
            item['rankTime'] = rankTime
            item['voteCount'] = voteCount
            item['replyCount'] = replyCount
            item['scoreTotal'] = scoreTotal
            yield item
            
