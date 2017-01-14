#!/usr/bin/python
import esp
import confrw
import os

 
def get_text_file(filename):
        f = open(filename, "r")
        content = f.read()
        f.close() 
        return content


filename = r'conf.ini'
if os.path.exists(filename):
    b=get_text_file(filename)
    if "bg" in b and "g" in b and "f" in b and "stv" in b and "env" in b:
        esp.main()
    #os.remove(filename)
    else:
        confrw.confcr()
        esp.main()
else:
    confrw.confcr()
    esp.main()

