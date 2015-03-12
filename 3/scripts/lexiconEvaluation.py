#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/cunger/local/lib/python2.7/site-packages/isodate-0.4.9-py2.7.egg")
sys.path.append("/home/cunger/local/lib/python2.7/site-packages/SPARQLWrapper-1.5.2-py2.7.egg")
sys.path.append("/home/cunger/local/lib/python2.7/site-packages/rdflib-3.2.3-py2.7.egg")
sys.path.append("/home/cunger/local/lib/python2.7/site-packages/pystache-0.5.3-py2.7.egg")

from aux.rdfEngine import *
import rdflib
import glob
from SPARQLWrapper import SPARQLWrapper, JSON
import datetime
import Entry

endpoint = "http://vtentacle.techfak.uni-bielefeld.de:443/sparql/"
path_goldstandard_train = "/home/cunger/public_html/qald/3/Task2/dbpedia-train-lexicon-en.ttl"
path_goldstandard_test  = "/home/cunger/public_html/qald/3/Task2/dbpedia-test-lexicon-en.ttl"
Laenge_Goldstandard = 40



#in commandline give path to lexicon and goldstandard lexicon


def MatchArrays(array1 ,array2):
    for user_lex in array1:
        for gold in array2:
            if user_lex == gold:
                return True
            
    #raw_input("no entry found...")
    return False
            

