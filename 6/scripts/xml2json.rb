require 'nokogiri'
require 'json'
require 'mustache'
require 'uri'

#################################################################

inputXML = ARGV[0]

#################################################################

def rewrite(sparql)

    prefixes = { "dbo"  => "http://dbpedia.org/ontology/", "dbp"  => "http://dbpedia.org/property/", "res"  => "http://dbpedia.org/resource/", "rdf"  => "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdfs" => "http://www.w3.org/2000/01/rdf-schema#", "yago" => "http://dbpedia.org/class/yago/" }

    sparql.gsub!(/.*((SELECT|ASK)\s)/,'\1')

    prefixes.each { |short,long| sparql.gsub!(Regexp.new(short+':([^\s]+)\s'),'<'+long+'\1> ') }

    sparql.gsub!("  "," ")
    sparql.gsub!("  "," ")
    sparql.gsub!("  "," ")

    return sparql
end

def contains_aggregation?(sparql)

    ["sum","count","filter"].any? { |s| sparql.include? s }
end

#################################################################

outputJSON = { "dataset" => {}, "questions" => [] }


doc = Nokogiri::XML(File.read(inputXML))

doc.xpath("/dataset").each do |dataset|
    outputJSON["dataset"]["id"] = dataset["id"]
end

doc.xpath("/dataset/question").each do |question|

      q = {}

      # question attributes (part 1)

      q["id"]          = question["id"]
      if not question["onlydbo"].nil?
         q["onlydbo"]  = question["onlydbo"]
      end
      if not question["hybrid"].nil?
         q["hybrid"]   = question["hybrid"]
      end

      # strings and keywords

      q["question"] = []

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
        q["question"] << b
      end

      # query

      q["query"] = {}

      question.xpath("query").each do |query|
        if query.text !~ /.*OUT OF SCOPE.*/
           q["query"]["sparql"] = rewrite(query.text.gsub("\n"," "))
        end
      end
      question.xpath("pseudoquery").each do |query|
        q["query"]["pseudo"] = query.text.gsub("\n"," ")
      end

      # question attributes (part 2)

      if not question["aggregation"].nil?
         q["aggregation"] = question["aggregation"]
      else
         if contains_aggregation? q["query"]["sparql"]
             q["aggregation"] = true
         else
             q["aggregation"] = false
         end
      end

      if not question["answertype"].nil?
         q["answertype"] = question["answertype"]
      # else
      #    answertype = nil
      #    answers_node = question.at_xpath("answers")
      #    if not answers_node.nil?
      #       answer_nodes = answers_node.children
      #    end
      #    if not answer_nodes.nil?
      #       answer_nodes.each do |node|
      #          if not node["answerType"].nil?
      #             answertype = node["answerType"]
      #             break
      #          end
      #       end
      #    end
      end
      # if not answertype.nil?
      #    q["answertype"] = answertype
      # end

      # add question to JSON output

      outputJSON["questions"] << q

end

File.write(inputXML.sub(".xml",".json"),JSON.pretty_generate(outputJSON))
