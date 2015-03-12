#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.dom.minidom as dom
import xml.dom
import os
import socket
import re
import sys
import datetime
#Version 3

# Dokument erzeugen
implement = xml.dom.getDOMImplementation()

dbpedia_Server="http://greententacle.techfak.uni-bielefeld.de:5171/sparql?default-graph-uri=&query="
restdbpedia="&format=text%2Fhtml&debug=on&timeout="
filename_out_html = None
filename_out_xml = None
knoten_id = None

def set_filename_xml_out(time):
    global filename_out_xml
    filename_out_xml="upload/out"+str(time)+".xml"
    
def set_filename_out(time):
    global filename_out_html
    filename_out_html="upload/out"+str(time)+".html"
    
    
    
def _knoten_auslesen(knoten): 
    return eval("%s('%s')" % (knoten.getAttribute("typ"), 
                              knoten.firstChild.data.strip()))

def lade_baum(dateiname): 
    d = {} 
    c={}
    baum = dom.parse(dateiname.encode( "utf-8" ))
    global knoten_id

    try:
        zaehler=1
        for eintrag in baum.firstChild.childNodes: 
            if(zaehler==1):
                knoten_id=((eintrag.parentNode).attributes["id"]).value
                zaehler=2
            blaid=""
            strinbla=""
            try:
                if eintrag.nodeName == "question": 
                    a=eintrag.attributes["id"]
                    id=a.value
                    blaid=id
                    #print(id)
                    question_text = query = None
                    #print(eintrag.Attr)

                    for knoten in eintrag.childNodes: 
                        if knoten.nodeName == "string" or knoten.nodeName == "text": 
                            question_text = _knoten_auslesen(knoten) 
                            stringbla = question_text
                        elif knoten.nodeName == "query": 
                    #query = _knoten_auslesen(knoten)
                            query=knoten.firstChild.data.strip()
                    d[question_text] = query+"HALLO"+id
            except Exception as inst:
                d[stringbla] = "error"+"HALLO"+blaid
                #print(inst)
                #print"Error"
                #print "\n"

    except Exception as inst:
    	error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>Could not load the given XML File.</p></body></html>"
        outfile=open(filename_out_html,"w")
        outfile.write(error)
        outfile.close()
        _ausgabe_(filename_out_html) 
        exit(1)
    else:
        return d

