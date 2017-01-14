# -*- coding: utf-8 -*-
import urllib2
import re
import wx
import threading
import sys
import confrw
import os
import time

class MainApp(wx.App):
    
    def OnInit(self):
       frame = MainFrame(u'EMUI版本检测工具', (500, 200), (260, 350))
       frame.SetMaxSize((260,350))
       frame.SetMinSize((260,350))
       frame.Center()
       frame.Show() 
       self.SetTopWindow(frame)
       return True
    
class MainFrame(wx.Frame):
    
    def __init__(self, title, pos, size):
        self.valueG = ''
        self.valueg = ''
        self.valuef = ''
        self.valuesv = ''
        self.valueev = ''
        self.threads = []
        self.version1 = ''
        self.updateconf()
        wx.Frame.__init__(self, None, -1, title, pos, size)
        menuFile = wx.Menu()
        menuFile.Append(1, u'&使用说明...',u'使用说明')
        menuFile.Append(2, u'联系作者')
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, u'&关于和更多')
        self.SetMenuBar(menuBar) 
        self.Bind(wx.EVT_MENU,self.OnAbout,id=1)
        self.Bind(wx.EVT_MENU,self.Onlxw,id=2)
        self.CreateStatusBar() 
        self.SetStatusText(u"欢迎使用-->请看关于和更多-->使用说明")
        panel = wx.Panel(self) 
        self.sp = wx.Button(panel,label=u"寻找",pos=(38, 196),size=(80, 25)) 
        self.esp = wx.Button(panel,label=u"停止",pos=(122,196),size=(80,25))
        wx.StaticText(panel, -1, u"G:", pos=(38, 50))
        self.G = wx.TextCtrl(panel, -1,self.valueG ,pos=(90, 50))
        self.G.SetInsertionPoint(0) 
        wx.StaticText(panel,-1, u"g:",pos=(38,77))
        self.g = wx.TextCtrl(panel, -1 ,self.valueg,pos=(90, 77))
        self.g.SetInsertionPoint(0)
        wx.StaticText(panel,-1, u"f:",pos=(38,104))
        self.f = wx.TextCtrl(panel, -1 ,self.valuef,pos=(90, 104))
        self.f.SetInsertionPoint(0)
        wx.StaticText(panel,-1, u"起始v:",pos=(38,131))
        self.sv = wx.TextCtrl(panel, -1 ,self.valuesv,pos=(90, 131))
        self.sv.SetInsertionPoint(0)
        wx.StaticText(panel,-1, u"结束v:",pos=(38,158))
        self.ev = wx.TextCtrl(panel, -1,self.valueev,pos=(90, 158))
        self.ev.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT,self.OnG,self.G)
        self.Bind(wx.EVT_TEXT,self.Ong,self.g)
        self.Bind(wx.EVT_TEXT,self.Onf,self.f)
        self.Bind(wx.EVT_TEXT,self.Onsv,self.sv)
        self.Bind(wx.EVT_TEXT,self.Onev,self.ev)
        self.esp.Disable()
        self.Bind(wx.EVT_BUTTON,self.Onstart,self.sp)
        self.Bind(wx.EVT_BUTTON,self.Onstop,self.esp)
        self._EnableOrDisableOkBtn() 
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) 

    def OnCloseWindow(self, event):
        while self.threads:
            self.StopThreads1()
            time.sleep(0.5)
            sys.exit()
        else:
            sys.exit()

    def updateconf(self):
        self.a=confrw.confread()
        self.valueG = self.a[0]
        self.valueg = self.a[1]
        self.valuef = self.a[2] 
        self.valuesv = self.a[3]
        self.valueev = self.a[4]    

    def log(self, msg):
        msg = unicode(msg)
        self.SetStatusText(msg)


    def Onev(self,event):
        self._EnableOrDisableOkBtn()  

    def Onsv(self,event):
        self._EnableOrDisableOkBtn()  
        
    def Onf(self,event):
        self._EnableOrDisableOkBtn()  

    def Ong(self,event):
        self._EnableOrDisableOkBtn()  
              
    def OnG(self,event):
        self._EnableOrDisableOkBtn()

    def _EnableOrDisableOkBtn(self):
        self.sp.Disable()
        self.valueG = self.G.GetValue()
        self.valueg = self.g.GetValue()
        self.valuef = self.f.GetValue()
        self.valuesv = self.sv.GetValue()
        self.valueev = self.ev.GetValue()
        if not self.valueG=='' and not self.valueg==''and not self.valuesv=='' and not self.valuef ==''and not self.valueev=='':
            self.sp.Enable()
            self.Writeconf()

    def Onnone(self,event):
        return True

    def Writeconf(self):
        confrw.confwriteG(self.valueG)
        confrw.confwriteg(self.valueg)
        confrw.confwritef(self.valuef)
        confrw.confwritesv(self.valuesv)
        confrw.confwriteev(self.valueev)


    def OnAbout(self,event):
        wx.MessageBox(u'这是一个爬取EMUI版本的爬虫！\n可开多个进程\n在主界面填上G/g/v/f对应的值即可扫描华为网盘\n如果你需要需要更老的版本，请移步:\nhttp://www.lcblues.cn/emui.html\n这是本人寻找的官方包和下载地址\n当然你也可以自己寻找\n这里提供几个标识给你~\nG1348/g104/v58146/f1----B120\nG1288/g88/v58743/f1----B136\nG1286/g88/v63947/f1----B160\nG1278/g104/v67572/f1----B322\nG1278/g104/v69778/f1----极客12.16\n爬完会生成一个txt文档在当前目录，GoodLuck！')


    def Onlxw(self,event):
        wx.MessageBox(u'联系我：\nQQ:947432168')


    def savever(self,ver):
        if not self.version1 == '':
            self.version1 = self.version1+ '\n' + ver
        else:
            self.version1 = ver
        

    def Onstart(self,event):
        self.timeupdate()
        self.OnStartThread()
        self.sp.Disable()
        self.esp.Enable()
        self.G.SetEditable(False)
        self.g.SetEditable(False)
        self.f.SetEditable(False)
        self.sv.SetEditable(False)
        self.ev.SetEditable(False)
        self.SetStatusText(u'开始寻找中...')


    def timeupdate(self):
        self.time = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())) 

    def Onstop(self,event):
        self.StopThreads()
        
    def OnStartThread(self):
        thread = WorkerThread(self.valueG,self.valueg,self.valuef,self.valuesv,self.valueev,self.time,self)
        self.threads.append(thread)
        thread.start()

    
    def StopThreads(self):
        self.G.SetEditable(True)
        self.g.SetEditable(True)
        self.f.SetEditable(True)
        self.sv.SetEditable(True)
        self.ev.SetEditable(True)
        while self.threads:
            thread = self.threads[0]
            thread.stop()
            self.threads.remove(thread)
            self.sp.Enable()
            self.esp.Disable()
            filename =self.time+'.txt'
            if os.path.exists(filename):
                self.SetStatusText(u"已停止！")
                msgbox = wx.MessageDialog(None, u'是否打开文件查看获取到的版本和下载地址？\n以下是获取到的版本:\n'+self.version1,u'已停止',wx.YES_NO | wx.ICON_QUESTION)
                ret = msgbox.ShowModal()
                if (ret == wx.ID_YES):
                    os.system(filename)
                    self.version1 = ''
                self.version1 = ''
            else:
                wx.MessageBox(u'没有获取到...请使用其他的G/g/f/v..')
                self.SetStatusText(u"已停止！")
                self.version1 = ''

    def StopThreads1(self):
        thread = self.threads[0]
        thread.stop()
        self.threads.remove(thread) 

