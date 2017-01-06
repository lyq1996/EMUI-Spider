# -*- coding: utf-8 -*-
import urllib2
import re
import wx
import threading

baseURL = 'http://update.hicloud.com:8180/TDS/data/files/p3/s15/G1278/g104/v67572/f1/full/changelog.xml'

def getPage(mark,config):
    try:
        
        url = baseURL.replace("67572",str(config))
        url = url.replace("G1278/g104",str(mark))
        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()
        return response,url
    except urllib2.HTTPError:
        return ['','']



    
def version(mark,config):
    rep = getPage(mark,config)
    html = rep[0]
    remove1 = re.compile('<.*?>')
    remove2 = re.compile('2052.*?')
    remove3 = re.compile('fa.*?lse')
    remove4 = re.compile('tr.*?ue')
    remove5 = re.compile('\n.*?')
    html2 = re.sub(remove1,'',html)
    html2 = re.sub(remove2,'',html2)
    html2 = re.sub(remove3,'',html2)
    html2 = re.sub(remove4,'',html2)
    html2 = re.sub(remove5,'',html2)
    url2 = rep[1]
    url2 = url2.replace("changelog.xml",'update.zip')
    if not html ==''and not url2 =='':
        reg = re.compile(r'<component name="TCPU" version="(.*?)"/>')
        items = re.findall(reg,html)
        items.append(url2)
        items.append(html2)
        print u"发现新版本",items[0],'.....'
        f = open('getversion.txt','a')
        f.write('版本:'+'  '+items[0]+'\n')
        f.write('下载地址:'+'  '+items[1]+'\n')
        f.write('更新日志:'+'\n'+items[2]+'\n\n\n')
        f.close()

def input_():
    while True:
        model = raw_input(u"输入要爬取的标识以及起始地址:\n例如(G1278/g104/v67572)表示从v67572爬到v80000，并爬取所有版本的更新日志:\n")
        if not model.strip()=='' :
            break
    model = str(model)
    return model

print u"这是一个爬取EMUI版本的小爬虫！\n这里提供几个标识给你~\nG1348/g104/v58146----B120\nG1288/g88/v58743----B136\nG1286/g88/v63947----B160\nG1278/g104/v67572----B322"
print u"\n现在你可以自己爬了，爬完会生成一个txt文档在当前目录"
mark = input_()
sStr1 = mark[0:10]
sStr2 = mark[12:]
print u"现在即将爬取从",mark,u"到",sStr1,u"/v80000的所有版本"
for y in range(int(sStr2),80000):
    version(sStr1,y)
