import urllib.request
from bs4 import BeautifulSoup
import os
def Download(url,picAlt,name):
    #path = 'D:\\pythonD爬虫妹子图\\'+picAlt+'\\'
    path = 'pythonD爬虫妹子图\\'+picAlt+'\\'
    print('路径为{0}'.format(path))
    if not os.path.exists(path):
        os.makedirs(path)
    urllib.request.urlretrieve( url, '{0}{1}.jpg'.format(path, name)) #download to specified path
 
header = {
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
    }

def run(targetUrl, beginNUM ,endNUM):
    global x
    x=0
    req = urllib.request.Request(url=targetUrl,headers=header)
    response = urllib.request.urlopen(req)
    html = response.read().decode('gb2312','ignore')
    soup = BeautifulSoup(html, 'html.parser')           #parser表示BS4的html解析器

    #class big_pic表示的是区域,对应xiannvku为class content.正因为是区域所以mmon里有两个big_pic,一个带#一个不带#
    #推测此处可以换为区域搜索,也就是改为class content
    #当前代码区域内只能搜到的Div长度为1,更换后推测大于1
    Divs = soup.find_all('div',attrs={'class':'big-pic' }) #div是名称,attrs是属性
    print(Divs)
    nowpage = soup.find('span',attrs={'class':'nowpage'}).get_text()
    totalpage= soup.find('span',attrs={'class':'totalpage'}).get_text()
    for div in Divs:
        x=x+1
    print(x)
    if beginNUM ==endNUM :
        return
    for div in Divs:
        beginNUM = beginNUM+1
 
        if div.find("a") is None :
            print("没有下一张了")
            return
        elif div.find("a")['href'] is None or div.find("a")['href']=="":
            print("没有下一张了None")
            return
        print("下载信息：总进度：",beginNUM,"/",endNUM," ，正在下载套图：(",nowpage,"/",totalpage,")")
 
        if int(nowpage)<int(totalpage):
            nextPageLink ="http://www.mmonly.cc/mmtp/qcmn/" +(div.find('a')['href'])
        elif int(nowpage)==int(totalpage):
            nextPageLink = (div.find('a')['href'])
 
        picLink = (div.find('a').find('img'))['src']
        picAlt = (div.find('a').find('img'))['alt']
        print('下载的图片链接:',picLink)
        print('套图名：[ ', picAlt , ' ] ')
        print('开始下载...........')
        Download(picLink,picAlt, nowpage)
        print("下载成功！")
        print('下一页链接:',nextPageLink)
        run(nextPageLink,beginNUM ,endNUM)
        return
 

if __name__ == '__main__':
    targetUrl ="http://www.mmonly.cc/mmtp/qcmn/237269.html"
    #targetUrl='http://www.xiannvku.com/'
    run(targetUrl,beginNUM=0,endNUM=70)
    print(" OVER")
    
