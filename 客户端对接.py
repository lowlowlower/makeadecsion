from supabase import create_client, Client

# 替换为你的 Supabase 项目 URL
SUPABASE_URL = "https://urfibhtfqgffpanpsjds.supabase.co"
# 替换为你的 Supabase 项目 API 密钥 (anon 密钥即可用于读取，如果需要写入则需要 service_role 密钥)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVyZmliaHRmcWdmZnBhbnBzamRzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNTc4NTY0NSwiZXhwIjoyMDUxMzYxNjQ1fQ.fHIeQZR1l_lGPV7hYJkcahkEvYytIBpasXOg4m1atAs"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

table_name = "随机关键词测试"  # 替换为你要读取的表名

try:
    response = supabase.table(table_name).select("Range").eq('id', 1).execute()
    data = response.data
    keyword=data[0]['Range']
    print(f"成功从表 '{table_name}' 读取数据:")
    print(keyword)
except Exception as e:
    print(f"读取数据时发生错误: {e}")
