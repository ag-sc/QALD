#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/cunger/local/lib/python2.7/site-packages/SPARQLWrapper-1.5.2-py2.7.egg")

import xml.dom.minidom as dom
import xml.dom
import os
import socket
import re
import datetime
import codecs

from SPARQLWrapper import SPARQLWrapper, JSON

en_sparql = SPARQLWrapper("http://vtentacle.techfak.uni-bielefeld.de:443/sparql/")
es_sparql = SPARQLWrapper("http://es.dbpedia.org/sparql/")

es = False

# Dokument erzeugen
implement = xml.dom.getDOMImplementation()

#dbpedia_Server="http://vtentacle.techfak.uni-bielefeld.de:443/sparql/?default-graph-uri=&query="
#restdbpedia="&format=text%2Fhtml&debug=on&timeout="
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
    try:
        string =  knoten.firstChild.data.strip().encode("utf-8")
        return string

    except:
#        print "Error in knoten auslesen"
#        print "Unexpected error:", sys.exc_info()[0]
        pass

    
def lade_baum(dateiname): 
    d = {} 
    c={}
#    baum = None
#    with codecs.open(dateiname, "r", "utf-8") as in_f:
#        #doc.writexml(out)
#        baum = dom.parse(in_f)
    baum = dom.parse(dateiname.encode( "utf-8" ))
    global knoten_id
    global es

    try:
        zaehler=1
        for eintrag in baum.firstChild.childNodes: 
            if(zaehler==1):
                knoten_id=((eintrag.parentNode).attributes["id"]).value
		if knoten_id.startswith("esdbpedia"): es = True
                zaehler=2
            id=""
            answertype=""
            fusion=""
            aggregation=""
            onlydbo=""
            onlyesdbp = ""
            strinbla=""
            keywords = []
            questions = []
            try: 
                if eintrag.nodeName == "question": 
                    #=eintrag.attributes["id"]
                    #id=a.value
                    id=(eintrag.attributes["id"]).value
                    #id=id
                    
                    try:
                        answertype=(eintrag.attributes["answertype"]).value
                    except Exception:
                        answertype="ERROR"
                       
                    try:
                        fusion=(eintrag.attributes["fusion"]).value
                    except Exception:
                        fusion="ERROR"
                        
                    try:    
                        aggregation=(eintrag.attributes["aggregation"]).value
                    except Exception:
                        aggregation="ERROR"
                        
                    try:
                        onlydbo=(eintrag.attributes["onlydbo"]).value
                    except Exception:
                        onlydbo="ERROR"
                        
                    try:
                        onlyesdbp=(eintrag.attributes["onlyesdbp"]).value
                    except Exception:
                        onlyesdbp="ERROR"
                        
                    #print(id)
                    english_question_text = query = None
                    #print(eintrag.Attr)

                    for knoten in eintrag.childNodes: 
                        if knoten.nodeName == "string" or knoten.nodeName == "text": 
                            
                            if (knoten.attributes["lang"]).value == "en":
                                english_question_text = _knoten_auslesen(knoten)
                                questions.append([english_question_text,"en"])
                                error_string = english_question_text
                                
                            elif (knoten.attributes["lang"]).value == "de":
                                try:
                                    questions.append([_knoten_auslesen(knoten),"de"])
                                except:
                                    questions.append(["","de"])
                                    
                            elif (knoten.attributes["lang"]).value == "es":
                                try:
                                    questions.append([_knoten_auslesen(knoten),"es"])
                                except:
                                    questions.append(["","es"])
                                    
                            elif (knoten.attributes["lang"]).value == "it":
                                try:
                                    questions.append([_knoten_auslesen(knoten),"it"])
                                except:
                                    questions.append(["","it"])
                                    
                            elif (knoten.attributes["lang"]).value == "fr":
                                try:
                                    questions.append([_knoten_auslesen(knoten),"fr"])
                                except:
                                    questions.append(["","fr"])
                                    
                            elif (knoten.attributes["lang"]).value == "nl":
                                try:
                                    questions.append([_knoten_auslesen(knoten),"nl"])
                                except:
                                    questions.append(["","nl"])
                                
                        
                        elif knoten.nodeName == "keywords":
                            if (knoten.attributes["lang"]).value == "en":
                                try:
                                    keywords.append([_knoten_auslesen(knoten),"en"])
                                except:
                                    keywords.append(["","en"])
                                    
                            elif (knoten.attributes["lang"]).value == "de":
                                try:
                                    keywords.append([_knoten_auslesen(knoten),"de"])
                                except:
                                    keywords.append(["","de"])
                                    
                            elif (knoten.attributes["lang"]).value == "es":
                                try:
                                    keywords.append([_knoten_auslesen(knoten),"es"])
                                except:
                                    keywords.append(["","es"])
                                    
                            elif (knoten.attributes["lang"]).value == "it":
                                try:
                                    keywords.append([_knoten_auslesen(knoten),"it"])
                                except:
                                    keywords.append(["","it"])
                                    
                            elif (knoten.attributes["lang"]).value == "fr":
                                try:
                                    keywords.append([_knoten_auslesen(knoten),"fr"])
                                except:
                                    keywords.append(["","fr"])
                                    
                            elif (knoten.attributes["lang"]).value == "nl":
                                try:
                                    keywords.append([_knoten_auslesen(knoten),"nl"])
                                except:
                                    keywords.append(["","nl"])
                                    
                            
                        elif knoten.nodeName == "query": 
                    #query = _knoten_auslesen(knoten)
                            query=knoten.firstChild.data.strip()
                            #print "found query: "+str(query)
                            
                            #add here at the end array with keywords and all language questions
                    d[english_question_text] = [query,id,answertype,fusion,aggregation, onlydbo, questions, keywords, onlyesdbp]
                    
            except Exception as inst:
                d[error_string] = ["error",id,answertype,fusion,aggregation, onlydbo, questions, keywords, onlyesdbp]
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
    for english_question, attributes in d.iteritems(): 

        questionElem = doc.createElement('question')

        newatt=doc.createAttribute("id")
        newatt.nodeValue=attributes[1]
        #print attributes[1]
        questionElem.setAttributeNode(newatt)
        
        if("ERROR" not in attributes[2]):
            newatt=doc.createAttribute("answertype")
            newatt.nodeValue=attributes[2]
            questionElem.setAttributeNode(newatt)
        
        if("ERROR" not in attributes[3]):
            newatt=doc.createAttribute("fusion")
            newatt.nodeValue=attributes[3]
            questionElem.setAttributeNode(newatt)
        
        if("ERROR" not in attributes[4]):
            newatt=doc.createAttribute("aggregation")
            newatt.nodeValue=attributes[4]
            questionElem.setAttributeNode(newatt)
            
        if("ERROR" not in attributes[5]):
            newatt=doc.createAttribute("onlydbo");
            newatt.nodeValue=attributes[5];
            questionElem.setAttributeNode(newatt);
            
        if("ERROR" not in attributes[8]):
            newatt=doc.createAttribute("onlyesdbp");
            newatt.nodeValue=attributes[8];
            questionElem.setAttributeNode(newatt);


        for item in attributes[6]:
            nameElem = doc.createElement('string')
            questionElem.appendChild(nameElem)
            #print(english_question)
            newatt_en=doc.createAttribute("lang")
            newatt_en.nodeValue=item[1]
            nameElem.setAttributeNode(newatt_en)
            nameTextElem = doc.createTextNode(item[0])
            nameElem.appendChild(nameTextElem)
               
        for item in attributes[7]:
            nameElem = doc.createElement('keywords')
            questionElem.appendChild(nameElem)
            #print(english_question)
            newatt_en=doc.createAttribute("lang")
            newatt_en.nodeValue=item[1]
            nameElem.setAttributeNode(newatt_en)
            nameTextElem = doc.createTextNode(item[0])
            nameElem.appendChild(nameTextElem)
        
        
        
        querryElem = doc.createElement('query')
        questionElem.appendChild(querryElem)
        #askElement = doc.createTextNode(attributes[0])
        askElement = doc.createTextNode("")
        querryElem.appendChild(askElement)
        #print(SPquery)
        
        answerElem = doc.createElement('answers')
        questionElem.appendChild(answerElem)
        if("OUT OF SCOPE" not in attributes[0]):
            if("ask" in attributes[0].lower()):
                answerElem_small = doc.createElement('answer')
                answerElem.appendChild(answerElem_small)       
    
                small_answer=doc.createElement("boolean")
                answerElem_small.appendChild(small_answer)
                askElement = doc.createTextNode(askQuery(attributes[0]))
                small_answer.appendChild(askElement)
    
                            
            else:
    
                try:
                    #d=sparql_anfrage_wget(_serverAnfrage_)
                    d = selectQuery(attributes[0])
                    
                except Exception as inst:
                    error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>Could not load the given XML File.</p></body></html>"
                    outfile=open(filename_out_html,"w")
                    outfile.write(error)
                    outfile.close()
                    _ausgabe_(filename_out_html) 
                    exit(1)
                if(d==0):
                    error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>Query number "+str(attributes[1])+" could not be parsed by the Server. Please correct the query.</p></body></html>"
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
                            askElement = doc.createTextNode(bereinigt.encode( "utf-8" ))
    
    
                            small_answer.appendChild(askElement)
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
    
                            askElement = doc.createTextNode(bereinigt.encode( "utf-8" ))
    
                            anschriftTextElem1 = doc.createTextNode(bereinigt1.encode( "utf-8" ))
                            
                            small_answer.appendChild(askElement)
                            small_answer1.appendChild(anschriftTextElem1)
                                                    
                    if(len(d)==0):
                        answerElem_small = doc.createElement('answer')
                        answerElem.appendChild(answerElem_small)
                        askElement = doc.createTextNode("") # ("ERROR NO FILES ON SERVER")
                        answerElem.appendChild(askElement)
                        
    
                            
                            #i=i+1
                            #questionElem.documentElement.appendChild(querryElem)
            
        doc.documentElement.appendChild(questionElem)

    datei = open(filename_out_xml, "w")

    try:
        doc.writexml(datei, "\n", "")
    except:
        print "Unexpected error:", sys.exc_info()[0]

    datei.close()
    
    fobj = open(filename_out_xml, "r") 
    string=""
    dataset_id="<dataset id=\""+str(knoten_id)+"\">"
    #print knoten_id
    replace = str.replace
    for line1 in fobj: 
        line=str(line1)
        line=replace(line,'<dataset>',dataset_id)
        line=replace(line,"&lt;","<")
        line=replace(line,"&gt;",">")
        line=replace(line,"&amp;&amp;","&&")
        line=replace(line,"</query>","]]></query>")
        line=replace(line,"</keywords>","]]></keywords>")
        line=replace(line,"<query>","<query><![CDATA[")
        #line=replace(line,"<string>","<string><![CDATA[")
        line=replace(line,"<string lang=\"en\">","<string lang=\"en\"><![CDATA[")
        line=replace(line,"<string lang=\"de\">","<string lang=\"de\"><![CDATA[")
        line=replace(line,"<string lang=\"es\">","<string lang=\"es\"><![CDATA[")
        line=replace(line,"<string lang=\"it\">","<string lang=\"it\"><![CDATA[")
        line=replace(line,"<string lang=\"fr\">","<string lang=\"fr\"><![CDATA[")
        line=replace(line,"<string lang=\"nl\">","<string lang=\"nl\"><![CDATA[")
        
        line=replace(line,"<keywords lang=\"en\">","<keywords lang=\"en\"><![CDATA[")
        line=replace(line,"<keywords lang=\"de\">","<keywords lang=\"de\"><![CDATA[")
        line=replace(line,"<keywords lang=\"es\">","<keywords lang=\"es\"><![CDATA[")
        line=replace(line,"<keywords lang=\"it\">","<keywords lang=\"it\"><![CDATA[")
        line=replace(line,"<keywords lang=\"fr\">","<keywords lang=\"fr\"><![CDATA[")
        line=replace(line,"<keywords lang=\"nl\">","<keywords lang=\"nl\"><![CDATA[")
        line=replace(line,"<string>","<string><![CDATA[")
        line=replace(line,"</string>","]]></string>")
        line=replace(line,"&quot;@en","")
        line=replace(line,"&quot;","")
        string+=line
    fobj.close()
   # print string
    fobj = open(filename_out_xml, "w") 
    fobj.write(string) 
    fobj.close()
    _ausgabe_(filename_out_xml) 
    exit(0)

