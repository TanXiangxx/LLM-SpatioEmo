import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import matplotlib.colors as mcolors

# 读取数据
data = pd.read_excel('eat2_mood.xlsx')

# 定义新的经纬度范围，扩大0.01
lat_min, lat_max = 39.522469 - 0.01, 40.690334 + 0.01  # 纬度范围扩大0.01
lon_min, lon_max = 115.90368 - 0.01, 117.150689 + 0.01  # 经度范围扩大0.01

# 设置网格大小
grid_size = 0.05  # 每个网格代表的经纬度差距

# 创建网格
lat_bins = np.round(np.arange(lat_min, lat_max + grid_size, grid_size), 3)
lon_bins = np.round(np.arange(lon_min, lon_max + grid_size, grid_size), 3)

# 使用 pd.cut 分配数据点到网格中
data['lat_grid'] = pd.cut(data['纬度'], lat_bins, include_lowest=True, right=False)
data['lon_grid'] = pd.cut(data['经度'], lon_bins, include_lowest=True, right=False)

# 计算每个网格内不同情绪标签的数量
grid_emotion_counts = data.groupby(['lat_grid', 'lon_grid', '情绪标签']).size().unstack(fill_value=0)

# 计算每个网格的情绪分，例如：根据比例来衡量情绪的强度
# 计算每个网格的情绪分： (正面 - 负面) / (正面 + 负面 + 中性)
w_pos = 2.3
w_neu = 1
w_neg = 1.2

grid_emotion_counts['emotion_score'] = (
    (w_pos * grid_emotion_counts['正面']) - (w_neg * grid_emotion_counts['负面'])
) / (
    (w_pos * grid_emotion_counts['正面']) +
    (w_neu * grid_emotion_counts['中性']) +
    (w_neg * grid_emotion_counts['负面'])
)

# 处理 NaN 值，确保有数据时才计算情绪分数
grid_emotion_counts['emotion_score'].fillna(0, inplace=True)


# 创建颜色映射，情绪分的范围从 -1 到 1，负面情绪为红色，正面为绿色
cmap = plt.get_cmap("RdYlGn_r")
norm = mcolors.Normalize(vmin=-1, vmax=1)

# 加载北京市的行政区划地图（从提供的 GeoJson 文件）
shapefile_path = '北京.geoJson'  # 使用上传的文件路径
beijing = gpd.read_file(shapefile_path)

# 绘制情绪标签地图
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制北京市的行政区地图
beijing.plot(ax=ax, color='lightgrey')

# 设置绘制区域为北京市范围
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)

# 绘制每个网格并根据情绪分着色
for i in range(len(lat_bins) - 1):  # 避免最后一个超出范围
    for j in range(len(lon_bins) - 1):
        # 使用与 pd.cut 相同的区间属性：左闭右开
        lat_interval = pd.Interval(lat_bins[i], lat_bins[i + 1], closed='left')
        lon_interval = pd.Interval(lon_bins[j], lon_bins[j + 1], closed='left')

        
        # 根据经纬度区间查找情绪分数
        if (lat_interval, lon_interval) in grid_emotion_counts.index:
            grid_emotion = grid_emotion_counts.loc[(lat_interval, lon_interval), 'emotion_score']

        else:
            grid_emotion = 0  # 如果该网格内没有数据，则设置情绪分为0
        
        color = cmap(norm(grid_emotion))  # 获取该网格对应的颜色
        
        # 创建每个网格的矩形
        square = Polygon([(lon_bins[j], lat_bins[i]), (lon_bins[j + 1], lat_bins[i]), 
                          (lon_bins[j + 1], lat_bins[i + 1]), (lon_bins[j], lat_bins[i + 1])])
        ax.add_patch(plt.Polygon(list(square.exterior.coords), color=color, alpha=0.5))

# 添加图例和标题
plt.legend()
plt.title("Emotion Distribution of Restaurants in Beijing")
#Emotion Distribution of Tourist Attractions in Beijing
#Emotion Distribution of Social and Entertainment Venues in Beijing
plt.xlabel("Longitude")
plt.ylabel("Latitude")
 
# 显示地图
plt.show()
  