def createArrayEntries(path):
    #print"Path: "+str(path)
    graph = loadGraph(path)
    lemon = Namespace("http://www.monnet-project.eu/lemon#")
    lexinfo = Namespace("http://www.lexinfo.net/ontology/2.0/lexinfo#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    isocat = Namespace("http://www.isocat.org/datcat/")
    #getProperties(graph)

    result_array = []
        
#   for lexicon in getResultsFrom(graph,'Task2/sparql/lexicon.sparql'):
    for _,_,o in graph.triples((None,lemon.entry ,None)):
            canonicalForm = None
            reference = []
            sense_arguments = []
            synBehavior_arguments = []
            frame = None
            partOfSpeech = None
            for _,_,o1 in graph.triples((o,lemon.sense ,None)):
                for _,_,o2 in graph.triples((o1,lemon.reference ,None)):
                    reference.append(str(o2))

                for _,_,o2 in graph.triples((o1,lemon.subsense ,None)):
                    for _,_,o3 in graph.triples((o2,lemon.reference ,None)):
                        if str(o3) not in reference:
                            reference.append(str(o3))
                for _,B,o2 in graph.triples((o1,None ,None)):
                    if "reference" not in B:
                        
                        if "subj" in B:
                            sense_arguments.append(["subject",str(o2)])
                        else:
                            sense_arguments.append(["object",str(o2)])
            
            for _,_,o1 in graph.triples((o,lemon.synBehavior,None)):
                for _,B,o2 in graph.triples((o1,rdf.type , None)):
                    frame = o2
                for _,B,o2 in graph.triples((o1,None , None)):
                    if "#type" not in B:
                        if lexinfo in B:
                            synBehavior_arguments.append([str(B.replace(lexinfo,"")),str(o2)])
                        if isocat in B:
                            synBehavior_arguments.append([str(B.replace(isocat,"")),str(o2)])
            
            for _,_,o1 in graph.triples((o,lemon.canonicalForm ,None)):
                for _,_,o2 in graph.triples((o1,lemon.writtenRep ,None)):
                    canonicalForm = o2
                    
            for _,_,o1 in graph.triples((o,lexinfo.partOfSpeech ,None)):
                tmp = str(o1)
                tmp = tmp.replace("http://www.lexinfo.net/ontology/2.0/lexinfo#","")
                partOfSpeech = tmp.lower()
                
            
                    
            if len(reference) != 0 and canonicalForm != None:
                #print "reference: "+reference
                entry = Entry.Entry(canonicalForm.replace(" ","").lower(), str(canonicalForm), reference, str(frame), None, str(partOfSpeech),sense_arguments, synBehavior_arguments)
                result_array.append(entry)
            
    return result_array








#####################################MAIN#########################################    
##################################################################################  
################################################################################## 
##################################################################################  

def main():
    path_user_lexicon = ""
    
    Train_evaluation = True
    
    results_each_uri = []
    
    
    if len(sys.argv)>2:
        path_user_lexicon = sys.argv[1]
        if str(sys.argv[2]) == "0":
            Train_evaluation = True
        elif str(sys.argv[2]) == "1":
            Train_evaluation = False
    else:
        exit(1)
       
    if Train_evaluation: path_goldstandard = path_goldstandard_train
    else:                path_goldstandard = path_goldstandard_test 
      
    user_lexicon_global = createArrayEntries(path_user_lexicon)
    hm_of_uris = {}
    
    for entry in user_lexicon_global:
        tmp = entry.getSense()
        for x in tmp:
            hm_of_uris[x] = ""
        
    ################## First Recall/Precision over given lexicon entries ##########################
    
    global_Recall = 0
    global_Precision = 0
    global_FMeasure = 0
    global_Accuracy = 0

    
    
    for uri_to_compare_with in hm_of_uris:

        listOfPathes = []
        lexicon_entries_gold = []
        user_lexicon = []
        
        listOfPathes.extend(glob.glob(path_goldstandard))
        
        
        #create gold lexicon only containing entries for uri_to_compare_with over all given pathes
        for path in listOfPathes:
            #print "Path: "+path
            for item in createArrayEntries(path):
                
                #check here, if already the same entry is in the goldstandard...
                #if there is the same, do not add!
                
                if uri_to_compare_with in item.getSense():
                    adding = True
                    for x in lexicon_entries_gold:
                        if item.getCanonicalForm().lower() == x.getCanonicalForm().lower() and MatchArrays(item.getSense(),x.getSense()) == True and item.getPartOfSpeech() == x.getPartOfSpeech():
                            adding = False
                            break
                    
                    if adding == True:
                        lexicon_entries_gold.append(item)
                        
                        
                        
        #create user lexicon only containing entries for uri_to_compare_with
        for user_entry in user_lexicon_global:  
            if uri_to_compare_with in user_entry.getSense():
                adding = True
                for x in user_lexicon:
                    if user_entry.getCanonicalForm().lower() == x.getCanonicalForm().lower() and MatchArrays(user_entry.getSense(),x.getSense()) == True and user_entry.getPartOfSpeech() == x.getPartOfSpeech():
                        adding = False
                        break
                
                if adding == True:
                    user_lexicon.append(user_entry)
                    
                    
        
        
        numberOfEntries_lexicon = float(len(user_lexicon))
        numberOfEntries_goldstandard = float(len(lexicon_entries_gold))
        
        numberOfCorrectEntries_lexicon = 0
        Recall = 0
        Precision = 0
        FMeasure = 0
        Accuracy = 0
        
            
        tmp_hm = {}
        
        #Only sense, canonical and partofSpeech form together can really identify an entry
        for user_lex in user_lexicon:
            for gold in lexicon_entries_gold:
                if user_lex.getCanonicalForm().lower() == gold.getCanonicalForm().lower() and tmp_hm.has_key(user_lex.getCanonicalForm()) == False and MatchArrays(user_lex.getSense(),gold.getSense()) == True and user_lex.getPartOfSpeech() == gold.getPartOfSpeech():
        
                    tmp_hm[user_lex.getCanonicalForm()] = ""
                    numberOfCorrectEntries_lexicon+=1
                
        
                
        if numberOfCorrectEntries_lexicon == 0:
            Recall = 0
            Precision = 0
            FMeasure = 0
        else:
            
            Recall = round((numberOfCorrectEntries_lexicon/numberOfEntries_goldstandard),5)
            Precision = round((numberOfCorrectEntries_lexicon/numberOfEntries_lexicon),5)
            FMeasure = round((2*Recall*Precision)/(Precision+Recall),5)
        
        
        subject_map = {}
        object_map = {}
        subject_map,object_map = return_mapping()
        
        
        
        
        
        
        points = 0
        entries_counter = 0
        for user_lex in user_lexicon:
            for gold in lexicon_entries_gold:
                if user_lex.getCanonicalForm().lower() == gold.getCanonicalForm().lower() and MatchArrays(user_lex.getSense(),gold.getSense()) == True and user_lex.getPartOfSpeech() == gold.getPartOfSpeech():
                    #print str(user_lex.getCanonicalForm())
                    local_points = 0
                    entries_counter += 1
                    # For classes check only the Frame!
                    if askClassProperty(user_lex.getSense()[0]) == True and len(user_lex.getSense())==1:
                        if user_lex.getFrame() == gold.getFrame():
                            local_points += 1
                            
                    else:
                        
                        #einen Punkt fuers korrekte Frame
                        if user_lex.getFrame() == gold.getFrame():
                            local_points +=1
                           
                            
                        #einen Punkt fuer korrekten eigenen Eintrag, d.h. ist das Subject Argument in der sense auch das Subject in synbehaviour? Nur fuer den vom user gegebenen Eintrag
                        if len(user_lex.getSynBehavior_arguments()) == len(user_lex.getSense_arguments()):
                            tmp_points = 0
                            
                            #Abhaengig von den Eintraegen in Gold!!!
                            #########################################
                            #
                            #
                            #
                            # 1 = sub -> obj
                            # 2 = obj -> sub
                            # 3 = sub -> sub
                            # 4 = obj -> obj
                            #
                            #
                            #
                            #########################################
                            fingerprint_user = []
                            fingerprint_gold = []
                            for entry_sense in user_lex.getSense_arguments():
                                for entry_syn in user_lex.getSynBehavior_arguments():
                                    if entry_sense[1] == entry_syn[1]:
                                        if "subject" in entry_sense[0] and entry_syn[0] in object_map:
                                            fingerprint_user.append("1")
                                        if "object" in entry_sense[0] and entry_syn[0] in subject_map:
                                            fingerprint_user.append("2")
                                        if "subject" in entry_sense[0] and entry_syn[0] in subject_map:
                                            fingerprint_user.append("3")
                                        if "object" in entry_sense[0] and entry_syn[0] in object_map:
                                            fingerprint_user.append("4")
                                            
                            for entry_sense in gold.getSense_arguments():
                                for entry_syn in gold.getSynBehavior_arguments():
                                    if entry_sense[1] == entry_syn[1]:
                                        if "subject" in entry_sense[0] and entry_syn[0] in object_map:
                                            fingerprint_gold.append("1")
                                        if "object" in entry_sense[0] and entry_syn[0] in subject_map:
                                            fingerprint_gold.append("2")
                                        if "subject" in entry_sense[0] and entry_syn[0] in subject_map:
                                            fingerprint_gold.append("3")
                                        if "object" in entry_sense[0] and entry_syn[0] in object_map:
                                            fingerprint_gold.append("4")
 
                            
                            
                            if len(fingerprint_user) == len(fingerprint_gold):
                                correct = True
                                for x in fingerprint_gold:
                                    if x not in fingerprint_user:
                                        correct = False
                                if correct == True:
                                    local_points += 1
                                        
                            elif len(fingerprint_user) != len(fingerprint_gold):
                                number_tmp = 0
                                for x in fingerprint_gold:
                                    if x in fingerprint_user:
                                        number_tmp += 1
                                if number_tmp == 0:
                                    local_points += 0
                                else:
                                    local_points += (number_tmp/len(fingerprint_gold))
                          
                                                
                        else:
                            local_points += 0
                           
                                            
                                            
                            
                            
                        #einen Punkt, wenn die Mappings im Synbehaviour von user_lex und gold gleich sind
        
                        if len(user_lex.getSynBehavior_arguments()) == len(gold.getSynBehavior_arguments()):
                            found = 0
                            for syn_1 in user_lex.getSynBehavior_arguments():
                                for syn_2 in gold.getSynBehavior_arguments():
                                    if syn_1[0] == syn_2[0]:
                                        found +=1
                            if found == len(gold.getSynBehavior_arguments()):
                                local_points += 1
                                
                                    
                        else:
                            local_points += 0
                            print local_points
                            
                        #ganz am Ende entweder 0 zurueck geben, oder normieren uber die 3 Punkte
                        if local_points == 0:
                            points += local_points
                          
                        else:
                            local_points = (local_points+0.0)/3
                           
                            
                            
                    points += local_points
     
                    
        if entries_counter >0:
            Accuracy = points/entries_counter
        else:
            Accuracy = 0
        
        
        results_each_uri.append([uri_to_compare_with,Recall,Precision,FMeasure,Accuracy])
        global_Recall += Recall
        global_Precision += Precision
        global_FMeasure += FMeasure
        global_Accuracy += Accuracy


    #write results
    global_Recall = global_Recall/Laenge_Goldstandard
    global_Precision = global_Precision/Laenge_Goldstandard
    global_FMeasure = global_FMeasure/Laenge_Goldstandard
    global_Accuracy = global_Accuracy/Laenge_Goldstandard
    
    #Train_evaluation == True -> HTML-Datei
    #Train_evaluation == False -> TEST-Datei
    
    system_time = datetime.datetime.now()
    filename_out_txt=path_user_lexicon.split('.')[0]+"_out.txt"
    filename_out_html=path_user_lexicon.split('.')[0]+"_out.html"
    #filename_out_html="upload/out"+str(system_time)+".html"

    if Train_evaluation == True:
        #create html
        create_html_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename_out_html)
        print filename_out_html
    
    if Train_evaluation == False:
        #create txt
        create_txt_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename_out_txt)
        print filename_out_txt
    
    
            

