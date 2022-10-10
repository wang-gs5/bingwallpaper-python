import ctypes
from datetime import date
import os
import requests

def set_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 1)

def save_img(bytes, path):
    dir = os.path.dirname(path)
    #路径对应的目录不存在，则创建
    if not os.path.exists(dir):
        os.makedirs(dir)
    #保存壁纸
    with open(path, "wb") as f:
        f.write(bytes)

def fecth(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    return res

def get_wallpaper_url():
    #重试次数
    retry = 5
    is_success = False
    domain = "https://cn.bing.com"
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    link = ""
    while retry >= 0 and not is_success:
        res = fecth(url)
        try:
            data = res.json()
            link = domain + data.get("images")[0].get("url")
            print(link)
            is_success = True
        except Exception as e:
            retry -= 1
    if link:
        return link
    else:
        raise Exception("获取失败")

def main():
    #壁纸保存的文件夹
    wallpaper_dir = "C:\\wallpaper\\"
    try:
        #以今天的日期重命名壁纸
        totay = str(date.today())
        path = wallpaper_dir + totay + ".jpg"
        #已经存在，直接设置壁纸
        if os.path.exists(path):
            set_wallpaper(path)
            return
        link = get_wallpaper_url()
        response = fecth(link)
        save_img(response.content, path)
        set_wallpaper(path)
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()