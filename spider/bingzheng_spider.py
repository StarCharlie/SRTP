import re
import urllib.error
import urllib.request
import xlwt

from bs4 import BeautifulSoup


# encoding=GBK
def main():
    # 简单查一下灸法这个页面的相关信息
    baseurl = "http://www.pharmnet.com.cn/tcm/zjdq/"
    datalist = getData(baseurl)
    savepath = "艾灸.xls"
    saveData(savepath, datalist)


# 全局变量，用于正则判断规则（字符串模式）
# r：忽视特殊符号
# ''：忽视双引号
findLink = re.compile(r'<a class="red5" href="(.*?)" title="(.*?)">.*?</a>', re.S)
findTempLink = re.compile(r'<a href="(.*?)" target="_blank"> (.*?)</a>', re.S)
findContext = re.compile(r'<div align="left">(.*?)</div>')
findName = re.compile(r'<strong>(.*?)</strong>')
findImgSrc = re.compile(r'<div align="left">.*', re.S)

findString = re.compile(r'<a href="(.*)>')


def getData(baseurl):
    datalist = []
    url = baseurl
    html = askURL(url)
    if html == "":
        return
    # 一个写的屎一样的获取脚本
    soup = BeautifulSoup(html, "html.parser", fromEncoding="gb18030")
    lis = soup.find_all('a', title=re.compile("(.*?)病症$"))
    for item in lis:
        item = str(item)
        try:
            item = re.findall(findLink, item)[0]
        except IndexError:
            continue
        for i in range(1, 7):
            html = askURL(str(item[0])+"index"+str(i))
            if html == "":
                continue;
            soup = BeautifulSoup(html, "html.parser", fromEncoding="gb18030")
            sublist = soup.find_all('a', href=re.compile(r'http://www.pharmnet.com.cn/tcm/zjdq/zjzl/10(.*?)'),
                                    target='_blank');
            for subItem in sublist:
                data = []
                subItem = str(subItem)
                subItem = re.findall(findTempLink, subItem)[0]
                html = askURL(str(subItem[0]))
                print(str(subItem[0]), str(subItem[1]));
                if html == "":
                    continue;
                soup = BeautifulSoup(html, "html.parser", fromEncoding="gb18030")
                contexts = soup.find_all('td', class_='red');
                finalCon = ""
                flag = False
                for context in contexts:
                    context = str(context.getText())
                    context = re.sub(r'\s', "", context)
                    context = re.sub(r'<b></b>', "", context)
                    context = re.sub(r'<br(\s+)?/>(\s+)?', "", context)
                    finalCon += context
                finalCon = finalCon.split("【治疗】");
                data.append(item[1])
                data.append(subItem[1])
                data.append(finalCon[0])
                data.append(finalCon[1])
                datalist.append(data)
    return datalist


def saveData(savepath, datalist):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet('基本病症', cell_overwrite_ok=True)
    col = ("类别", "病名", "病症", "治疗")
    for i in range(0, 4):
        worksheet.write(0, i, col[i]);
    i = 0
    for data in datalist:
        i = i+1
        for j in range(0, 4):
            try:
                worksheet.write(i, j, data[j])
            except IndexError:
                continue
    workbook.save(savepath)
    return 0;


def askURL(url):
    # 网站请求
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            return ""
        if hasattr(e, "reason"):
            return ""
    return html


if __name__ == "__main__":
    main()
