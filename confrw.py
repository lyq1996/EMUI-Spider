#!/usr/bin/python
#-*-coding:utf-8-*-
import ConfigParser 

        
def confread():
        conf = ConfigParser.ConfigParser()
        conf.read("conf.ini")
        G = conf.get("conf", "bg")
        g = conf.get("conf","g")
        f = conf.get("conf","f")
        stv = conf.get("conf","stv")
        env = conf.get("conf","env")
        a = []
        a.append(G)
        a.append(g)
        a.append(f)
        a.append(stv)
        a.append(env)
        return a



def confcr():
        f=file("conf.ini","w+")
        con=["[conf]\n","bg =\n","g =\n","f =\n","stv=\n","env =\n"]
        f.writelines(con)
        f.close()

def confwriteG(a):
        conf = ConfigParser.ConfigParser()
        conf.read("conf.ini")
        conf.set("conf", "bg", a)
        conf.write(open("conf.ini", "w"))
        
def confwriteg(a):
        conf = ConfigParser.ConfigParser()
        conf.read("conf.ini")
        conf.set("conf", "g", a)
        conf.write(open("conf.ini", "w"))

        
def confwritef(a):	
        conf = ConfigParser.ConfigParser()
        conf.read("conf.ini")
        conf.set("conf", "f", a)
        conf.write(open("conf.ini", "w")) 

def confwritesv(a):
                        
        conf = ConfigParser.ConfigParser()
        conf.read("conf.ini")
        conf.set("conf", "stv", a)
        conf.write(open("conf.ini", "w")) 	

def confwriteev(a):
        conf = ConfigParser.ConfigParser()
        conf.read("conf.ini")
        conf.set("conf", "env", a)
        conf.write(open("conf.ini", "w"))
