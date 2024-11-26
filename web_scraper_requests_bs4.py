"""
文件名: web_scraper_requests_bs4.py

描述:
该脚本用于从 API 获取分页数据，并对响应中提供的网页链接进行解析。
- 使用 `requests` 库发送 HTTP 请求获取 API 数据和网页内容。
- 使用 `BeautifulSoup` 解析网页 HTML，并提取指定的内容（如特定 `div` 标签的文本）。
- 最终将 API 数据与解析内容结合，输出为结构化的 JSON 格式。

主要功能:
1. 从 API 接口获取分页数据。
2. 爬取网页中指定的 HTML 内容（例如指定类名的 `div` 标签）。
3. 将处理结果以 JSON 格式打印输出。

依赖:
- `requests`: 用于发送 HTTP 请求。
- `BeautifulSoup`: 用于解析 HTML 并提取内容。

日期: [2024/11/26]
"""


import requests
from bs4 import BeautifulSoup
import json
import time

API_BASE_URL = "https://xxxxx.php"  # API 的基地址

def fetch_data(page_num):
    """获取指定页的数据"""
    params = {
        "text": "关键字",
        "pageSize": 20,
        "page": page_num
    }
    try:
        response = requests.get(API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("list", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from page {page_num}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from page {page_num}: {e}")
        print(f"Raw response:\n{response.text}")
    return []

def extract_video_brief(url, class_name="className"):
    """根据class_name提取div内容"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        target_div = soup.find("div", class_=class_name)
        if target_div:
            return target_div.text.strip()
        print(f"No '{class_name}' div found on {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
    except Exception as e:
        print(f"Unexpected error on {url}: {e}")
    return None

def process_pages(start_page, end_page):
    """处理多个页面的数据"""
    all_data = []
    for page_num in range(start_page, end_page + 1):
        print(f"Fetching data for page {page_num}...")
        page_data = fetch_data(page_num)
        time.sleep(1)  # 控制请求频率
        for item in page_data:
            urllink = item.get("urllink")
            if urllink:
                print(f"Processing URL: {urllink}")
                target_text = extract_video_brief(urllink)
                all_data.append({
                    "all_title": item.get("all_title"),
                    "urllink": urllink,
                    "target_text": target_text
                })
    return all_data

if __name__ == "__main__":
    # 设置页码范围
    start_page = 1
    end_page = 2  # 示例：抓取1到2页
    result_data = process_pages(start_page, end_page)
    print(json.dumps(result_data, indent=2, ensure_ascii=False))
