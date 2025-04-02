import pandas as pd
import requests
import time
import urllib.parse

BAIDU_AK = 'j23PTlGhTpqEZi0WMbEHqzjuDKevgtOv'

def baidu_geocode(address):
    if pd.isna(address):
        return pd.Series([None, None])
    
    # 编码地址（百度API要求URL编码）
    address_encoded = urllib.parse.quote(f"北京市{address}")
    
    url = f"http://api.map.baidu.com/geocoding/v3/?address={address_encoded}&output=json&ak={BAIDU_AK}"
    
    try:
        response = requests.get(url).json()
        if response['status'] == 0:
            lat = response['result']['location']['lat']
            lng = response['result']['location']['lng']
            return pd.Series([lat, lng])
        else:
            print(f"❌ 百度无法识别：{address}")
            return pd.Series([None, None])
    except Exception as e:
        print(f"Error at {address}: {e}")
        return pd.Series([None, None])

# 读取地址表格
df = pd.read_excel('./data/eat.xlsx')

# 开始转经纬度
df[['纬度', '经度']] = df['address'].apply(baidu_geocode)
df.to_excel('./address_with_latlng_baidu.xlsx', index=False)
