require 'sparql/client'
require 'json'


#endpoint = SPARQL::Client.new("http://cubeqa.aksw.org/sparql")
endpoint = SPARQL::Client.new("http://dbpedia.org/sparql/")

input    = ARGV[0]
output   = input + ".answers"

doc = JSON.parse(File.read(input))

doc["questions"].each do |question|

  answers = []

  if question["query"].key?("sparql")

     sparql = question["query"]["sparql"]

     begin
       results = endpoint.query(sparql,{ "Accept" => "application/sparql-results+json" })

       if results.inspect == "true"
          answers << { "head" => {}, "boolean" => true }
       elsif results.inspect == "false"
          answers << { "head" => {}, "boolean" => false }
       else
         r = { "head" => { "vars" => [] }, "results" => { "bindings" => [] }}
         results.each do |result|
            b = {}
            result.each_binding do |var,value|
              if not r["head"]["vars"].include? var then r["head"]["vars"] << var end
              if value.uri?
                 b[var.inspect.gsub(":","")] = { "type" => "uri", "value" => value.to_rdf }
              elsif value.literal?
                 b[var.inspect.gsub(":","")] = { "type" => "literal", "value" => value.to_rdf }
              end
            end
            r["results"]["bindings"] << b
          end
          answers << r
        end

    rescue Exception=>e
        puts "Oops, something went wrong with question " + question["id"].to_s + "..."
        puts e
    end

  end

  question["answers"] = answers

  sleep(1) # needed for friendship with the DBpedia endpoint

end

File.write(output,JSON.pretty_generate(doc))
