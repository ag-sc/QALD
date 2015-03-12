#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Version Jela! 6.0

import xml.dom.minidom as dom
import xml.dom
from decimal import *
import sys
import os
import datetime
#from Numeric import *


# Dokument erzeugen
implement = xml.dom.getDOMImplementation()

###################Globale Variablen###################
musicbrainz= False
dbpedia=False
musicbrainz_test=False
dbpedia_test=False
choosen_tag={}
system_time=0
filename_out_html = None
filename_out_txt = None
system_name=None
configuration=None
Pfad_Musterloesung_Musicbrainz_train=None
Pfad_Musterloesung_Dbpedia_train = None
Pfad_Musterloesung_Musicbrainz_test=None
Pfad_Musterloesung_Dbpedia_test = None
MLTrain=False
OutOfScopeQuestions=[]

#Pfad_Musterloesung-Dbpedia-train = "http://greententacle.techfak.uni-bielefeld.de/~cunger/qald1/dbpedia-train.xml"
#Pfad_Musterloesung-Musicbrainz-train="http://greententacle.techfak.uni-bielefeld.de/~cunger/qald1/musicbrainz-train.xml"
###################Funktionen##########################
def set_Pfade_Musterloesung():
    global Pfad_Musterloesung_Musicbrainz_train,Pfad_Musterloesung_Dbpedia_train,Pfad_Musterloesung_Musicbrainz_test,Pfad_Musterloesung_Dbpedia_test
    #Pfad_Musterloesung_Dbpedia_train = "../dbpedia-train.xml"
    Pfad_Musterloesung_Dbpedia_train ="dbpedia-train-answers.xml"
    Pfad_Musterloesung_Musicbrainz_train="musicbrainz-train-answers.xml"
    Pfad_Musterloesung_Dbpedia_test = "dbpedia-test.xml"
    Pfad_Musterloesung_Musicbrainz_test="musicbrainz-test.xml"   
    
    
def set_system_name(name):
    global system_name
    system_name=name
    
def set_configuration(name):
    global configuration
    configuration=name
    
    
def _ausgabe_(ausgabe):
    print ausgabe
    
def set_filename_txt_out(time):
    global filename_out_txt
    filename_out_txt="upload/out"+str(time)+".txt"
    
def set_filename_out(time):
    global filename_out_html
    filename_out_html="upload/out"+str(time)+".html"

def set_musicbrainz_test():
    global dbpedia,musicbrainz,musicbrainz_test,dbpedia_test
    musicbrainz=False
    dbpedia=False
    musicbrainz_test=True
    dbpedia_test=False
    
def set_dbpedia_test():
    global dbpedia,musicbrainz,musicbrainz_test,dbpedia_test
    musicbrainz=False
    dbpedia=False
    musicbrainz_test=False
    dbpedia_test=True
    

def set_dbpedia():
    global dbpedia,musicbrainz
    musicbrainz=False
    dbpedia=True

    

def set_musicbrainz():
    global dbpedia,musicbrainz
    dbpedia=False
    musicbrainz=True
    
    
def _knoten_auslesen(knoten): 
    return eval("%s('%s')" % (knoten.getAttribute("typ"), 
                              knoten.firstChild.data.strip()))




def lade_musterloesung(dateiname): 
    d = {} 
    global choosen_tag
    global OutOfScopeQuestions
    #baum = dom.parse(dateiname.encode( "utf-8" ))
    baum = dom.parse(dateiname)
    zaehler=1
    for eintrag in baum.firstChild.childNodes: 
              
        if eintrag.nodeName == "question": 
            id=(eintrag.attributes["id"]).value
            question_text = query = None
            answer=[]
            for knoten in eintrag.childNodes: 
                if knoten.nodeName == "text" or knoten.nodeName == "string": 
                    question_text = _knoten_auslesen(knoten) 
                elif knoten.nodeName == "query": 
                    query=knoten.firstChild.data.strip()
                    if("OUT OF SCOPE" in query):
                        OutOfScopeQuestions.append(id)
                        
                if knoten.nodeName=="answers":
                    answer_elem_1=[]
                    for knoten_answer in knoten.childNodes:
			#here i have to check for optional. 
                        if knoten_answer.nodeName=="answer":
                            answer_elem=[]
                                    
                            for knoten_answer1 in knoten_answer.childNodes:
                                for id_loesung,tag_loesung in choosen_tag.iteritems():
                                    if(id==id_loesung):
                                        if knoten_answer1.nodeName == "string" and choosen_tag[id]=="string":
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "boolean" and choosen_tag[id]=="boolean":
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "number"and choosen_tag[id]=="number":
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "date" and choosen_tag[id]=="date":
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "uri" and choosen_tag[id]=="uri":
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                
                            answer_elem_1.append(answer_elem)
                        
                    answer.append(answer_elem_1)
           # print(answer)
            d[id] = [query,question_text,answer]
    return d



