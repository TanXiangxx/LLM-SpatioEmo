import os
import pandas as pd

# 设置目标文件夹路径
folder_path = 'eat_origin'  # 文件夹名为 eat_origin

# 获取该文件夹下所有 .xlsx 文件
file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
             if f.endswith('.xlsx')]

# 读取并合并所有文件
all_data = pd.concat([pd.read_excel(file) for file in file_list], ignore_index=True)

# 保存合并后的结果
output_path = os.path.join(folder_path, 'merged_eat_origin.xlsx')
all_data.to_excel(output_path, index=False)

print(f"已合并 {len(file_list)} 个文件，保存为 {output_path}")
