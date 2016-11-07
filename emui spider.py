#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import sys
def input_():
    while True:
        model = raw_input("Select your devices model (1:For FRD-AL00 & CL00 & AL10):\n")
        if not model.strip()=='' :
            break
    model = str(model)
    return model

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

model = input_()

for y in range(64000,66000):
    if model=='1':
        x='http://update.hicloud.com:8180/TDS/data/files/known/v58146/f1/full/changelog.xml'
        x=x.replace("known","p3/s15/G1348/g104")
        x=x.replace("58146",str(y))
        y=y+1
        html = getHtml(x)
        if "升级" in html:
            x = x.replace("changelog.xml","update.zip")
            print html,str("Find new version:\n"),x
