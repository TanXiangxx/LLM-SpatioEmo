import pandas as pd
import os

def split_column_by_fixed_size(text, size=45):
    return [text[i:i+size] for i in range(0, len(text), size)]

def process_excel_by_parts(input_path, column_name, max_chars=45, output_dir="output_reviews"):
    df = pd.read_excel(input_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 为每一行的指定列切分，并记录最长的切片数
    split_data = []
    max_parts = 0
    for idx, row in df.iterrows():
        text = str(row[column_name])
        chunks = split_column_by_fixed_size(text, size=max_chars)
        split_data.append(chunks)
        max_parts = max(max_parts, len(chunks))

    # 按“第1段、第2段...”聚合所有行，生成多个文件
    for part_idx in range(max_parts):
        part_rows = []
        for i, row in df.iterrows():
            row_copy = row.copy()
            chunks = split_data[i]
            if part_idx < len(chunks):
                row_copy[column_name] = chunks[part_idx]
            else:
                row_copy[column_name] = ""  # 不足部分补空
            part_rows.append(row_copy)

        part_df = pd.DataFrame(part_rows)
        part_df.to_excel(f"{output_dir}/part_{part_idx+1}.xlsx", index=False)

    print(f"完成，共保存 {max_parts} 个文件。")

# 示例调用
process_excel_by_parts("eat2.xlsx", column_name="扩充评论", max_chars=45)
