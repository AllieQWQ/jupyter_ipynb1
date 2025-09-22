import csv
import requests
import json

#1.请求连接
def get_one_page(url,header):
    res=requests.get(url,headers=header)
    return res.text
#   print(r)
#2.分析页面
def parse_one_page(js1):
    data_json=json.loads(js1)
    # print(data_json)
    for i in data_json:
        provice=i["ProvinceName"]
        PID=i["Id"]
        print(provice)
        yield provice,PID
def parse_second_page(PID,header):
        url2=f'https://air.cnemc.cn:18007/CityData/GetCitiesByPid?pid={PID}'
        r2=requests.get(url2,headers=header)
        return r2.text

def parse_city_data(r2):
        data_json2= json.loads(r2)
        for j in data_json2:
            CityCode=j["CityCode"]
            yield CityCode

def parse_third_page(CityCode,header):
            url3=f'https://air.cnemc.cn:18007/HourChangesPublish/GetCityDayAqiHistoryByCondition?citycode={CityCode}'
            data={'citycode':CityCode}
            r3=requests.post(url3, headers=header, json=data)
            return r3.text

def parse_aqi_data(r3):
            data_json3=json.loads(r3)
            for n in data_json3:
                date=n["TimePointStr"]
                Area=n["Area"]
                AQI=n["AQI"]
                PM25=n["PM2_5_24h"]
                print(date,Area,AQI,PM25)
                yield date,Area,AQI,PM25

def write_to_csv(content, path):
    with open(path,'a',newline="",encoding='utf-8-sig')as f1:
        f=csv.writer(f1)
        h1= ["省份","日期", "城市", "空气指标AQI", "PM_2.5"]
        if f1.tell()==0:  # 如果文件不存在或为空，写入表头
            f.writerow(h1)
        f.writerow(content)

if __name__=='__main__':
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'}
        url='https://air.cnemc.cn:18007/CityData/GetProvince'
        js1=get_one_page(url,header)
        for province, pid in parse_one_page(js1):
            r2 = parse_second_page(pid, header)
            for city_code in parse_city_data(r2):
                r3 = parse_third_page(city_code, header)
                for date, area, aqi, pm25 in parse_aqi_data(r3):
                    data = [province, date, area, aqi, pm25]
                    write_to_csv(data, "各市的空气指标优化版.csv")

