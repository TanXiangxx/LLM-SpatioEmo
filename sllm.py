from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# 选择更适合的多类别情感分析模型
MODEL_NAME = "uer/roberta-base-finetuned-jd-binary-chinese" # 适用于 3 类情感分析
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
print("开始加载模型...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to("cpu")
print("模型加载完成！")

def hf_semantic_analysis(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to("cpu")
    
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    sentiment = torch.argmax(logits, dim=1).item()
    
    # 计算情感强度
    sentiment_score = probabilities[0][sentiment].item()

    # 3 分类情感：0=负面，1=中性，2=正面
    sentiment_labels = ["0", "1", "2"]
    
    return sentiment_labels[sentiment], round(sentiment_score, 2)

# 示例文本
text = "sentence"

print("执行推理...")
result, confidence = hf_semantic_analysis(text)
print("推理结束！")

print(f"情感分析结果：{result} (置信度: {confidence})")