def bearbeite_baum(dateiname):
    #setze Zeielnumbrueche, damit der Parser spaeter besser mit dem Dokument zurecht kommt
    fobj = open(dateiname, "r") 
    string=""
    for line1 in fobj: 
        line=str(line1)
        line=line.replace('<question','\n<question')
        #line=line.replace('<string>','\n<string>')
        line=line.replace('</string>','</string>\n')
        line=line.replace('</query>','</query>\n')
        line=line.replace('<answers>','<answers>\n')
        line=line.replace('<answer>','<answer>\n')
        line=line.replace('</answer>','</answer>\n')
        line=line.replace('</answers>','</answers>\n')
        line=line.replace('</uri>','</uri>\n')
        line=line.replace('</boolean>','</boolean>\n')
        line=line.replace('</number>','</number>\n')
        line=line.replace('</date>','</date>\n')
        #line=line.replace('&','&amp;')
        string+=line
    fobj.close()
   # print string
    fobj = open(dateiname, "w") 
    fobj.write(string) 
    fobj.close()
    
    return string

def lade_baum(dateiname): 
    d = {} 
    bearbeite_baum(dateiname)
    global choosen_tag
    baum = dom.parse(dateiname.encode( "utf-8" ))
    zaehler=1
    for eintrag in baum.firstChild.childNodes: 
        
        if(zaehler==1):
            knoten_id=((eintrag.parentNode).attributes["id"]).value
            if("musicbrainz-train" in knoten_id):
                set_musicbrainz()
            if("dbpedia-train" in knoten_id):
                set_dbpedia()
            if("dbpedia-test" in knoten_id):
                set_dbpedia_test()
	    if ("qald2-test" in  knoten_id):
	    	set_dbpedia_test()
            if("musicbrainz-test" in knoten_id):
                set_musicbrainz_test()
            zaehler=2
              
        if eintrag.nodeName == "question": 
            id=(eintrag.attributes["id"]).value
            question_text = query = None
            answer=[]
            for knoten in eintrag.childNodes: 
                if knoten.nodeName == "text" or knoten.nodeName == "string": 
                    question_text = _knoten_auslesen(knoten) 
                elif knoten.nodeName == "query": 
                    query=knoten.firstChild.data.strip()
                elif knoten.nodeName=="answers":
                    try:
                        answer_elem_1=[]
                        for knoten_answer in knoten.childNodes:
                            if knoten_answer.nodeName=="answer":
                                answer_elem=[]
                                mehr_als_ein_typ=False
                                eins=zwei=None
                                eins=((knoten_answer.childNodes).item(1)).nodeName
                                if((knoten_answer.childNodes).item(3)):
                                    zwei=((knoten_answer.childNodes).item(3)).nodeName
                                else:
                                    zwei= None
                                if(eins==zwei or zwei==None):
                                    mehr_als_ein_typ=False
                                    choosen_tag[id]=((knoten_answer.childNodes).item(1)).nodeName
                                else:
                                    mehr_als_ein_typ=True
                                    #choosen_tag[id]="string"
                                    choosen_tag[id]="uri"
                            
                                n=0    
                                for knoten_answer1 in knoten_answer.childNodes:
                                    if(knoten_answer1.nodeName!="#text"):
                                        n=n+1
                                        if knoten_answer1.nodeName == "string" and mehr_als_ein_typ==False:
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "boolean" and mehr_als_ein_typ==False:
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "number" and mehr_als_ein_typ==False:
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "date" and mehr_als_ein_typ==False:
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == "uri" and mehr_als_ein_typ==False:
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                        if knoten_answer1.nodeName == choosen_tag[id] and mehr_als_ein_typ==True:
                                            try:
                                                answer_elem.append(knoten_answer1.firstChild.data.strip())
                                            except Exception:
                                                answer_elem.append(" ")
                                answer_elem_1.append(answer_elem)
                    except Exception as inst:
                        error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>"+str(type(inst))+"</p><p>"+str(inst.args)+"</p><p>"+str(inst)+"</p><p>"+id+"</p><p>PLEASE CHECK YOUR XML FILE</p></body></html>"
                        outfile=open(filename_out_html,"w")
                       # _ausgabe_(filename_out_html)
                        outfile.write(error)
                        outfile.close()
                        choosen_tag[id]="string"
                        answer_elem_1.append("ERROR IN FILE")
                        
                    answer.append(answer_elem_1)
            d[question_text] = [query,id,answer]
    return d

    


