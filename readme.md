### 前言

觉得bing官网的壁纸挺好看的，就使用python自制一个更换壁纸的小脚本，每次电脑登录后更换壁纸。

### 用到的包

```Python
import ctypes
from datetime import date
import os
import requests
```

- ctypes：用于设置桌面壁纸

- requests：爬取壁纸

### bing壁纸接口

```Plain
https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1
```

- format：返回内容的格式
  - 不带：返回的结果为xml格式
  - js：返回为json格式
  - xml：返回为xml格式

- idx：0为当天的图片，1为昨天的图片，以此类推，最大为7

- n:输出图片信息的数量，从idx所代表的日期开始，之前的n张图片，结合idx，最大值为8，结合idx，最大可获取15天的图片信息。

### 获取壁纸url

以json格式为例，分析接口返回的内容

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212519.png)

url就是我们需要的，加上bing官网的域名（"https://cn.bing.com"）就得到了图片的访问地址;

代码如下：

```Python
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
```

### 保存壁纸

将壁纸保存在本地，我保存的是在c盘的目录下：`C:\\wallpaper\\`

```Plain
def save_img(bytes, path):
    dir = os.path.dirname(path)
    #路径对应的目录不存在，则创建
    if not os.path.exists(dir):
        os.makedirs(dir)
    #保存壁纸
    with open(path, "wb") as f:
        f.write(bytes)
```

### 设置壁纸

使用ctypes模块调用windows系统函数设置壁纸。

filepath需为绝对路径。

这里函数的参数不是很了解，网上搜这么用，就这么用了（-_-）

```Python
def set_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 1)
```

### 主函数

```Python
#wallpaper.py
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
        #保存壁纸
        save_img(response.content, path)
        #设置壁纸
        set_wallpaper(path)
    except Exception as e:
        raise e
```

### 打包成exe文件

使用pyinstaller将python文件打包成exe文件。

未安装的使用pip安装即可：`pip install pyinstaller`

pyinstaller参数：

- -F：pyinstaller 会将 python 程序打包成单个可执行文件。

- -D： pyinstaller 会将 python 程序打包成一个文件夹，运行程序时，需要进入该文件夹，点击运行相应的可执行程序。

- -w：不弹出命令行窗口

- -i：打包的exe文件的图标

- -n：指定打包后生成文件的名称,不指定与python文件同名

bing的favicon.ico地址：https://cn.bing.com/favicon.ico

将下载好的ico图片放在和py文件（我的叫wallpaper.py）同一目录。执行命令：

```Python
pyinstaller -F -w -i xxx.ico wallpaper.py
```

xxx.ico为你的图标路径

打包好的exe文件在生成的dist文件夹下

### 配置计划任务

设置windows计划任务，开机后自动换壁纸。

1. 按下`windows键+x`,打开计算机管理

2. 点击任务任务计划程序

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212521.png)

3. 点击创建基本任务，设置好任务名

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212522.png)

4. 点击下一步，选择每天

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212523.png)

5. 设置好执行的时间

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212524.png)

6. 下一步，操作选择启动程序

7. 选择你的打包好的exe文件所在的路径（我的放到了桌面）

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212525.png)

8. 右键刚刚配置好的任务，点击属性->条件

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212526.png)

将电源这一栏取消

9.点击设置

​	将`如果过了计划开始时间，立即启动` 勾上

![img](https://wang-1310173418.cos.ap-guangzhou.myqcloud.com/blogs/202207291212527.png)

可根据需求自行设置。

感谢浏览，有错误敬请指正。