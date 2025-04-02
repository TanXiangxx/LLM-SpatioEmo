import pandas as pd
import requests
import time
import urllib.parse

GAODE_KEY = 'e9464ef761139d192d713ef77834aa4d'

def gaode_geocode(address):
    full_address = f"北京市{address}"
    url = f"https://restapi.amap.com/v3/geocode/geo?address={urllib.parse.quote(full_address)}&output=json&key={GAODE_KEY}"

    try:
        response = requests.get(url).json()
        if response['status'] == '1' and int(response['count']) > 0:
            location = response['geocodes'][0]['location']
            lng, lat = map(float, location.split(','))
            return pd.Series([lat, lng])
        else:
            return None  # 地理编码失败，返回 None
    except:
        return None

def gaode_poi_fallback(address):
    # 使用关键词模糊搜索（最多返回1条）
    keyword = urllib.parse.quote(address[:30])
    url = f"https://restapi.amap.com/v3/place/text?keywords={keyword}&city=北京&key={GAODE_KEY}"
    
    try:
        response = requests.get(url).json()
        if response['status'] == '1' and int(response['count']) > 0:
            location = response['pois'][0]['location']
            lng, lat = map(float, location.split(','))
            print(f"✅ 使用POI兜底成功：{address}")
            return pd.Series([lat, lng])
        else:
            print(f"❌ 完全无法识别：{address}")
            return pd.Series([None, None])
    except Exception as e:
        print(f"Error in POI fallback at {address}: {e}")
        return pd.Series([None, None])

def get_latlng(addr):
    result = gaode_geocode(addr)
    if result is None:
        result = gaode_poi_fallback(addr)
    else:
        time.sleep(0.2)
    return result

if __name__ == '__main__':
    df = pd.read_excel('./data/eat.xlsx')
    df[['纬度', '经度']] = df['address'].apply(get_latlng)
    df.to_excel('./address_with_latlng_gaode_fallback.xlsx', index=False)
    print("✅ 高德地理编码 + POI兜底 完成，结果保存在 address_with_latlng_gaode_fallback.xlsx")