def inhalt_ueberpruefen(anfrage):
    anfrage = anfrage.replace("\"","")
    anfrage = anfrage.replace("@en","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#date>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#int>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#string>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#number>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#boolean>","")
    anfrage=anfrage.replace("\"","")
    if("http" in anfrage):
        return 0
    #if(re.match('^\s*[1-9][0-9][0-9][0-9][-][0-9][0-9][-][0-9][0-9]\s*$',anfrage)):
    if(re.match('^[0-9]*[-][0-9,-]*\W*$',anfrage)):
    #    print anfrage
        return 2
    if(re.match('^[0-9,\.]*$',anfrage)):
        return 3
    else:
        return 1

def antwort_bereinigen(anfrage):
    anfrage=anfrage.replace(u'\ä','ae')
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#date>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#int>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#string>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#number>","")
    anfrage=anfrage.replace("^^<http://www.w3.org/2001/XMLSchema#boolean>","")
    anfrage=anfrage.replace(u'\Ä','Ae')
    anfrage=anfrage.replace(u'\ö','oe')
    anfrage=anfrage.replace(u'\Ö','Oe')
    anfrage=anfrage.replace(u'\ü','ue')
    anfrage=anfrage.replace(u'\Ü','ue')
    anfrage=anfrage.replace(u'ß','ss')
    return anfrage



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
 



def askQuery(query):
    #print query
    if es: sparql = es_sparql
    else:  sparql = en_sparql
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        #print str(results)
        for result in results:

            try:
                string = str(results[result])
                if "True" in string:
                    return "True"
            except:
                return "False"
    except:
        return "False"
        
    return "False"

def selectQuery(query):
    if es: sparql = es_sparql
    else:  sparql = en_sparql
    array = []
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        select_term = ""
        for result in results["head"]["vars"]:
            select_term = result
        for result in results["results"]["bindings"]:
            try:
                string1 = result[select_term]["value"]
                array.append(string1)
            except:
                #print "Unexpected error:", sys.exc_info()[0]
                pass
    except:
        pass
    return array
        


if __name__ == "__main__":
    main()
    
