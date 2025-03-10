import requests


def check_url(ip, path):
    url = f"http://{ip}{path}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.text.strip() and "Xinference" in response.text:
                print(f"[+] 成功访问 {url}，且返回内容包含 Xinference，可能存在未授权可执行任意操作漏洞。")
                return True
            else:
                print(f"[-] 成功访问 {url}，但返回内容不符合预期。")
        else:
            print(f"[-] 访问 {url} 失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"[-] 访问 {url} 时发生错误: {e}")
    return False


if __name__ == "__main__":
    ip = input("请输入目标 IP 地址及端口: ")
    paths = [
        "/ui/#/launch_model/llm",
    ]
    for path in paths:
        check_url(ip, path)
