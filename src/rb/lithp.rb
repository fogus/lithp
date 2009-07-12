# The Lithp interpreter
# For more information:
#   http://www.slideshare.net/jza/python-3000
#   http://www.ibm.com/developerworks/linux/library/l-python3-1/
#   http://www.python.org/dev/peps/pep-3000/
#   http://www.python.org/dev/peps/
#   http://www.python.org/dev/peps/pep-0008/

NAME = 'Lithp'
VER = '0.0.1'
WWW = 'http://fogus.me'

module Lithp
  class Repl
    def print_banner
      puts "The #{NAME} programming shell v#{VER}"
      puts "   by Fogus, #{WWW}"
      puts "   Type :help for more information"
    end
  end
end



repl = Lithp::Repl.new
repl.print_banner

