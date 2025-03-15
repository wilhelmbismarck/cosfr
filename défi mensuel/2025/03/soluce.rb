class Matrice

    #attr_accessor :ordre, :list, :max

    def initialize(ordre = 100)
        @ordre = ordre
        @list  = Array.new(ordre) { Array.new(ordre, 0) }
        @max   = 0
    end

    def to_s
        txt = 'Matrice'
        maxLen = @max.to_s.length
        @ordre.times do |j|
            txt += "\n"
            @ordre.times do |i|
                item = @list[j][i]
                iLen = item.to_s.length
                if   iLen < maxLen then txt += " "*(maxLen - iLen) end
                txt += item.to_s + " "
                end
            end
        return txt
    end

    def verifierIndex(i, j)
        if i >= @ordre then raise IndexError.new("indice [i] au-delà des limites") end
        if j >= @ordre then raise IndexError.new("indice [j] au-delà des limites") end
        if i < 0 then return self.verifierIndex(@ordre + i, j) end
        if j < 0 then return self.verifierIndex(i, @ordre + j) end
        return [i, j]
    end

    def [](i, j)
        bi, bj = self.verifierIndex(i, j)
        return @list[bj][bi]
    end

    def incrementer(i, j)
        bi, bj = self.verifierIndex(i, j)
        @list[bj][bi] += 1
        if @list[bj][bi] > @max then @max = @list[bj][bi] end
    end

    def appartientCercle(i, j)
        bi, bj   = self.verifierIndex(i, j)
        centre   = (@ordre - 1) / 2
        distance = (centre - bi)**2 + (centre - bj)**2
        rayon    = (@ordre / 2)**2
        return distance <= rayon
    end

    def getOrdre
        return @ordre
    end

    def getMax
        return @max
    end

    def each
        j = 0
        @ordre.times do
            i = 0
            @ordre.times do
                yield [@list[j][i], i, j]
                i += 1
            end
            j += 1
        end
    end
end

def approcherPI(matrice)
    if matrice.getMax == 0 then raise StandardError.new("Pas de lancers dans la matrice.") end
    countOUT, countIN = [0.0, 0.0]
    matrice.each { |item, i, j| if matrice.appartientCercle(i, j) then countIN += item.to_f else countOUT += item.to_f end }
    return ((4 * countIN) / (countOUT + countIN))
end

def simulerLancer(matrice, n = 200)
    b = matrice.getOrdre - 1
    n.times do matrice.incrementer(rand(0..b), rand(0..b)) end
end

A = Matrice.new(10)
#puts A
simulerLancer(A, 20000)
#puts A
puts approcherPI(A)