def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    return [dict[key] for key in keys]


def _evluation(loesung, musterloesung,string):
    anzahl_bearbeiteter_fragen=0
    anzahl_korrekter_antworten=0
    anzahl_falscher_antworten=0
    falsche_antworten=[]
    anzahl_bearbeiteter_fragen=len(loesung)
    bewertung_ausgabe={}
    global OutOfScopeQuestions
    for question_text, query_loesung in loesung.iteritems():
        
        
        anzahl_falscher_frageelemente=anzahl_richtiger_frageelemente=0
        R=P=F=0
        answer_loesung1=query_loesung[2]
        answer_loesung=answer_loesung1[0]
        loesung_id=query_loesung[1]
        answer_musterloesung1=musterloesung[loesung_id]
        answer_musterloesung2=answer_musterloesung1[2]
        answer_musterloesung=answer_musterloesung2[0]
        
        #here muss das rein mit dem Abfragen nach OutOfScope
        if(len(answer_loesung)==0 and loesung_id not in OutOfScopeQuestions):
            
            # anzahl_falscher_fragen+=1
            anzahl_falscher_antworten+=1
            falsche_antworten.append(loesung_id)
            R=P=F=0
            bewertung_ausgabe[loesung_id]=[question_text,str(R),str(P),str(F)]
                
        elif (loesung_id in OutOfScopeQuestions):
            if(len(answer_loesung)==0):
                R=P=F=1.0
                anzahl_korrekter_antworten+=1
                bewertung_ausgabe[loesung_id]=[question_text,str(R),str(P),str(F)]
            else:
                R=P=F=0
                anzahl_falscher_antworten+=1
                falsche_antworten.append(loesung_id)
                bewertung_ausgabe[loesung_id]=[question_text,str(R),str(P),str(F)]
            
            
            
        else:
            if(len(answer_musterloesung)>len(answer_loesung)):
                anzahl_falscher_antworten+=1
                anzahl_falscher_frageelemente+=(len(answer_musterloesung)-len(answer_loesung))
                falsche_antworten.append(loesung_id)
                for i in range(0,len(answer_loesung)):
                    for j in range(0,len(answer_musterloesung)):
                        if(answer_loesung[i]==answer_musterloesung[j]):
                            anzahl_richtiger_frageelemente+=1
                            break
                if(anzahl_richtiger_frageelemente==0):
                    R=F=P=0
                else:
                    R1=Decimal(anzahl_richtiger_frageelemente)
                    R2=Decimal(len(answer_musterloesung))
                    R=round((R1/R2),5)
                    P1=R1
                    P2=Decimal(len(answer_loesung))
                    P=round((P1/P2),5)
                    F=round(((2*P*R)/(R+P)),5)
                bewertung_ausgabe[loesung_id]=[question_text,str(R),str(P),str(F)]
                
                
            else:
                for i in range(0,len(answer_loesung)):
                    for j in range(0,len(answer_musterloesung)):
                        if(answer_loesung[i]==answer_musterloesung[j]):
                            anzahl_richtiger_frageelemente+=1
                            break
                if(anzahl_richtiger_frageelemente==len(answer_loesung)):
                    anzahl_korrekter_antworten+=1
                else:
                    anzahl_falscher_antworten+=1
                    falsche_antworten.append(loesung_id)
                if(anzahl_richtiger_frageelemente==0):
                    R=F=P=0
                else:
                    R1=Decimal(anzahl_richtiger_frageelemente)
                    R2=Decimal(len(answer_musterloesung))
                    R=round((R1/R2),5)
                    P1=R1
                    P2=Decimal(len(answer_loesung))
                    P=round((P1/P2),5)
                    F=round(((2*P*R)/(R+P)),5)

                bewertung_ausgabe[loesung_id]=[question_text,str(R),str(P),str(F)]     
                
                
    if(anzahl_korrekter_antworten==0):
        fmeasure=recall=precision=0
    else:
        wert1=Decimal(anzahl_korrekter_antworten)
        wert2=Decimal(anzahl_bearbeiteter_fragen)
        recall=round(((wert1/len(musterloesung))),5)
        precision=round(((wert1/wert2)),5)
        fmeasure=round(((2*recall*precision)/(recall+precision)),5)
    recall=str(recall)                 
    precision=str(precision)
    fmeasure=str(fmeasure)
    anzahl_bearbeiteter_fragen=str(anzahl_bearbeiteter_fragen)
    anzahl_korrekter_antworten=str(anzahl_korrekter_antworten)
    anzahl_falscher_antworten=str(anzahl_falscher_antworten)

    global_precision=0.0
    global_recall=0.0
    global_fmeasure=0.0
    global_zaehler=0;
    for id,answer in bewertung_ausgabe.iteritems():
        global_zaehler=global_zaehler+1;
        #here mueste ich dann alle werte aufsummieren, also p,r,f und dann durch die anzahl teilen.
        string_bla=id+";"+answer[0]+";"+answer[2]+";"+answer[1]+";"+answer[3]+"\n"       
        string+=string_bla
        global_precision=global_precision+float(answer[2])
        global_recall=global_recall+float(answer[1])
        global_fmeasure=global_fmeasure+float(answer[3])
        
    global_precision=str(global_precision/global_zaehler)
    global_recall=str(global_recall/global_zaehler)
    global_fmeasure=str(global_fmeasure/global_zaehler)

    global MLTrain
    if(musicbrainz==True and MLTrain==False):
        #write_txt(anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,fmeasure,precision,recall,bewertung_ausgabe,falsche_antworten)
        write_html(string,anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,global_fmeasure,global_precision,global_recall,bewertung_ausgabe,falsche_antworten)
    if(dbpedia==True and MLTrain==False):
        #write_txt(anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,fmeasure,precision,recall,bewertung_ausgabe,falsche_antworten)
        write_html(string,anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,global_fmeasure,global_precision,global_recall,bewertung_ausgabe,falsche_antworten)
        
    if((dbpedia_test==True or musicbrainz_test==True) and MLTrain==True):
        write_txt(anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,global_fmeasure,global_precision,global_recall,bewertung_ausgabe,falsche_antworten)
    if((dbpedia_test==True or musicbrainz_test==True) and MLTrain==False):
        write_html(string,anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,global_fmeasure,global_precision,global_recall,bewertung_ausgabe,falsche_antworten)


