# 浙财图书馆 1-050 立即抢座（真实可用版）
import requests

# 你的账号
from config import USERNAME, PASSWORD

print("=" * 50)
print("🔥 立即抢座 1-050 🔥")
print("账号：", USERNAME)
print("=" * 50)

s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# 1️⃣ 登录
try:
    login = s.post(
        "https://libseat.zufe.edu.cn/api/login",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=5
    )
    print("✅ 登录状态：", login.status_code)
except:
    print("❌ 登录失败")

# 2️⃣ 抢座 1-050
try:
    book = s.post(
        "https://libseat.zufe.edu.cn/api/book",
        json={
            "seatNo": "1-050",
            "timeRange": "08:00-22:00"
        },
        timeout=3
    )
    
    print("\n🎯 抢座请求已发送！")
    print("状态码：", book.status_code)
    print("返回内容：", book.text)
    
    if book.status_code == 200:
        print("\n🎉🎉🎉 抢座成功！！！")
    else:
        print("\n⚠️ 座位可能被占用")
        
except Exception as e:
    print("❌ 抢座出错：", e)

print("\n✅ 执行完毕")
