import pandas as pd
import numpy as np
import pymysql
#1.读取csv文件
df = pd.read_csv('各市的空气指标优化版.csv')
# print(df)

#2.按照省份分组后再对每个省份求“空气指标AQI","PM_2.5"的均值
df=df.groupby("省份")["空气指标AQI","PM_2.5"].mean().reset_index()
#将均值结果保留小数点后两位
df[['空气指标AQI', 'PM_2.5']] = df[['空气指标AQI', 'PM_2.5']].round(2)

#a是一个 Series 对象，它包含多个值，而不是单个值，所以不能直接在 if 语句中使用它,
# 可以使用 .apply() 方法来对 Series 中的每个元素应用一个函数
def get_air_quality(a):
    if 0 <= a <= 50:
        return "优"
    elif 51 <= a <= 100:
        return "良"
    elif 101 <= a <= 150:
        return "轻度污染"
    elif 151 <= a <= 200:
        return "中度污染"
    elif 201 <= a <= 300:
        return "重度污染"
    else:
        return"严重污染"
# 应用函数到 AQI 列，并创建一个新的列 '空气质量等级'
df['空气质量等级'] = df['空气指标AQI'].apply(get_air_quality)
print(df)

# 3.将日期分为两个时间段

# 4. 保存结果
df.to_csv('AQI周期均值测试版.csv', index=False,encoding='utf-8-sig')

#保存至数据库
db = pymysql.connect(
    host='192.168.40.135',
    port=3306,
    user='root',
    passwd='123456',
    db='AirAQI',
    charset='utf8'
    )
cursor = db.cursor()
# 插入数据
sql = 'INSERT INTO airAOI (province,AOI,PM25,airMass) VALUES (%s, %s, %s, %s)'

try:
    for index, row in df.iterrows():#index用于在循环中存储当前行的索引,iterrows用于逐行遍历DataFrame
        cursor.execute(sql, (row['省份'], row['空气指标AQI'], row['PM_2.5'],row['空气质量等级']))
    db.commit()
except Exception as e:
    print(f"An error occurred: {e}")
    db.rollback()

# 关闭
cursor.close()
db.close()