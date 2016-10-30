#-*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
import cookielib

#  http://www.jianshu.com/p/7c5a4d7545ca
def spider(user_id):

  # 实例化一个LWPCookieJar对象
  load_cookiejar = cookielib.LWPCookieJar()
  # 从文件中加载cookies(LWP格式)
  load_cookiejar.load('cookies/' + str(user_id) + '.txt', ignore_discard=True, ignore_expires=True)
  # 工具方法转换成字典
  load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
  # 工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
  session = requests.Session()
  session.cookies = requests.utils.cookiejar_from_dict(load_cookies)
  # 可以用cookie保存登录信息
  # 也可以用weibo api登陆
  #cookie = {"Cookie": "#your cookie"}
  url = 'http://weibo.cn/%d/profile'%user_id
  #print user_id
  #print url
  # html = requests.get(url, cookie = cookie).content
  html = session.get(url).content
  fhtml = open('a.txt','wb')
  fhtml.write(html)
  selector = etree.HTML(html)
  pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
  print u'你共有%d页微博' %pageNum
  print u'点击查看:'+ url
  '''
  result = ""
  urllist_set = set()
  word_count = 1
  image_count = 1
  '''
  startpage = (int)(raw_input(u"请输入删除开始页面（如1，包含1）: "))
  endpage = (int)(raw_input(u"请输入删除结束页面（如5，包含5）: "))
  for page in range(startpage,endpage+1):
    print page
    #获取lxml页面
    url = 'http://weibo.cn/%d/profile?&page=%d'%(user_id,page)
    lxml = session.get(url).content
    ids = re.findall(r'(?<=M_).*?(?=\")', lxml)
    #print ids
    return ids

    '''
    #文字爬取
    selector = etree.HTML(lxml)
    content = selector.xpath('//span[@class="ctt"]')
    weiboid = selector.xpath('//span[@class="ctt"]')
    print content
    for each in content:
      text = each.xpath('string(.)')

      if word_count>=4:
        text = "%d :"%(word_count-3) +text+"\n\n"
      else :
        text = text+"\n\n"
      result = result + text
      word_count += 1
    '''
    '''
    #图片爬取
    soup = BeautifulSoup(lxml, "lxml")
    urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
    first = 0
    for imgurl in urllist:
      urllist_set.add(session.get(imgurl['href']).url)
      image_count +=1
    '''
  '''
  fo = open("users/%d"%user_id, "wb")
  fo.write(result.encode('utf-8'))
  word_path=os.getcwd()+'/%d'%user_id
  print u'文字微博爬取完毕'
  '''


'''
  link = ""
  fo2 = open("/Users/%d_imageurls"%user_id, "wb+")
  for eachlink in urllist_set:
    link = link + eachlink +"\n"
  fo2.write(link)
  print u'图片链接爬取完毕'


  if not urllist_set:
    print u'该页面中不存在图片'
  else:
    #下载图片,保存在当前目录的pythonimg文件夹下
    image_path=os.getcwd()+'/weibo_image'
    if os.path.exists(image_path) is False:
      os.mkdir(image_path)
    x=1
    for imgurl in urllist_set:
      temp= image_path + '/%s.jpg' % x
      print u'正在下载第%s张图片' % x
      try:
        urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp)
      except:
        print u"该图片下载失败:%s"%imgurl
      x+=1

  print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
  print u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path)
'''

def delWeibo(uid, ids):
    # 实例化一个LWPCookieJar对象
    load_cookiejar = cookielib.LWPCookieJar()
    # 从文件中加载cookies(LWP格式)
    load_cookiejar.load('cookies/' + str(uid) + '.txt', ignore_discard=True, ignore_expires=True)
    # 工具方法转换成字典
    load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
    # 工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict(load_cookies)
    for i in ids:
        delete_url = 'http://weibo.cn/mblog/del?type=del&id=%s&act=delc&rl=1&st=892435'%i
        session.get(delete_url)
        print 'weibo id: ' + i +'  deleted'
    print "delete done！"
if __name__ == "__main__":
  reload(sys)
  sys.setdefaultencoding('utf-8')
  if(len(sys.argv)>=2):
      user_id = (int)(sys.argv[1])
  else:
      user_id = (int)(raw_input(u"请输入user_id: "))

  spider(user_id)