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

# 1. 获取 "RANGE" 列的值
response = supabase.table(TABLE_NAME).select("Range").eq('id', 1).execute()
data = response.data
if data:
    range_value = data[0]['Range']
    print(f"获取到的 Range 值: {range_value}")

    # 2. 构造 Gemini API 请求
    prompt = f"为 {range_value} 生成一个关键词，要求英文，每一次都不一样，输出格式只保留一个关键词不要其他任何的符号和语言"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    json_payload = json.dumps(payload)
    # 3. 发送 API 请求
    api_response = requests.post(api_url, headers=headers, data=json_payload)
    api_response_json = api_response.json()
    print(f"API 响应: {api_response_json}")
    keyword=api_response_json['candidates'][0]['content']['parts'][0]["text"].strip().strip('*')
    print(keyword)


    # 这里你需要处理 API 的响应，提取生成的关键词
else:
    print("未找到 id 为 1 的记录")