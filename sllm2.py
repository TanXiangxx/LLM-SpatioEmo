from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pandas as pd

# 模型加载
MODEL_NAME = "uer/roberta-base-finetuned-jd-binary-chinese"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
print("开始加载模型...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to("cpu")
print("模型加载完成！")


def hf_semantic_analysis(prompt):
    # 在这里指定一个 max_length 避免 tokenizer 的提示“默认不截断”
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512).to("cpu")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).squeeze()

    # 只需使用 probabilities[1] （正面概率）
    sentiment_score = round(probabilities[1].item() * 10, 2)  
    return sentiment_score


# 情绪标签映射函数
def map_sentiment_label(score):
    if score < 4.0:
        return "负面"
    elif score < 9.2:
        return "中性"
    else:
        return "正面"

# 负面情绪增强函数（按评分差值）
def augment_negative(comment, diff_score):
    if diff_score <= 0.1:
        enhance = "比网上评论稍微差一点,没有那么好，整体一般"
    elif diff_score <= 0.3:
        enhance = "比网上评论差不少，有些东西不好吃，难吃，有点差"
    elif diff_score <= 1.0:
        enhance = "比网上评论差非常非常多，很差劲，各方面都不算好"
    else:
        enhance = "感觉被欺骗了，很差很差很差，很差，很差，很差，很坏。"
    return comment + " " + enhance

# 正面情绪增强函数
def augment_positive(comment, diff_score):
    if diff_score <= 0.5:
        enhance = "比预期略好"
    else:
        enhance = "服务超出预期"
    return comment + " " + enhance

# 读取Excel数据
data = pd.read_excel('./data/eat1.xlsx')  # 替换为你的文件路径
data['star'] = pd.to_numeric(data['star'], errors='coerce')
data['mrks'] = pd.to_numeric(data['mrks'], errors='coerce')

results = []

valid_rows = data.dropna(subset=['star', 'mrks'])
print(f"有效评分数据行数：{len(valid_rows)}")

for idx, row in valid_rows.iterrows():
    star = row['star'] / 10.0  # 标准化为 0-5
    mrks = row['mrks']
    comment = str(row['comment']) if pd.notna(row['comment']) else ""

    # 忽略空评论
    if comment.strip() == "":
        continue

    diff = round(star - mrks, 2)

    # 增强处理
    if star < mrks:
        comment_augmented = augment_negative(comment, mrks - star)
    elif star > mrks:
        comment_augmented = augment_positive(comment, star - mrks)
    else:
        comment_augmented = comment

    sentiment_score = hf_semantic_analysis(comment_augmented)
    sentiment_label = map_sentiment_label(sentiment_score)

    results.append({
        "原始评论": comment,
        "增强后评论": comment_augmented,
        "用户评分": round(star, 2),
        "商店评分": round(mrks, 2),
        "评分差": diff,
        "情绪评分(0-10)": sentiment_score,
        "情绪标签": sentiment_label,
        "经度": row["经度"],
        "纬度": row["纬度"]
    })

# 输出结果
if len(results) == 0:
    print("⚠️ 没有有效的结果，请检查数据文件！")
else:
    df_results = pd.DataFrame(results)
    df_results.to_excel("情感分析结果_细粒度3.xlsx", index=False)
    print("分析完成，结果已保存为 '情感分析结果_细粒度.xlsx'")