class WorkerThread(threading.Thread):
    
    def __init__(self,G,g,f,sv,ev,tm,window):
        threading.Thread.__init__(self)
        baseURL = u'http://update.hicloud.com:8180/TDS/data/files/p3/s15/G1278/g104/v67572/f1/full/changelog.xml'
        self.G = G
        self.g = g
        self.f = f
        self.sv = int(sv)
        self.ev = int(ev)
        self.time = tm
        mark = 'G'+str(self.G)+u'/g'+str(self.g)
        self.url1 = baseURL.replace(u'G1278/g104',mark)
        mark2 = 'f'+str(self.f)
        self.url1 = self.url1.replace(u'f1',mark2)
        self.window=window
        self.threadNum = 1
        self.timeToQuit = threading.Event()

    def getPage(self,config):
        try:
            url = self.url1.replace(u'67572',str(config))
            request = urllib2.Request(url)
            response = urllib2.urlopen(request).read()
            return response,url
        except urllib2.HTTPError:
            return ['','']


        
    def version(self,config):
        rep = self.getPage(config)
        html = rep[0]
        url2 = rep[1]
        url2 = url2.replace('changelog.xml','update.zip')
        if not html ==''and not url2 =='':
            reg = re.compile(r'version=(.*?)/>')
            items = re.findall(reg,html)
            remove1 = re.compile(r'<.*?>')
            html = re.sub(remove1,'',html)
            items.append(url2)
            name =self.time+'.txt'
            f = open(name,'a')
            f.write(('Version:\t')+items[0]+'\n')
            f.write('Download link:\t'+items[1]+'\n')
            f.write('Changelog:\t'+html+'\n\n\n')
            f.close()
            wx.CallAfter(self.window.savever,items[0])
            return u'发现新版本'+items[0]+'...'
        else:
            return ''
             
    def stop(self):
        self.timeToQuit.set()
    
    def run(self):
        self.timeToQuit.wait(1)
        while self.sv <=self.ev:
            if self.timeToQuit.isSet():
                break
            else:
                a = self.version(self.sv)
                if not a == '':
                    wx.CallAfter(self.window.log,a)
            self.sv = self.sv+1
            time.sleep(0.5)
        wx.CallAfter(self.window.StopThreads)

def main():
    app = MainApp()
    app.MainLoop()

if __name__ == '__main__':
    main()
