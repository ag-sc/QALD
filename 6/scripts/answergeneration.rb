require 'sparql/client'
require 'json'


endpoint = SPARQL::Client.new("http://dbpedia.org/sparql/")

input    = ARGV[0]
output   = input + ".answers"

doc = JSON.parse(File.read(input))

doc["questions"].each do |question|

  answers = []

  if question["query"].key?("sparql")

     sparql = question["query"]["sparql"]

     begin
       results = endpoint.query(sparql)

       if results.inspect == "true"
          answers << { "head" => {}, "boolean" => true }
       elsif results.inspect == "false"
          answers << { "head" => {}, "boolean" => false }
       else
         results.each do |result|
            result.each_binding do |var,value|
              if value.uri?
                 answers << { "head" => { "vars" => [ var.inspect.gsub(":","") ] }, "bindings" => [ { var.inspect.gsub(":","") => { "type" => "uri", "value" => value.to_rdf } } ] }
              elsif value.literal?
                 answers << { "head" => { "vars" => [ var.inspect.gsub(":","") ] }, "bindings" => [ { var.inspect.gsub(":","") => { "type" => "literal", "value" => value.to_rdf } } ] }
              end
            end
          end
        end

    rescue Exception=>e
        puts "Oops, something went wrong with question " + question["id"] + "..."
        puts e
    end

  end

  question["answers"] = answers

  sleep(1) # needed for friendship with the DBpedia endpoint

end

File.write(output,JSON.pretty_generate(doc))
