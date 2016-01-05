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

      # answers

      # q["answers"] = []
      #
      # answers      = []
      # answer_nodes = []
      # answers_node = question.at_xpath("answers")
      #
      # if not answers_node.nil?
      #    answer_nodes = answers_node.children
      # end
      # if not answer_nodes.nil?
      #    answer_nodes.each do |node|
      #       if node.text.gsub("\n","").strip != ""
      #          answers << node.text.strip
      #       end
      #    end
      # end
      #
      # answers.each { |a| q["answers"] << { "head" => { "vars" => [ "uri" ] }, "bindings" => [ "uri" => { "type" => "uri", "value" => a } ] } }

      # add question to JSON output

      outputJSON["questions"] << q

end

File.write(inputXML.sub(".xml",".json"),JSON.pretty_generate(outputJSON))
