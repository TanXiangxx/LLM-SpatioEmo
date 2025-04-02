from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# 选择更小的模型
MODEL_NAME = "google/flan-t5-small"

# 加载 Tokenizer 和模型（确保在 CPU 上运行）
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
print("开始加载模型...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, device_map=None).to("cpu")
print("模型加载完成！")

def hf_semantic_analysis(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    
    with torch.no_grad():
        output = model.generate(**inputs, max_length=256)

    return tokenizer.decode(output[0], skip_special_tokens=True)

# 测试语义分析
text = "i am "

print("执行推理...")
result = hf_semantic_analysis(f"analysis my sentence mood : {text}")
print("推理结束！")

print(result)
