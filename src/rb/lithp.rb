# The Lithp interpreter
# For more information:
#   http://www.slideshare.net/jza/python-3000
#   http://www.ibm.com/developerworks/linux/library/l-python3-1/
#   http://www.python.org/dev/peps/pep-3000/
#   http://www.python.org/dev/peps/
#   http://www.python.org/dev/peps/pep-0008/

require 'reader'
require 'env'
require 'lisp'
require 'fun'

NAME = 'Lithp'
VER = '0.0.1'
WWW = 'http://github.com/fogus/lithp'
PROMPT = 'lithp'
DEPTH_MARK = '.'

module Fogus
  class Lithp
    attr_reader :stdin, :stdout,   :stderr
    attr_reader :core,  :closures
    attr_reader :rdr,   :global

    def print_banner
      puts "The #{NAME} programming shell v#{VER}"
      puts "   by Fogus, #{WWW}"
      puts "   Type :help for more information"
      puts ""
    end

    def initialize
      @stdin           = STDIN
      @stdout          = STDOUT
      @stderr          = STDERR
      @rdr             = Reader.new
      @global          = Env.new
      @core, @closures = true, false

      bootstrap
    end

    def bootstrap
      @global.set('eq', Fun.new(@@eq))
    end

    def read_line(prompt)
      @stdout.write(prompt)
      line = @stdin.gets.strip

      if line.empty?
        :done
      end

      line
    end

    def get_complete_expr(line='',depth=0)
      line += ' ' unless line.empty?

      if @global.level != 0
        prompt = "#{PROMPT} #{@global.level}#{DEPTH_MARK * (depth + 1)}"
      else
        if depth == 0
          prompt = "#{PROMPT}> "
        else
          prompt = "#{PROMPT}#{DEPTH_MARK * (depth + 1)}"
        end

        line += read_line(prompt)
      end

      balance = 0;
      line.each_char {|c|
        if c.eql?('(')
          balance += 1
        elsif c.eql?(')')
          balance -= 1
        end
      }

      if balance > 0
        get_complete_expr(line, depth+1)
      elsif balance < 0
        raise "Unmatched parenthesis #{balance}"
      end

      line
    end

    def process(expr)
      puts 'this is where i will get the sexpr from the rdr'
      puts "for the expr #{expr}"
    end

    def go
      while true
        expr = get_complete_expr

        if expr.eql? ':quit'
          puts 'bye now'
          break
        elsif expr.eql? ':help'
          puts 'help is on its way'
        elsif expr == :done
          puts 'end of file encountered'
          break
        elsif expr.eql? ':env'
          puts 'todo - print env'
        else
          process(expr)
        end

        puts expr
      end
    end
  end
end

repl = Fogus::Lithp.new
repl.print_banner
repl.go