def write_txt(anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,fmeasure,precision,recall,bewertung_ausgabe,falsche_antworten):
    
    #global system_name, configuration
    bla=""
    bla=system_name+";"+configuration+"\n"
    globale_uebersicht_txt= anzahl_bearbeiteter_fragen+";"+anzahl_korrekter_antworten+";"+anzahl_falscher_antworten+";"+recall+";"+precision+";"+fmeasure+"\n"
    string=""
    for id,answer in bewertung_ausgabe.iteritems():
        string_bla=id+";"+answer[0]+";"+answer[2]+";"+answer[1]+";"+answer[3]+"\n"       
        string+=string_bla                                                                                            

    outfile=open(filename_out_txt,"w")
    outfile.write(bla+globale_uebersicht_txt+string)
    outfile.close()
    _ausgabe_(filename_out_txt)
    
    
    
def write_html(string,anzahl_falscher_antworten,anzahl_korrekter_antworten,anzahl_bearbeiteter_fragen,fmeasure,precision,recall,bewertung_ausgabe,falsche_antworten):
    tabelle3="<table class=\"eval\" border=\"1\"><tr><th>Failed questions (IDs)</th></tr>"
    string_question ="<tr>"
    for i in range(0,len(falsche_antworten)):
        string_question+="<td>"+str(falsche_antworten[i])+"</td></tr>"
    end_tabelle3="</table>"
    
    test= "<!doctype html> <html> <head> <title>Evaluation of "+string+"</title></head> <body> <p>Evaluation</p><p>Skript Version 6.0</p>"
    space="<p></p><p></p><p></p><p></p><p></p>"
    tabelle1="<table class=\"eval\" border=\"1\"><tr><th>ID</th><th>Question</th><th>Precision</th><th>Recall</th><th>F-Measure</th></tr>"
    tabelle2="<table class=\"eval\" border=\"1\"><tr><th>Number of constructed Querries</th><th>Number of correct Answers</th><th>Number of wrong Answers</th><th>Global Recall</th><th>Global Precision</th><th>Global F-Measure</th></tr>"
    inhalt_tabelle2="<tr><td>"+anzahl_bearbeiteter_fragen+"</td><td>"+anzahl_korrekter_antworten+"</td><td>"+anzahl_falscher_antworten+"</td><td>"+recall+"</td><td>"+precision+"</td><td>"+fmeasure+"</td></tr>" 
    end_tabelle2="</table>"
    end_tabelle1="</table>"
    
    ende="</body> </html>"
    string=""
    for id,answer in bewertung_ausgabe.iteritems():
        string_bla="<tr><td>"+id+"</td><td>"+answer[0]+"</td><td>"+answer[2]+"</td><td>"+answer[1]+"</td><td>"+answer[3]+"</td></tr>"       
        string+=string_bla                                                                                            

    outfile=open(filename_out_html,"w")
    outfile.write(test+space+tabelle2+inhalt_tabelle2+end_tabelle2+space+tabelle1+string+end_tabelle1+space+tabelle3+string_question+end_tabelle3+ende)
    outfile.close()
    _ausgabe_(filename_out_html)