def schreibe_baum(d, dateiname): 
    bla = "dataset"
    doc = implement.createDocument(None, "dataset", None)
    #doc.createAttribute("hey")
    #(doc.documentElement).createAttribute("hey")
    
    for ReturnQuery, SPquery in d.iteritems(): 
        c=SPquery.split("HALLO")


        questionElem = doc.createElement('question')

        newatt=doc.createAttribute("id");
        newatt.nodeValue=c[1];
        
        questionElem.setAttributeNode(newatt);


        nameElem = doc.createElement('string')
        questionElem.appendChild(nameElem)
	    #print(ReturnQuery)
        nameTextElem = doc.createTextNode(ReturnQuery)
        nameElem.appendChild(nameTextElem)
        
        querryElem = doc.createElement('query')
        questionElem.appendChild(querryElem)
        anschriftTextElem = doc.createTextNode(c[0])
        querryElem.appendChild(anschriftTextElem)
        #print(SPquery)
        
        answerElem = doc.createElement('answers')
        questionElem.appendChild(answerElem)
        #print(SPquery)
        _serverAnfrage_=dbpedia_Server+server_anfrage_erzeugen(c[0])+restdbpedia
        #_serverAnfrage_=musicbrainz_Server+server_anfrage_erzeugen(c[0])+restmusicbrainz
       # print _serverAnfrage_
        if("ASK" in c[0]):
            import urllib
            try:
                page = urllib.urlopen(_serverAnfrage_)
            except Exception as inst:
                error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>Could not load the given XML File.</p></body></html>"
                outfile=open(filename_out_html,"w")
                outfile.write(error)
                outfile.close()
                _ausgabe_(filename_out_html) 
                exit(1)
                            #print page.read()

            answerElem_small = doc.createElement('answer')
            answerElem.appendChild(answerElem_small)
                        

            small_answer=doc.createElement("boolean")
            answerElem_small.appendChild(small_answer)
            anschriftTextElem = doc.createTextNode(page.read())
            #print(anschriftTextElem)
            small_answer.appendChild(anschriftTextElem)

                        
        else:

            try:
                d=sparql_anfrage_wget(_serverAnfrage_)
            except Exception as inst:
                error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>Could not load the given XML File.</p></body></html>"
                outfile=open(filename_out_html,"w")
                outfile.write(error)
                outfile.close()
                _ausgabe_(filename_out_html) 
                exit(1)
            if(d==0):
                error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>Query number "+str(c[1])+" could not be parsed by the Server. Please correct the query.</p></body></html>"
                outfile=open(filename_out_html,"w")
                outfile.write(error)
                outfile.close()
                _ausgabe_(filename_out_html) 
                exit(1)
            if(d!=0):
                #schauen, ob die Kombination Uri/string vorhanden ist. 
                if((len(d)>=2 and inhalt_ueberpruefen(d[0])==inhalt_ueberpruefen(d[1])) or len(d)==1):

                    for i in range(0,len(d)) :
                        antwort=None
                        n=inhalt_ueberpruefen(d[i])
                        if(n==0):
                            antwort="uri"
                        if(n==1):
                            antwort="string"
                        if(n==2):
                            antwort="date"
                        if(n==3):
                            antwort="number"
                        
                        answerElem_small = doc.createElement('answer')
                        answerElem.appendChild(answerElem_small)
                        
                        small_answer=doc.createElement(antwort)
                        answerElem_small.appendChild(small_answer)
                        bereinigt=antwort_bereinigen(d[i])
                        anschriftTextElem = doc.createTextNode(bereinigt.encode( "utf-8" ))


                        small_answer.appendChild(anschriftTextElem)
                elif(len(d)>0):
                    for i in range(0,len(d)-1,2) :
                        antwort=None
                        n=inhalt_ueberpruefen(d[i])
                        if(n==0):
                            antwort="uri"
                        if(n==1):
                            antwort="string"
                        if(n==2):
                            antwort="date"
                        if(n==3):
                            antwort="number"
                            
                        m=inhalt_ueberpruefen(d[i+1])
                        if(m==0):
                            antwort1="uri"
                        if(m==1):
                            antwort1="string"
                        if(m==2):
                            antwort1="date"
                        if(m==3):
                            antwort1="number"
   
                        answerElem_small = doc.createElement('answer')
                        answerElem.appendChild(answerElem_small)
                        
                        small_answer=doc.createElement(antwort)
                        small_answer1=doc.createElement(antwort1)
                        
                        answerElem_small.appendChild(small_answer)
                        answerElem_small.appendChild(small_answer1)
                        

                        bereinigt=(antwort_bereinigen(d[i]))
                        bereinigt1=(antwort_bereinigen(d[i+1]))

                        anschriftTextElem = doc.createTextNode(bereinigt.encode( "utf-8" ))

                        anschriftTextElem1 = doc.createTextNode(bereinigt1.encode( "utf-8" ))
                        
                        small_answer.appendChild(anschriftTextElem)
                        small_answer1.appendChild(anschriftTextElem1)
                                                
                if(len(d)==0):
                    answerElem_small = doc.createElement('answer')
                    answerElem.appendChild(answerElem_small)
                    anschriftTextElem = doc.createTextNode("ERROR NO FILES ON SERVER")
                    answerElem.appendChild(anschriftTextElem)
                    

                        
                        #i=i+1
                        #questionElem.documentElement.appendChild(querryElem)
        
        doc.documentElement.appendChild(questionElem)
        
    #doc.encode( "utf-8" )
    datei = open(filename_out_xml, "w")
    doc.writexml(datei, "\n", "")
    #print(datei)
    datei.close()
    
    fobj = open(filename_out_xml, "r") 
    string=""
    dataset_id="<dataset id=\""+str(knoten_id)+"\">"
    print knoten_id
    for line1 in fobj: 
        line=str(line1)
        line=line.replace('<dataset>',dataset_id)
        string+=line
    fobj.close()
   # print string
    fobj = open(filename_out_xml, "w") 
    fobj.write(string) 
    fobj.close()
    _ausgabe_(filename_out_xml)

def inhalt_ueberpruefen(anfrage):
    if("http" in anfrage):
        return 0
    if(re.match('[1-9]*[-][0-9]*',anfrage)):
        return 2
    if(re.match('^[0-9]*$',anfrage)):
        return 3
    else:
        return 1

