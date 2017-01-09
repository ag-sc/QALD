9. Jan 2017

For parsing the jsons you find a full class structure and parser at:
https://github.com/AKSW/NLIWOD/tree/dev/qa.commons/src/main/java/org/aksw/qa/commons/load/json

==Qald7-train-hybrid dataset==

	The qald7-train-hybrid dataset was created using the hybrid questions from QALD4 to QALD6.
	Duplicates were identified by hash of english question string, and removed.

==Qald7-train-multilingual dataset==
	
	The qald7-train-multilingual dataset was created using the multilingual questions from QALD3
	to QALD6(QALD1 and QALD2 questions are not multilingual)
	However, there was some cleaning necessary:
	
	1. Languages
		The natural language question had to be present in at least six languages.
	2. Keywords
		For all languages a question is present, there had to be at least one keyword.
    3. Answertype
		Had to be present.
	4. Sparql
		Had to be present and parseable. 
		When dbpedia.org threw an error on a question, it was disqualified.
	5. OnlyDBO-Flag
		Was autocorrected when wrong. 
		OnlyDBO-flag was set to true when sparql query only contains "rdf","rdfs",
		"http://dbpedia.org/ontology/" or
		http://dbpedia.org/resource/ as prefix, otherwise false.
	6. Answers
		The answerset was not allowed to be empty.
		Furthermore, the answerset stored in a question had to be identical with 
		the answerset obtained from dbpedia.org
		(dbpedia.org version:2016-04, date: 09.01.2017, dd.mm.yyyy)
	7. Duplicates 
		Duplicates were identified by the hash of the english natural language question, and removed.
		When more than one duplicate of a question was present, the copy with the least errors was chosen
		for further handling.
		
	You can find the corresponding code at:
	https://github.com/AKSW/NLIWOD/blob/dev/qa.commons/src/main/java/org/aksw/qa/commons/qald/Qald7CreationTool.java
	
	Make sure to change the paths in the main method.
	
	By running the creator, there will also be a file report created for all the disqualified questions.
	You can find one for the latest run here:
	https://github.com/AKSW/NLIWOD/blob/dev/qa.commons/resources/qald/BadQuestionsfileReport.txt
	
	The last line of the file report can be paticularly interesting:
	"Unique Questions total in all Datasets: 520 Faulty: 312 beforehand removed duplicates: 617"
	
	Which leaves uns with 520-312=208 good questions.

	Note that the error with by far the highest occurrence is difference in answer sets. 
	 
	All possible error flags are defined here:
	https://github.com/AKSW/NLIWOD/blob/dev/qa.commons/src/main/java/org/aksw/qa/commons/qald/Fail.java
	 
	
	
		
	
		
		