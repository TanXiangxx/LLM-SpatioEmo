import pandas as pd
import folium

# Load Excel file
file_path = '情感分析结果_细粒度3.xlsx'
df = pd.read_excel(file_path)

# Set up color mapping for emotions
color_map = {
    'Positive': 'green',
    'Neutral': 'blue',
    'Negative': 'red'
}

# Convert Chinese emotion labels to English
label_translation = {
    '正面': 'Positive',
    '中性': 'Neutral',
    '负面': 'Negative'
}
df['Emotion'] = df['情绪标签'].map(label_translation)

# Initialize folium map centered at the mean location
map_center = [df['纬度'].mean(), df['经度'].mean()]
emotion_map = folium.Map(location=map_center, zoom_start=5)

# Add points to the map
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['纬度'], row['经度']],
        radius=3,
        color=color_map.get(row['Emotion'], 'gray'),
        fill=True,
        fill_opacity=0.7,
        popup=f"Emotion: {row['Emotion']}"
    ).add_to(emotion_map)

# Save map to HTML and open in browser
emotion_map.save('emotion_map2.html')
print("Map has been saved as emotion_map.html")
