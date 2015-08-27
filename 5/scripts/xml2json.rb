require 'nokogiri'
require 'json'
require 'mustache'
require 'uri'

#################################################################

inputXML = ARGV[0]

#################################################################

outputJSON = { "dataset" => {}, "questions" => [] }


doc = Nokogiri::XML(File.read(inputXML))

doc.xpath("/dataset").each do |dataset| 
    outputJSON["dataset"]["id"] = dataset["id"]
end

doc.xpath("/dataset/question").each do |question|

      q = {}

      # question attributes

      q["id"]          = question["id"]
      q["answertype"]  = question["answertype"]
      q["aggregation"] = question["aggregation"]
      q["onlydbo"]     = question["onlydbo"] 
      if question["hybrid"].nil?
         q["hybrid"]   = "false"
      else 
         q["hybrid"]   = question["hybrid"]
      end      

      # strings and keywords

      q["body"] = []

      strings   = {}
      keywords  = {}

      question.xpath("string").each do |s| 
        strings[s["lang"]] = s.text
      end
      question.xpath("keywords").each do |k|
        keywords[k["lang"]] = k.text
      end 

      strings.each do |l,s|
        b = { "language" => l, "string" => s } 
        not keywords.key?(l) ? b["keywords"] = keywords[l] : b
        q["body"] << b
      end

      # query 

      question.xpath("query").each do |query| 
        q["query"] = query.text.gsub("\n","").squeeze
      end

      # answers 

      q["answers"] = []

      answers      = []
      answer_nodes = []
      answers_node = question.at_xpath("answers")

      if not answers_node.nil?
         answer_nodes = answers_node.children
      end
      if not answer_nodes.nil?
         answer_nodes.each do |node| 
            if node.text.gsub("\n","").strip != ""
               answers << node.text.strip
            end 
         end
      end

      answers.each { |a| q["answers"] << { "string" => a } }

      # add question to JSON output

      outputJSON["questions"] << q
      
end

File.write(inputXML.sub(".xml",".json"),JSON.pretty_generate(outputJSON))
