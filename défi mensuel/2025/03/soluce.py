class Matrice :
    """Matrice simulée avec une liste en 2D."""
    
    def __init__(self, ordre : int = 100):
        self.ordre : int  = ordre
        self.list  : list = [ [ 0 for _ in range(0, ordre) ] for _ in range(0, ordre) ]
        self.max   : int = 0
        
    def vérifierIndex(self, i : int, j : int) -> tuple :
        if i >= self.ordre or j >= self.ordre : raise IndexError("soit i soit j en dehors de la plage des indices valables")
        if i < 0 : i = self.ordre + i
        if j < 0 : j = self.ordre + j
        return(i, j)        

    def __getitem__(self, i : int, j : int) -> int :
        i, j = self.vérifierIndex(i, j)
        return self.list[j][i]
    
    def incrémenter(self, i : int, j : int):
        i, j = self.vérifierIndex(i, j)
        self.list[j][i] += 1
        if self.list[j][i] > self.max : self.max = self.list[j][i]
        
    def appartientCercle(self, i : int, j : int) -> bool :
        i, j = self.vérifierIndex(i, j)
        centre   : float = (self.ordre - 1) / 2
        distance : float = (centre - i)**2 + (centre - j)**2
        rayon    : float = (self.ordre / 2)**2
        return distance <= rayon
    
    def __str__(self) -> str :
        txt : str = "Matrice"
        maxLen : int = len(str(self.max))
        for j in self.list :
            txt += '\n'
            for i in j     :
                iLen : int = len(str(i))
                if iLen < maxLen :
                       txt += " "*(maxLen-iLen) + str(i)
                else : txt += str(i)
                txt += ' '
        return txt
    
    def getOrdre(self) -> int : return self.ordre
    
    def __iter__(self) :
        for j in range(0, self.ordre):
            for i in range(0, self.ordre):
                yield (i, j, self.list[j][i])

def approcherPI(matrice : 'Matrice') -> float :
    """À partir d'une matrice, approche π."""
    if matrice.max == 0 : raise ValueError("Pas de lancers dans la matrice.")
    count   : int = 0
    countIn : int = 0
    for element in matrice :
        pos : bool = matrice.appartientCercle(element[0], element[1])
        if pos : countIn += element[2]
        count += 1
    return 4 * (countIn / count)

def simulerLancer(matrice : 'Matrice', n : int = 1):
    """Simule n lancers aléatoires dans la matrice donnée."""
    from random import randint
    for _ in range(n): matrice.incrémenter(randint(0, matrice.getOrdre()-1), randint(0, matrice.getOrdre()-1))

# Création de la matrice
A = Matrice(100)
# Nombre de lancers dans la matrice - essayez avec une valeur de n différente
simulerLancer(A, 20000)
# Approche de π
print("π ≈ ", approcherPI(A), "; π = 3.14159")
