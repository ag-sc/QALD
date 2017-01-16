# QALD-7
Last update: 2017-01-07

For parsing the json files you find a full class structure and parser at:
https://github.com/AKSW/NLIWOD/tree/master/qa.commons/src/main/java/org/aksw/qa/commons/load/json


## QALD-7-train-multilingual dataset
The qald7-train-multilingual dataset was created using the multilingual questions from QALD3-to QALD-6(QALD-1 and QALD-2 questions are not multilingual). However, there was some cleaning necessary:
	
1. Languages
	The natural language question had to be present in at least six languages.
2. Keywords
	For all languages a question is present, if there is at least one keyword.
3. Answertype
	Had to be present.
4. Sparql
	Had to be present and parsable. 
	When dbpedia.org/sparql threw an error on a question, it was disqualified.
5. OnlyDBO-Flag
	Was autocorrected in case it was wrong. 
	OnlyDBO-flag was set to true when the SPARQL query only contains "rdf","rdfs", "http://dbpedia.org/ontology/" or	http://dbpedia.org/resource/ as prefix, otherwise false.
6. Answers
	The answerset was not allowed to be empty. Furthermore, the answerset stored in a question had to be identical with 
	the answerset obtained from dbpedia.org (dbpedia.org version:2016-04, date: 09.01.2017, dd.mm.yyyy)
7. Duplicates 
	Duplicates were identified by the hash of the English natural language question, and removed. If more than one duplicate of a question was present, the copy with the least errors was chosen for further handling.
		
You can find the corresponding code at:
https://github.com/AKSW/NLIWOD/blob/master/qa.commons/src/main/java/org/aksw/qa/commons/qald/Qald7CreationTool.java

Make sure to change the paths in the main method.

By running the creator, there will also be a file report created for all the disqualified questions.
You can find one for the latest run here:
https://github.com/AKSW/NLIWOD/blob/master/qa.commons/resources/qald/BadQuestionsfileReport.txt

The last line of the file report can be paticularly interesting:
"Unique Questions total in all Datasets: 520 Faulty: 305 beforehand removed duplicates: 617"

Which leaves uns with 520-305 = 215 good questions.

Note that the error with by far the highest occurrence is difference in answer sets. 

All possible error flags are defined here:
https://github.com/AKSW/NLIWOD/blob/master/qa.commons/src/main/java/org/aksw/qa/commons/qald/Fail.java

## QALD-7-train-hybrid dataset
The qald7-train-hybrid dataset was created using the hybrid questions from QALD4 to QALD6.
Duplicates were identified by hash of english question string, and removed.

## QALD-7-train-largescale dataset
The qald7-train-largescale dataset was created by replacing the QALD1 to QALD5 question's instance data, mostly but not limited to named entities, by another random instance data of the same DBpedia class. The instance data was replaced in both the question and the query. Queries that did not give a proper result were removed.

## QALD-7-train-multilingual-wikidata dataset

The qald-7-train-en-wikidata dataset was created based on the qald-6-test-multilingual dataset from QALD-6. We took only the English questions and gold standard queries created for DBpedia and formulated corresponding queries to answer these questions from Wikidata. Due to different schema and data structure of Wikidata, some questions could not be answered using Wikidata. We replaced these questions with the ones taken from qald-6-train-multilingual.
The gold standard answers were generated using the Wikidata dumps from 09-01-2017 (https://dumps.wikimedia.org/wikidatawiki/entities/20170109/).

