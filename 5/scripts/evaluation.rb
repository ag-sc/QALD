Gem.path.push '/home/cunger/.gem/ruby/2.0.0'
require 'nokogiri'
require 'mustache'
require 'uri'

#################################################################

system     = ARGV[2].nil? ? "" : ARGV[2]
config     = ARGV[3].nil? ? "" : ARGV[3]
mode       = ARGV[1] 
input_user = ARGV[0]
input_gold = mode == "test" ? "../data/qald-5_test.xml" : "../data/qald-5_train.xml"
template   = "../scripts/evaluation_result_html.mustache"

#################################################################


def read_answers(file)

    out = { :dbpedia => {}, :hybrid => {} }

    doc = Nokogiri::XML(File.read(file))
    doc.xpath("/dataset/question").each do |question|

      id           = question["id"]
      answers      = []
      answer_nodes = []
      answers_node = question.at_xpath("answers")

      if not answers_node.nil?
         answer_nodes = answers_node.children
      end
      if not answer_nodes.nil?
        answer_nodes.each { |node| answers << normalize(node.text) }
      end

      answers.delete("")

      if question.attr("hybrid") == "true"
         out[:hybrid][id]  = answers 
      else 
         out[:dbpedia][id] = answers
      end
    end

    return out
end

def normalize(answer) 

    if answer =~ /\A\d+\z/ 
       return answer + ".0"
    else
       return URI.unescape(answer.strip)
    end
end

def evaluate_answers(answers_user,answers_gold)

    results = []

    if answers_user.any?
       answers_user.each do |id,answers|
          gold = answers_gold[id]

          if gold.nil?
             STDERR.puts "ERROR The question IDs in your file seem different from the IDs in the benchmark."
          end

          # OUT OF SCOPE questions
          if gold.length == 0 
             if answers.length == 0
                precision = 1
                recall    = 1 
                f1measure = 1
             else
                precision = 0
                recall    = 0
                f1measure = 0
             end
          # all other questions 
          else
                precision = (answers.select {|x| gold.include? x}).length.to_f / answers.length.to_f
                recall    = (gold.select    {|x| answers.include? x }).length.to_f / gold.length.to_f
                f1measure = recall == 0 ? 0 : (2 * precision * recall) / (precision + recall)
          end 

          results <<  { :id        => id.to_i,
                        :precision => precision.round(2), 
                        :recall    => recall.round(2),
                        :f1measure => f1measure.round(2) }
       end
    end

  return results
end

def compute_results(results,total)

    if results.empty? 
       return { :empty => true }
    end

    sum_precision = 0
    sum_recall    = 0

    results.each do |result|
      sum_precision += result[:precision]
      sum_recall    += result[:recall]
    end

    global_precision = sum_precision.to_f / total.to_f
    global_recall    = sum_recall.to_f / total.to_f
    global_f1measure = global_recall == 0 ? 0 : (2 * global_precision * global_recall) / (global_precision + global_recall)

    return { :global => { :precision => global_precision.round(4), 
                          :recall    => global_recall.round(4),
                          :f1measure => global_f1measure.round(4) },
             :local  => results.sort_by { |x| x[:id] } } 
end


#################################################################


answers_gold    = read_answers(input_gold)
answers_user    = read_answers(input_user)

results_dbpedia = evaluate_answers(answers_user[:dbpedia],answers_gold[:dbpedia])
results_hybrid  = evaluate_answers(answers_user[:hybrid], answers_gold[:hybrid])

context_dbpedia = compute_results(results_dbpedia,answers_gold[:dbpedia].keys.length)
context_hybrid  = compute_results(results_hybrid,answers_gold[:hybrid].keys.length)

html = Mustache.render(File.read(template),{ :gold    => input_gold,
                                             :system  => system,
                                             :config  => config,
                                             :time    => Time.now,
                                             :dbpedia => context_dbpedia, 
                                             :hybrid  => context_hybrid })

file = input_user + ".html"
File.write(file,html)
puts file
