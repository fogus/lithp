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
WWW = 'http://fogus.me/_/lithp/'
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
    end

    def initialize
      @stdin    = STDIN
      @stdout   = STDOUT
      @stderr   = STDERR
      @rdr      = Reader.new
      @global   = Env.new
      @core = @closures = true

      bootstrap
    end

    def bootstrap
      @global.set('eq', Fun.new(@@eq))
    end
  end
end



repl = Fogus::Lithp.new
repl.print_banner
