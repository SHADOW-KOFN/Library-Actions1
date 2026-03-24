import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://lib.zufe.edu.cn/cas/login"
MY_BOOKS_URL = "https://lib.zufe.edu.cn/my/library"

class BookRenew:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.is_login = False

    def login(self):
        try:
            res = self.session.get(LOGIN_URL, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            lt = soup.find("input", {"name": "lt"})["value"]
            execution = soup.find("input", {"name": "execution"})["value"]
            
            login_data = {
                "username": self.username,
                "password": self.password,
                "lt": lt,
                "execution": execution,
                "_eventId": "submit"
            }
            login_res = self.session.post(LOGIN_URL, data=login_data, timeout=10)
            
            if "我的图书馆" in login_res.text:
                self.is_login = True
                print("✅ 登录成功！")
            else:
                self.is_login = False
                print("❌ 登录失败")
            return self.is_login
        except Exception as e:
            print(f"❌ 登录出错：{str(e)}")
            return False

    def get_borrowed_books(self):
        if not self.is_login:
            print("⚠️ 请先登录！")
            return []
        try:
            res = self.session.get(MY_BOOKS_URL, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            books = []
            for item in soup.select(".borrow-list-item"):
                book_info = {}
                title_tag = item.select_one(".book-title a")
                book_info["title"] = title_tag.text.strip() if title_tag else "未知书名"
                renew_tag = item.select_one(".renew-btn a")
                book_info["renew_url"] = renew_tag["href"] if renew_tag else ""
                books.append(book_info)
            return books
        except Exception as e:
            print(f"❌ 获取借阅列表出错：{str(e)}")
            return []

    def batch_renew(self):
        books = self.get_borrowed_books()
        success = []
        failed = []
        for book in books:
            if not book["renew_url"]:
                failed.append(f"{book['title']}（无续期权限）")
                continue
            try:
                renew_full_url = f"https://lib.zufe.edu.cn{book['renew_url']}"
                res = self.session.get(renew_full_url, timeout=10)
                if "续期成功" in res.text:
                    success.append(book["title"])
                else:
                    failed.append(book["title"])
            except Exception as e:
                failed.append(f"{book['title']}（出错：{str(e)}）")
        
        print(f"✅ 续期成功：{len(success)}本")
        print(f"❌ 续期失败：{len(failed)}本")
        return {"success": success, "failed": failed}
