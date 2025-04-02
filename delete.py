import shutil
import os
huggingface_cache = os.path.expanduser("~/.cache/huggingface/hub")
shutil.rmtree(huggingface_cache, ignore_errors=True)
print("已删除 Hugging Face 缓存")
