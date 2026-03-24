# 浙财图书馆 1-050 真实抢座脚本（匹配 yylib.zufe.edu.cn）
import requests
from config import USERNAME, PASSWORD

print("=" * 50)
print("🔥 真实抢座：yylib.zufe.edu.cn 1-050 🔥")
print("账号：", USERNAME)
print("=" * 50)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://yylib.zufe.edu.cn/",
    "Content-Type": "application/json;charset=UTF-8"
})

# 1. 登录（真实系统登录接口）
try:
    login_url = "https://yylib.zufe.edu.cn/api/user/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    res = session.post(login_url, json=login_data, timeout=10)
    print("✅ 登录状态：", res.status_code)
    if res.status_code == 200:
        print("✅ 登录成功！")
    else:
        print("❌ 登录失败，请检查账号密码")
except Exception as e:
    print("❌ 登录异常：", e)

# 2. 抢座 1-050（真实预约接口）
try:
    book_url = "https://yylib.zufe.edu.cn/api/ic/seatPredetermine/book"
    seat_data = {
        "seatNo": "1-050",
        "date": "2026-03-24",  # 今天日期
        "startTime": "19:50",
        "endTime": "22:30",
        "areaId": 15  # 一楼西区（芸窗）
    }
    res = session.post(book_url, json=seat_data, timeout=5)
    
    print("\n🎯 抢座请求发送成功！")
    print("状态码：", res.status_code)
    print("返回内容：", res.text)
    
    if res.status_code == 200 and "success" in res.text:
        print("\n🎉🎉🎉 抢座成功！座位：1-050！")
    else:
        print("\n⚠️ 座位可能被占用或时间不可选")
except Exception as e:
    print("❌ 抢座出错：", e)

print("\n✅ 执行完毕")
