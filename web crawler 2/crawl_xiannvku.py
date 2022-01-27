import urllib.request
from bs4 import BeautifulSoup
import os
import time
header = {
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
    }
#receive url and download to specific path
def Download(url,picAlt,name,endNUM):
    path='秀人网爬虫/'+picAlt+'/'               #folder address
    urllib.request.urlretrieve( url, '{0}{1}.jpg'.format(path, name))   #download to specified path
    print('Picture {0}/{1} named {2} downloaded on: {3}{0}.jpg'.format(name,endNUM,picAlt,path)) #可视化了解进度
    '''
    pic_path=path+str(name)+'.jpg'            #picture address
    if not os.path.exists(pic_path):          #picture dosen't exist
        urllib.request.urlretrieve( url, '{0}{1}.jpg'.format(path, name))   #download to specified path
        print('Picture {0}/{1} named {2} downloaded on: {3}{0}.jpg'.format(name,endNUM,picAlt,path)) #可视化了解进度  
    else:
        print('图片{0}已存在\t'.format(name),end='')
    return
    '''
#套图下载函数
def cycle_download(targetUrl, beginNUM ,endNUM,Album_title):
    req = urllib.request.Request(url=targetUrl,headers=header)
    time.sleep(1)                               #访问停顿
    response = urllib.request.urlopen(req)              #以标签方式打开网址
    html = response.read().decode('utf-8','ignore')     #以utf-8方式解码read,遇到错误ignore
    soup = BeautifulSoup(html, 'html.parser')           #parser表示BS4的html解析器
    Divs = soup.find_all('img',attrs={'class':'content_img' }) #找到对应标签对应属性的图片,在此为居中放置的大图
    nowpage = soup.find('a',attrs={'class':'on'}).get_text()    #class: on 对应当前页码的按钮
    nextpage=str(int(nowpage)+1)                                #理论上的下一页页码
    nowpageLink = targetUrl                                     #当前页码链接
    nextPageLink = soup.find('a',attrs={'class':'a1'},text='下一页')['href']   #'下一页'按钮对应的链接
    if beginNUM ==endNUM :                              #图片爬完了,退出
        return
    for div in Divs:
        beginNUM = beginNUM+1
        picLink = div.get('src')            # 获取图片的url
        Download(picLink,Album_title, beginNUM,endNUM)  # 根据获取的链接下载图片，传入由图片Alt决定的路径中
    if (nextPageLink != nowpageLink):       # 没到最后一页，则递归调用本函数继续cycle循环下载
        print('next page is: {0}    Link is: {1}\n'.format(nextpage,nextPageLink))  #可视化
        cycle_download(nextPageLink,beginNUM ,endNUM,Album_title)
    return
 
#传输父节点链接，本函数用于根据传入的url提取所有子url
def run(root_url,startpage,endpage):
    cnt_album=0
    cnt_page=startpage
    #解析 IMISS 页面
    #url如下
    req_root = urllib.request.Request(url=root_url,headers=header)
    time.sleep(1)                                       #访问停顿
    response_root = urllib.request.urlopen(req_root)
    html_root = response_root.read().decode('utf-8','ignore')
    soup_root = BeautifulSoup(html_root, 'html.parser')

    #找到所有title标签
    title_list = soup_root.find('ul',attrs={'class':'img'}).find_all('p',attrs={'class':'p_title'})
    next_link =  soup_root.find('a',attrs={'class':'a1'},text='下一页')['href']   #'下一页'按钮对应的链接
    #找到title标签内的封面超链接
    x=0
    for title in title_list:
        x=x+1
    print('第{0}页找到了{1}套图片,开始下载'.format(cnt_page,x))
    for title in title_list:
        cnt_album+=1
        cover_link = title.find('a',target='_blank')['href']
        Album_title = title.find('a',target='_blank').get_text()
        path='秀人网爬虫/'+Album_title+'/'
        if not os.path.exists(path):    #图集地址不存在
            os.makedirs(path)           #创建图集地址 
            print('创建图集{0}'.format(Album_title))
        else:
            print('Album{0} {1}is done, link is{2}'.format(str(cnt_album),Album_title,cover_link))
            continue
        req = urllib.request.Request(url=cover_link,headers=header)
        time.sleep(1)                                       #访问停顿
        #解析页码
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8','ignore')
        soup = BeautifulSoup(html, 'html.parser')           #parser表示BS4的html解析器
        endNUM = int(soup.find('a',attrs={'class':'a1'}).get_text()[:-1])
        beginNUM = 0
        #下载套图
        cycle_download(cover_link,beginNUM,endNUM,Album_title)
        print("Album {0} is done".format(str(cnt_album)))
        time.sleep(1)
    cnt_page=cnt_page+1
    print("Album Page {0} is Done! Next Album Page is {1}".format(str(cnt_page),next_link))
    if cnt_page<endpage:                                              #爬多少页
        run(next_link,cnt_page,10)
    return 
    
if __name__ == '__main__':
    url='http://www.xiannvku.com/jigou/xiuren-1.html'           #根据需要更改
    try:
        run(url,1,10)
    except:
        time.sleep(30)
        run(url,1,10)