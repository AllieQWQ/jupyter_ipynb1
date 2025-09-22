# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import pymysql
class JdProgramPipeline:
    def process_item(self, item, spider):
        with open('goods.csv','a',newline='',encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow([item['userId'],item['userName'],item['productType'],item['contentEva'],
                                 item['buyTime'],item['rankTime'],item['voteCount'],item['replyCount'],item['scoreTotal']])
        print('存入数据')    
        return item

class MySQLPipeline():
    def open_spider(self,spider):
        #1、创建数据库链接对象connect
        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1024',
            db='goods_data',
            charset='utf8'
        )

        #2、获取游标对象 cursor
        self.cursor = self.db.cursor()
        
    def process_item(self,item,spider):
        #插入数据
        insert_sql = """
        insert into goods(userId,userName,productType,contentEva,buyTime,rankTime,voteCount
                  ,replyCount,scoreTotal) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        try:
            
            self.cursor.executemany(insert_sql,item)
            self.db.commit()
            print(item["userId"]+"...成功写入数据库..")
        except:
            self.db.rollback()
        

        