def main():
    global dbpedia,musicbrainz, system_time, MLTrain
    
    
    system_time = datetime.datetime.now()
    set_filename_out(system_time)
    set_filename_txt_out(system_time)
    #print system_time
    #print filename_out_html
    set_Pfade_Musterloesung();
    
    import urllib
    dateiname=sys.argv[1]
    MLTrain_bla=sys.argv[2]
    if "0" in MLTrain_bla :
        MLTrain=False
    else:
        MLTrain=True
    #print MLTrain
    if (len(sys.argv)>=5):
        set_system_name(sys.argv[3])
        set_configuration(sys.argv[4])
    else:
        set_system_name("None")
        set_configuration("None")     
    
    loesung=None
    try:
        loesung=lade_baum(dateiname)
    except Exception as inst:
        error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>"+str(type(inst))+"</p><p>"+str(inst.args)+"</p><p>"+str(inst)+"</p><p>PLEASE CHECK YOUR XML FILE</p></body></html>"
        outfile=open(filename_out_html,"w")
        outfile.write(error)
        outfile.close()
        _ausgabe_(filename_out_html) 
    
    enable=True
    
    if((musicbrainz==True or dbpedia==True) and MLTrain==1):
        error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>You need to upload a file with dataset id 'dbpedia-test' or 'musicbrainz-test' for testing.</p></body></html>"
        write_error(error)
        enable=False
    if((musicbrainz_test==True or dbpedia_test==True) and MLTrain==0):
        error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>It is not allowed to upload a test file while choosing the option 'training'. Please make sure to choose a file with dataset id 'dbpedia-train' or 'musicbrainz-train' for training.</p></body></html>"
        write_error(error)
        enable=False
        
    if(musicbrainz==True and enable==True):
        try:
           # if(urllib.urlopen(Pfad_Musterloesung-Musicbrainz-train)):
           #     musterloesung=lade_musterloesung(urllib.urlopen(Pfad_Musterloesung-Musicbrainz-train))
           # else:
            musterloesung=lade_musterloesung(urllib.urlopen(Pfad_Musterloesung_Musicbrainz_train))
        except Exception as inst:
            error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>"+str(type(inst))+"</p><p>"+str(inst.args)+"</p><p>"+str(inst)+"</p></body></html>"
            write_error(error)
        else:
            _evluation(loesung, musterloesung,"musicbrainz")


        
    if(dbpedia==True and enable==True):
        try:
            musterloesung=lade_musterloesung(urllib.urlopen(Pfad_Musterloesung_Dbpedia_train))
        except Exception as inst:
            error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>"+str(type(inst))+"</p><p>"+str(inst.args)+"</p><p>"+str(inst)+"</p></body></html>"
            write_error(error)
        else:
            _evluation(loesung, musterloesung,"dbpedia")
            
    if(dbpedia_test==True and enable==True):
        try:
            musterloesung=lade_musterloesung(urllib.urlopen(Pfad_Musterloesung_Dbpedia_test))
        except Exception as inst:
            error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>"+str(type(inst))+"</p><p>"+str(inst.args)+"</p><p>"+str(inst)+"</p></body></html>"
            write_error(error)
        else:
            _evluation(loesung, musterloesung,"dbpedia_test")

    if(musicbrainz_test==True and enable==True):
        try:
            musterloesung=lade_musterloesung(urllib.urlopen(Pfad_Musterloesung_Musicbrainz_test))
        except Exception as inst:
            error= "<!doctype html> <html> <head> <title>ERROR</title></head> <body> <p>"+str(type(inst))+"</p><p>"+str(inst.args)+"</p><p>"+str(inst)+"</p></body></html>"
            write_error(error)
        else:
            _evluation(loesung, musterloesung,"musicbrainz_test")



def write_error(error):
    global filename_out_html
    outfile=open(filename_out_html,"w")
    outfile.write(error)
    outfile.close()
    _ausgabe_(filename_out_html)

if __name__ == "__main__":
    main()
    
