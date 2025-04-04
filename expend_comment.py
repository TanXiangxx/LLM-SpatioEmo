import pandas as pd

# 负面情绪增强函数
def augment_negative(diff_score):
    if diff_score <= 0.1:
        return "比网上评论稍微差一点，没有那么好，整体一般。"
    elif diff_score <= 0.3:
        return "比网上评论差不少，有些东西不好吃，难吃，有点差。"
    elif diff_score <= 1.0:
        return "比网上评论差非常非常多，很差劲，各方面都不算好。"
    else:
        return "感觉被欺骗了，很差很差很差，很差，很差，很差，很坏。"

# 正面情绪增强函数
def augment_positive(diff_score):
    if diff_score <= 0.5:
        return "比预期略好。"
    else:
        return "服务超出预期，整体体验十分令人惊喜。"

# 拼接扩充评论
def rule_based_expand_comment(store, address, star, mrks, comment, nums):
    star_score = round(star / 10.0, 2)
    mrks_score = round(mrks, 2)
    diff = round(mrks_score - star_score, 2)  # 用户评分 - 平台评分（正值说明用户体验更好）

    # 判断差异并选择增强文本
    if diff > 0:
        emotion_text = augment_positive(diff)
    elif diff < 0:
        emotion_text = augment_negative(abs(diff))
    else:
        emotion_text = "这次体验和平台评价完全一致，整体感觉还不错。"

    # 长评论拼接
    long_comment = (
        f"我在【{store}】用餐，这家餐厅位于{address}。"
        f"在来之前，我查看了这家店的评分为 {star_score} 分，共有 {nums} 条评论。"
        f"我的实际体验给出了 {mrks_score} 分，两者相差 {abs(diff)} 分，{emotion_text} "
        f"\n\n以下是我此次的简评：{comment} "
        f"\n整体来说是一次{'还不错、不后悔的' if mrks_score >= 4.9 else '一般甚至有些失望的'}用餐体验，希望我的评论能对其他人有所帮助。"
    )

    return long_comment

# ========== 主程序部分 ==========

# 文件路径
input_path = 'data/eat1.xlsx'
output_path = 'eat2.xlsx'

# 读取数据
data = pd.read_excel(input_path)

# 数据清洗
data['star'] = pd.to_numeric(data['star'], errors='coerce')
data['mrks'] = pd.to_numeric(data['mrks'], errors='coerce')

# 扩充评论生成
expanded_comments = []

for idx, row in data.iterrows():
    try:
        store = str(row['store_link'])
        address = str(row['address'])
        star = float(row['star'])
        mrks = float(row['mrks'])
        nums = str(row['nums'])
        comment = str(row['comment'])

        # 生成扩充评论
        long_comment = rule_based_expand_comment(store, address, star, mrks, comment, nums)
    except Exception as e:
        long_comment = f"生成失败：{e}"

    expanded_comments.append(long_comment)

# 写入新列并导出文件
data['扩充评论'] = expanded_comments
data.to_excel(output_path, index=False)

print(f"✅ 评论扩充完成，结果已保存到：{output_path}")
