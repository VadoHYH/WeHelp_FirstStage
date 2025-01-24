# 抓取PTT
import urllib.request as req
from bs4 import BeautifulSoup
import csv

base_url = "https://www.ptt.cc"
pages_to_crawl = 3
current_page_url = f"{base_url}/bbs/Lottery/index.html"

# 打開 CSV 文件準備寫入
with open("article.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Likes", "PublishTime"])  # 寫入表頭

    for _ in range(pages_to_crawl):
        # 獲取當前頁面的 HTML
        request = req.Request(current_page_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = BeautifulSoup(data, "html.parser")

        # 提取標題和按讚數
        titles = root.find_all("div", class_="title")
        likes_counts = root.find_all("div", class_="nrec")

        for i in range(len(titles)):
            title_tag = titles[i].a
            if not title_tag:  # 排除已刪除文章
                continue

            # 提取標題和文章連結
            article_title = title_tag.string.strip()
            article_url = base_url + title_tag["href"]

            # 提取按讚數
            like_count = "0"
            if i < len(likes_counts):
                like_count = likes_counts[i].string.strip() if likes_counts[i].string else "0"

            # 提取文章發佈時間
            publish_time = ""
            try:
                article_request = req.Request(article_url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                })
                with req.urlopen(article_request) as article_response:
                    article_data = article_response.read().decode("utf-8")
                article_root = BeautifulSoup(article_data, "html.parser")

                # 篩選出時間
                meta_tags = article_root.find_all("div", class_="article-metaline")
                for tag in meta_tags:
                    meta_tag = tag.find("span", class_="article-meta-tag")
                    meta_value = tag.find("span", class_="article-meta-value")
                    if meta_tag and meta_value and meta_tag.string == "時間":
                        publish_time = meta_value.string.strip()
                        break

            except Exception as e:
                print(f"無法抓取文章發佈時間: {article_title}, 錯誤: {e}")

            # 寫入 CSV
            writer.writerow([article_title, like_count, publish_time])

        # 下一頁
        next_page = root.find("a", class_="btn wide", string="‹ 上頁")
        if next_page is not None:
            current_page_url = base_url + next_page["href"]
        else:
            print("無法找到下一頁連結，結束抓取")
            break 
