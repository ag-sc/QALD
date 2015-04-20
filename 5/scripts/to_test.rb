require 'nokogiri'

input  = ARGV[0]
output = input + ".questions"

doc = Nokogiri::XML(File.read(input))

doc.xpath("/dataset/question").each do |question|

    question.search(".//query").remove
    question.search(".//answers").remove
    question.search(".//pseudoquery").remove

end

File.write(output,doc)
