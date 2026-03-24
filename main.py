from lib.zufe_library import BookRenew
from config import USERNAME, PASSWORD

if __name__ == "__main__":
    print("===== 浙财大图书馆续期脚本 =====")
    renew_tool = BookRenew(USERNAME, PASSWORD)
    login_ok = renew_tool.login()
    if not login_ok:
        print("登录失败")
        exit()
    renew_tool.batch_renew()