def antwort_bereinigen(anfrage):
    anfrage=anfrage.replace(u'\ä','ae')
    anfrage=anfrage.replace(u'\Ä','Ae')
    anfrage=anfrage.replace(u'\ö','oe')
    anfrage=anfrage.replace(u'\Ö','Oe')
    anfrage=anfrage.replace(u'\ü','ue')
    anfrage=anfrage.replace(u'\Ü','ue')
    anfrage=anfrage.replace(u'ß','ss')
    return anfrage

def server_anfrage_erzeugen(anfrage):
    
    anfrage=steuerzeichen_entfernen(anfrage)
    
    anfrage=anfrage.replace('&lt;','<')
    anfrage=anfrage.replace('%gt;','>')
    anfrage=anfrage.replace('&amp;','&')
    anfrage=anfrage.replace('#>','%23%3E%0D%0A%')
    anfrage=anfrage.replace(' ','+')
    anfrage=anfrage.replace('/','%2F')
    anfrage=anfrage.replace(':','%3A')
    anfrage=anfrage.replace('?','%3F')
    anfrage=anfrage.replace('$','%24')
    #anfrage=anfrage.replace('F&gt;+','F%3E%0D%0A')
    anfrage=anfrage.replace('>','%3E')
    anfrage=anfrage.replace('<','%3C')
    anfrage=anfrage.replace('"','%22')
    anfrage=anfrage.replace('\n','%0D%0A%09')
    anfrage=anfrage.replace('%%0D%0A%09','%09')
    anfrage=anfrage.replace('=','%3D')
    anfrage=anfrage.replace('@','%40')
    anfrage=anfrage.replace('&','%26')
    anfrage=anfrage.replace('(','%28')
    anfrage=anfrage.replace(')','%29')
    #anfrage=anfrage.replace('\n','.%0D%0A%09')
    
    return anfrage

def steuerzeichen_entfernen(anfrage):
    #alle steuerzeichen entfernen
    anfrage=anfrage.replace('\\','')
    anfrage=anfrage.replace('\a','')
    anfrage=anfrage.replace('\b','')
    anfrage=anfrage.replace('\f','')
    #anfrage=anfrage.replace('\n','.%0D%0A%09')
    anfrage=anfrage.replace('\r','')
    anfrage=anfrage.replace('\t','')
    anfrage=anfrage.replace('\v','')
    
    return anfrage

def pasrse_html_xml(dateiname):
    #ausgabe123.xml
    d = []
   # print("vorm laden")
    try:
        baum = dom.parse(dateiname)

        #print("#############################Abbruch in parse_html_xml#############################")
        for eintrag in baum.firstChild.childNodes: 
            if eintrag.nodeName == "tr": 
                schluessel = wert = None

                wert=1
                for knoten in eintrag.childNodes: 
                    if knoten.nodeName == "td": 
                        try:
                            schluessel = knoten.firstChild.data.strip()
                        except Exception:
                           # anschriftTextElem=" "
                           schluessel = " "
                    #schluessel = knoten.firstChild.data.strip()
		    #schluessel=_knoten_auslesen(knoten)
                        d.append(schluessel)
    except Exception:
        d.append("ERROR")  
    #print d           
    return d
        
def sparql_anfrage_wget(query):
    if(fFileExist("upload/antwort.html")==1):
        os.system("rm upload/antwort.html")
    anfrage="wget "+"\""+query+"\""+" -O upload/antwort.html"
    import urllib
    try:
        page = urllib.urlopen(query)
        outfile=open("upload/antwort.html","w")
        outfile.write(page.read())
        outfile.close()
    except Exception:
        return 0
    else:
        if(fFileExist("upload/antwort.html")==1):
            return pasrse_html_xml("upload/antwort.html")



def fFileExist(psFilePath):
   
    try:
        oFile = open(psFilePath,'r')
    except Exception:
        return 0
    else:
        oFile.close()
        return 1
   
   




def _ausgabe_(ausgabe):
    print ausgabe 
    
def main():
    dateiname=sys.argv[1]  
    system_time = datetime.datetime.now()
    set_filename_out(system_time)
    set_filename_xml_out(system_time)
    
    #dateiname = "musicbrainz-test-noanswers.xml"
    schreibe_baum(lade_baum(dateiname),"")
    #print("done")
 



if __name__ == "__main__":
    main()
    
