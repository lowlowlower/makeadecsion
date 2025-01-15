import time
from supabase import create_client, Client
import requests
import json

# Supabase 连接信息
SUPABASE_URL = "https://urfibhtfqgffpanpsjds.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVyZmliaHRmcWdmZnBhbnBzamRzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNTc4NTY0NSwiZXhwIjoyMDUxMzYxNjQ1fQ.fHIeQZR1l_lGPV7hYJkcahkEvYytIBpasXOg4m1atAs"
TABLE_NAME = "随机关键词测试"

# Gemini API 密钥
GEMINI_API_KEY = "AIzaSyApuy_ax9jhGXpUdlgI6w_0H5aZ7XiY9vU"
MODEL_NAME = "gemini-exp-1206"
# 初始化 Supabase 客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_keywords(prompt, max_retries=3, retry_delay=5):
    """调用 Gemini API 生成关键词，带重试机制"""
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    for attempt in range(max_retries):
        try:
            json_payload = json.dumps(payload)
            api_response = requests.post(api_url, headers=headers, data=json_payload)
            api_response.raise_for_status()  # 抛出 HTTPError，如果状态码是 4xx 或 5xx
            api_response_json = api_response.json()
            try:
                keyword = api_response_json['candidates'][0]['content']['parts'][0]['text'].strip()
                return keyword
            except (KeyError, IndexError, TypeError):
                print(f"尝试 {attempt + 1}: API 响应格式异常: {api_response_json}")
        except requests.exceptions.RequestException as e:
            print(f"尝试 {attempt + 1}: API 请求失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("达到最大重试次数，放弃。")
                return None
    return None

# 1. 从 Supabase 获取 "RANGE" 列的值
response = supabase.table(TABLE_NAME).select("Range").eq('id', 1).execute()
data = response.data
if data:
    range_value = data[0]['Range']
    print(f"获取到的 Range 值: {range_value}")

    # 2. 构造 Gemini API 请求的 prompt
    prompt = f"针对 {range_value}，生成一个英文关键词，只要一个关键词，每次不一样，输出格式只保留一个关键词不要其他任何的符号和语言"

    # 3. 调用 Gemini API 生成关键词
    generated_keyword = generate_keywords(prompt)

    if generated_keyword:
        # 清理关键词，移除可能存在的星号或其他不需要的字符
        cleaned_keyword = generated_keyword.strip().strip('*')
        print(f"生成的关键词: {cleaned_keyword}")

        # 4. 将生成的关键词更新到 Supabase 表的 "Keywords" 列
        
        update_data = {"Keyword": cleaned_keyword.lower()}  # 统一转换为小写
        print(f"尝试更新的数据: {update_data}")
        update_response = supabase.table(TABLE_NAME).update(update_data).eq('id', 1).execute()

        if update_response.data is None:
            print(f"更新 Supabase 失败: {{update_response}}")
        else:
            print("成功将关键词更新到 Supabase")
    else:
        print("未能成功生成关键词")

else:
    print("未找到 id 为 1 的记录")