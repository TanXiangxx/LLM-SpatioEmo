import pandas as pd
import os

def merge_cleaned_excels(input_dir="output_reviews", column_name="扩充评论", output_file="merged_eat2.xlsx"):
    all_dfs = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(input_dir, filename)
            df = pd.read_excel(file_path)
            
            # 删除指定列为空的行
            df = df[df[column_name].notna()]
            df = df[df[column_name].astype(str).str.strip() != ""]

            all_dfs.append(df)

    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df.to_excel(output_file, index=False)
        print(f"合并完成，已保存为 {output_file}，共 {len(merged_df)} 行。")
    else:
        print("没有可用的文件或所有文件都为空。")

# 示例调用
merge_cleaned_excels()
