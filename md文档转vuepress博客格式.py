import os
import re
import shutil
from datetime import datetime
import configparser
import urllib.parse


config = configparser.ConfigParser()
config.read('config.ini',encoding="utf8")


imageSavePath = config.get("info","imageSavePath")
mdFileSavePath = config.get("info","mdFileSavePath")
imagePutPath = config.get("info","imagePutPath")

# imageSavePath = r"C:\Users\86155\Desktop\小制作\个人博客\VuepressBlog\src\.vuepress\public\assets\images"
# mdFileSavePath = r"C:\Users\86155\Desktop\小制作\个人博客\VuepressBlog\src\posts"
# imagePutPath = "/assets/images"

# 设置Markdown的博客模板文件
def template(fileNamePath,mdfileContext,filename):
    with open(fileNamePath,mode="w+",encoding="utf8") as file:
        file.writelines("---\r\n")
        file.writelines("title: " + filename + "\r\n")
        file.writelines("date: " + datetime.now().strftime('%Y-%m-%d')+ "\r\n")
        file.writelines("---\r\n")
        file.writelines(mdfileContext)



# 获取当前路径下所有文件名并筛选出Markdown文件
mdFileList = []
for fileName in os.listdir():
    if fileName.endswith("md"):
        mdFileList.append(fileName)
print("待处理文档列表：",end='')
print(mdFileList)
# 匹配Markdown中插入图片的正则表达式
mdImagePattern = "!\[.*\]\(.*\)"

for mdFileName in mdFileList:
    # 依次读取Markdown文件内容，并找出需要替换的部分
    with open(mdFileName,mode="r",encoding="utf8") as mdFile:
        mdFiletext = mdFile.read()
        # 获取当前Markdown文档中所有的图片链接
        mdImagePaths = re.findall(mdImagePattern,mdFiletext)
        # 图片计数
        imageCount = 1
        for mdImagePath in mdImagePaths:
            # 获取Markdown文档中图片在本机中的位置
            imagePathSource = re.search("\(.*\)",mdImagePath)[0][1:-1]

            # notion 中的图片经过URL编码，需要解码后才能使用
            imagePath = urllib.parse.unquote(imagePathSource)

            tarPath = os.path.join(imageSavePath,mdFileName.replace(".md",""))
            # print(tarPath)
            if not os.path.exists(tarPath):
                os.mkdir(tarPath)

            # 获取图片后缀
            imageSuf = imagePath.split("\\")[-1].split(".")[-1]
            # 将Markdown文档中的图片复制到指定位置
            shutil.copy(imagePath,tarPath + "\\"+ str(imageCount) +"." + imageSuf)

            # print(imagePath)
            targText = imagePutPath + "/" + mdFileName.replace(".md","") + "/" + str(imageCount) +"." + imageSuf
            # print(targText)
            # 修改Markdown中图片的路径为博客中的响应地址
            mdFiletext = mdFiletext.replace(imagePathSource,targText)
            # 图片数量自增
            imageCount = imageCount + 1

        mdSavePath = os.path.join(mdFileSavePath,mdFileName)
        template(mdSavePath,mdFiletext,mdFileName.replace(".md",""))
        print("图片已保存至："+ os.path.join(imageSavePath,mdFileName.replace(".md","")))
        print("文档已保存至：" + mdSavePath)
        input()
     



