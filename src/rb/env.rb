module Fogus
  class Env
    attr_reader :level
    
    def initialize(p=nil,b=nil)
      if b
        @bindings = b
      else
        @bindings = Hash.new
      end

      @parent = p

      if @parent
        @level = @parent.level + 1
      else
        @level = 0
      end
    end

    def get(key)
      if @bindings.has_key? key
        return @bindings[key]
      else
        return @parent.get(key) rescue raise "Unknown binding for #{key} in context #{@bindings.inspect}"
      end
    end

    def set(key, val)
      if @bindings.has_key? key
        @bindings[key] = val
      elsif @parent
        @parent.set(key, val)
      else
        @bindings[key] = val
      end
    end

    def def?(key)
      @bindings.has_key? key
    end

    def push(context=nil)
      Env.new(self, context)
    end

    def pop()
      @parent
    end
  end
end
