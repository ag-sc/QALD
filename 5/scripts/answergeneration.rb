require 'nokogiri'
require 'sparql/client'
require 'htmlentities'


endpoint = SPARQL::Client.new("http://dbpedia.org/sparql/")
html     = HTMLEntities.new

input    = ARGV[0]
output   = input + ".answers"

doc = Nokogiri::XML(File.read(input))

doc.xpath("/dataset/question[not(answers)]").each do |question|

  id = question["id"]

  begin
    query_node   = question.at_xpath("query")
    query_text   = query_node.text
    
    answers      = []
    answers_node = Nokogiri::XML::Node.new("answers",doc)

    if query_text.strip != "OUT OF SCOPE"

       result = endpoint.query(query_text)

       if result.inspect == "true" or result.inspect == "false"
          answers << result.inspect
       elsif not result.empty? and not result.nil?
          result.each { |r| r.each_value { |value| answers << value }}
       end

       answers.each do |answer|
               answer_node   = Nokogiri::XML::Node.new("answer",doc)
               answer_string = "<![CDATA[" + html.decode(answer) + "]]>"
               # answer_node.content = answer # note that answer gets HTML encoded here
               answer_node.send(:native_content=, answer_string)
               answers_node << answer_node
       end
    end 

    question << answers_node

    sleep(1) # needed for friendship with the DBpedia endpoint
  
  rescue Exception=>e

    puts "Oops, something went wrong with question #{id}..."
    puts e
  end

end

File.write(output,doc)
