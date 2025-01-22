import csv
import urllib.request as request
import json
import re

url1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
url2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with request.urlopen(url1) as response1:
    data1=json.load(response1)
with request.urlopen(url2) as response2:
    data2=json.load(response2)

slist=data1["data"]["results"]
dlist=data2["data"]
#--------------寫入spot,csv---------------
serial_to_address={}
serial_to_mrt={}
for item in dlist:
    serial_no = item["SERIAL_NO"]
    address = item["address"]
    mrt=item["MRT"]
    serial_to_address[serial_no]=address
    serial_to_mrt[serial_no]=mrt

#提取區名
def extract_district(address):
    match = re.search(r"(\w+區)",address)
    return match.group(1) if match else "未知區"
#提取第一張圖片
def extract_fist_img(filelist):
    urls=re.findall(r"https?://.*?\.(?:jpg|png|jpeg|JPG|PNG|JPEG)",filelist)
    return urls[0] if urls else "無圖片"
#寫入CSV
with open("spot.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["SpotTitle", "District", "Longitude", "ImageURL"])  # 寫入表頭
    for spot in slist:  # 替換為正確的 JSON 結構
        serial_no =spot["SERIAL_NO"]
        SpotTitle = spot["stitle"]        
        Longitude = spot["longitude"]
        ImageURL = extract_fist_img(spot["filelist"])
        #用SERIAL_NO匹配區名
        address = serial_to_address.get(serial_no,"未知地址")
        District = extract_district(address)

        writer.writerow([SpotTitle, District, Longitude, ImageURL])  # 區域假設為地址的前3字
#--------------寫入mrt,csv---------------
mrt_to_spots={}

#配對MRT和景點
for spot in slist:
    serial_no=spot["SERIAL_NO"]
    StationName = serial_to_mrt.get(serial_no)
    AttrctionTitle=spot["stitle"]

    if StationName not in mrt_to_spots:
        mrt_to_spots[StationName]=[]
    mrt_to_spots[StationName].append(AttrctionTitle)
#寫入csv
with open("mrt.csv",mode="w",newline="",encoding="utf-8") as file:
    writer =csv.writer(file)
    writer.writerow(["StationName","AttractionTitle1","AttractionTitle2","AttractionTitle3"])

    for StationName,AttrctionTitle in mrt_to_spots.items():
        row = [StationName]+AttrctionTitle
        writer.writerow(row)