def create_html_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename):
    start_table= "<!doctype html> <html> <head> <title>Evaluation</title></head> <body> <p>Evaluation</p>"
    space="<p></p><p></p><p></p><p></p><p></p>"
    tabelle1="<table class=\"eval\" border=\"1\"><tr><th>URI</th><th>Recall</th><th>Precision</th><th>F-Measure</th><th>Accuracy</th></tr>"
    tabelle2="<table class=\"eval\" border=\"1\"><tr><th>Global Recall</th><th>Global Precision</th><th>Global F-Measure</th><th>Global Accuracy</th></tr>"
    inhalt_tabelle2="<tr><td>"+str(global_Recall)+"</td><td>"+str(global_Precision)+"</td><td>"+str(global_FMeasure)+"</td><td>"+str(global_Accuracy)+"</td></tr>" 
    end_tabelle="</table>"
    
    ende="</body> </html>"
    string=""
    
    #results_each_uri.appen([uri_to_compare_with,Recall,Precision,FMeasure,Accuracy])
    
    for uri,recall,precision,fmeasure,accuracy in results_each_uri:
        string_bla="<tr><td>"+uri+"</td><td>"+str(recall)+"</td><td>"+str(precision)+"</td><td>"+str(fmeasure)+"</td><td>"+str(accuracy)+"</td></tr>"       
        string+=string_bla                                                                                            

    outfile=open(filename,"w")
    outfile.write(start_table+space+tabelle2+inhalt_tabelle2+end_tabelle+space+tabelle1+string+end_tabelle+ende)
    outfile.close()



