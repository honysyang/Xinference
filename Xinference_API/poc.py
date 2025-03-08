import requestsimport json

    try:

        response = requests.get(url, verify=False if url.startswith("https") else True)
        if response.status_code == 200:
            try:
                # 尝试将响应内容解析为JSON格式
                json_data = response.json()
                print(f"[+] successful visit {url}，Returns JSON content, there may be an unauthorized vulnerability in the Xinference framework API interface。")
                print("The returned content is as follows：")
                # 格式化打印JSON数据，缩进为4个空格
                print(json.dumps(json_data, indent=4))
                return True
            except json.JSONDecodeError:
                print(f"[-] Access to {url} was successful, but the returned content is not in a valid JSON format。")
        else:
            print(f"[-] Access to {url} failed, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"[-] An error occurred while accessing {url}: {e}")
    return False

if __name__ == "__main__":
    # 提示用户输入目标URL
    url = input("Please enter the destination URL.: ")
    check_status_url(url)
