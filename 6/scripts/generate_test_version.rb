require 'json'


def del(question,attribute)
    if question.key?(attribute)
       question.delete(attribute)
    end
end


input  = ARGV[0]
output = input + ".questions"

doc = JSON.parse(File.read(input))

doc["questions"].each do |question|

  del(question,"answertype")
  del(question,"aggregation")
  del(question,"onlydbo")
  del(question,"hybrid")
  del(question,"query")
  del(question,"answers")
end

File.write(output,JSON.pretty_generate(doc))
