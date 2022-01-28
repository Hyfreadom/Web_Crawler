import urllib.request
from bs4 import BeautifulSoup
import os
import time
url='http://www.xiannvku.com/tags/chaoduanqun-1.html'           #根据需要更改
Folder ='超短裙/'                                               #根据需要更改
endpage=5

header = {
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
    }
#receive url and download to specific path
def Download(url,picAlt,name):
    path=Folder+picAlt+'/'               #folder address
    urllib.request.urlretrieve( url, '{0}{1}.jpg'.format(path, name))   #download to specified path
    return
#套图下载函数
def cycle_download(targetUrl,Album_title,number):
    req = urllib.request.Request(url=targetUrl,headers=header)
    time.sleep(1)                               #访问停顿
    response = urllib.request.urlopen(req)              #以标签方式打开网址
    html = response.read().decode('utf-8','ignore')     #以utf-8方式解码read,遇到错误ignore
    soup = BeautifulSoup(html, 'html.parser')           #parser表示BS4的html解析器
    Divs = soup.find_all('img',attrs={'class':'content_img' }) #找到对应标签对应属性的图片,在此为居中放置的大图
    nowpageLink = targetUrl                                     #当前页码链接
    nextPageLink = soup.find('a',attrs={'class':'a1'},text='下一页')['href']   #'下一页'按钮对应的链接
    for div in Divs:
        number+=1
        picLink = div.get('src')            # 获取图片的url
        Download(picLink,Album_title,number)  # 根据获取的链接下载图片，传入由图片Alt决定的路径中
    if (nextPageLink != nowpageLink):       # 没到最后一页，则递归调用本函数继续cycle循环下载
        cycle_download(nextPageLink,Album_title,number)
    return
 
#传输父节点链接，本函数用于根据传入的url提取所有子url
def run(root_url,startpage,endpage):
    cnt_page=startpage
    #解析 主页面
    #url如下
    req_root = urllib.request.Request(url=root_url,headers=header)
    time.sleep(1)                                       #访问停顿
    response_root = urllib.request.urlopen(req_root)
    html_root = response_root.read().decode('utf-8','ignore')
    soup_root = BeautifulSoup(html_root, 'html.parser')

    #找到所有title标签
    title_list = soup_root.find('ul',attrs={'class':'img'}).find_all('p',attrs={'class':'p_title'})
    #'下一页'按钮对应的链接
    next_link =  soup_root.find('a',attrs={'class':'a1'},text='下一页')['href']   
    x=0
    for title in title_list:
        x=x+1
    print('Page {0} found {1} album'.format(cnt_page,x))
    #解析title标签内的超链接
    for title in title_list:
        cover_link = title.find('a',target='_blank')['href']
        Album_title = title.find('a',target='_blank').get_text()
        path=Folder+Album_title+'/'
        if not os.path.exists(path):    #图集地址不存在
            os.makedirs(path)           #创建图集地址 
        else:
            print('{0} is done'.format(Album_title))
            continue
        #下载套图
        cycle_download(cover_link,Album_title,1)
        print('{0} is done'.format(Album_title))
        time.sleep(1)
    print("Page {0} is Done! Next page is {1}".format(str(cnt_page),next_link))
    cnt_page=cnt_page+1
    if cnt_page<endpage:                                              #爬多少页
        run(next_link,cnt_page,endpage)
    return 
    
if __name__ == '__main__':
    try:
        run(url,1,endpage)
    except:
        time.sleep(30)
        run(url,1,endpage)