def create_txt_file(global_Recall,global_Precision,global_FMeasure,global_Accuracy,results_each_uri,filename):
    
    globale_uebersicht_txt= "global_Recall: "+str(global_Recall)+"; global_Precision: "+str(global_Precision)+"; global_FMeasure: "+str(global_FMeasure)+"; global_Accuracy: "+str(global_Accuracy)+";\n"
    string=""
    string += "uri;recall;precision;fmeasure;accuracy\n"
    for uri,recall,precision,fmeasure,accuracy in results_each_uri:
        string += uri+";"+str(recall)+";"+str(precision)+";"+str(fmeasure)+";"+str(accuracy)+"\n"                                                                                                  

    outfile=open(filename,"w")
    outfile.write(globale_uebersicht_txt+"\n\n"+string)
    outfile.close()


def return_mapping():
    subject_map = {}
    subject_map["http://www.lexinfo.net/ontology/2.0/lexinfo#subject"]=""
    subject_map["http://www.isocat.org/datcat/DC-2261"]=""
                
    subject_map["subject"]=""
    subject_map["DC-2261"]=""
    subject_map["copulativeArg"]=""
    
    object_map = {}
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#directObject"]=""
    object_map["http://www.isocat.org/datcat/DC-2263"]=""
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#indirectObject"]=""
    object_map["http://www.isocat.org/datcat/DC-1310"]=""
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#prepositionalObject"]=""
    object_map["http://www.isocat.org/datcat/DC-4638"]=""
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#prepositionalAdjunct"]=""
    object_map["http://www.isocat.org/datcat/DC-4622"]=""
    object_map["http://www.isocat.org/datcat/copulativeArg"]=""
    
    object_map["http://www.lexinfo.net/ontology/2.0/lexinfo#possessiveAdjunct"]=""
    object_map["http://www.isocat.org/datcat/DC-4622"]=""
    object_map["possessiveAdjunct"]=""
    object_map["DC-4622"]=""
    
    object_map["directObject"]=""
    object_map["DC-2263"]=""
    object_map["indirectObject"]=""
    object_map["DC-1310"]=""
    object_map["prepositionalObject"]=""
    object_map["DC-4638"]=""
    object_map["prepositionalAdjunct"]=""
    object_map["DC-4622"]=""
    return subject_map, object_map


def create_entryTerm(entry):
    create_entryTerm = entry.split(";")[0]
    create_entryTerm = create_entryTerm.lower()
    create_entryTerm = create_entryTerm.replace("a lemon:lexicalentry","")
    create_entryTerm = create_entryTerm.replace(":","")
    create_entryTerm = create_entryTerm.replace(" ","")
    return create_entryTerm
    
    

 
 
def askClassProperty(uri):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX owl: <http://www.w3.org/2002/07/owl#>  ASK WHERE {<"+uri+"> rdf:type owl:Class}")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print results
    for result in results:
        try:
            string = str(results[result])
            if "False" in string:
                return False
            
            if "True" in string:
                return True
        except:
            pass
    return False


if __name__ == "__main__":
    main()
 
   

    
