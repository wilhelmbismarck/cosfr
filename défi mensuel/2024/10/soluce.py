### Définition de l'objet Angle

class Angle :
    """[objet / Angle] Représente un angle mathématique en degrès."""
    
    def __init__(self, val : int = 0) :
        if not 0 <= val < 360: raise ValueError(f"la valeur {val} n'est pas dans [0 : 360[")
        self.a : int = val
        
    def __add__(self, other : 'Angle') -> 'Angle' :
        """[Angle + Angle]"""
        return (self.a + other.a) % 360
    
    def __sub__(self, other : 'Angle') -> 'Angle' :
        """[Angle - Angle]"""
        return (self.a - other.a) % 360
    
    def opposé(self) -> 'Angle' :
        """[Angle] Retourne l'angle opposé à l'angle actuel."""
        return Angle((self.a + 180) % 360)
    
    def get(self) -> int :
        """[Angle] Retourne la valeur de l'angle, en degrés."""
        return self.a
        
    def rad(self) -> float :
        """[Angle -> Radians]"""
        pi : float = 3.1415925
        return self.a / 180 * pi
    
    def cos(self) -> float :
        """[cos(Angle)]"""
        from math import cos
        return cos(self.rad())
        
    def sin(self) -> float :
        """[sin(Angle)]"""
        from math import sin
        return sin(self.rad())
    
    def __str__(self) -> str :
        """[Angle -> str]"""
        return f'{self.a} degrès'
    
    def __repr__(self) -> str :
        """[display Angle]"""
        return str(self)
       
### Définition de l'objet Octet  

class Octet :
    """[objet / Octet]"""
    
    def __init__(self, val : int = 0) :
        if not 0 <= val <= 255: raise ValueError(f"la valeur {val} ne peut pas représenter un octet")
        self.nb : int = val
        
    def __add__(self, other : 'Octet') -> 'Octet' :
        """[Octet + Octet]"""
        sm = self.nb + other.nb
        if sm > 255 : return Octet(255)
        else : return Octet(sm)
    
    def __sub__(self, other : 'Octet') -> 'Octet' :
        """[Octet + Octet]"""
        sm = self.nb - other.nb
        if sm < 0 : return Octet(0)
        else : return Octet(sm)
    
    def __lt__(self, nb : float) -> bool :
        return self.nb < nb
    
    def __gt__(self, nb : float) -> bool :
        return self.nb > nb
    
    def __le__(self, nb : float) -> bool :
        return self.nb <= nb
    
    def __ge__(self, nb : float) -> bool :
        return self.nb >= nb
    
    def __eq__(self, nb : float) -> bool :
        return self.nb == nb
        
    def hex(self) -> str :
        """[Octet -> Hex]"""
        return hex(self.nb)
    
    def __str__(self) -> str:
        """[Octet -> str]"""
        return self.hex()
    
    def __repr__(self) -> str:
        """[display Octet]"""
        return self.hex()

### Définition de l'objet RGB

class RGB :
    """[objet / RGB]"""
    
    def __init__(self, r : int = 255, g : int = 255, b : int = 255) :
        self.r = Octet(r)
        self.g = Octet(g)
        self.b = Octet(b)
    
    @staticmethod
    def mix(clr1 : 'RGB', clr2 : 'RGB', strength : float = 50) -> 'RGB' :
        if not 0 <= strength <= 100: raise ValueError('la force doit être comprise dans [0 ; 100]')
        r = int((clr1.r.nb * (100 - strength) + clr2.r.nb * strength) / 100) # on mélange le canal Rouge
        g = int((clr1.g.nb * (100 - strength) + clr2.g.nb * strength) / 100) # on mélange le canal Vert
        b = int((clr1.b.nb * (100 - strength) + clr2.b.nb * strength) / 100) # on mélange le canal Bleu
        return RGB(r, g, b)
    
    def __getitem__(self, val : str) :
        if val in ['R', 'r', 'red']   : return self.r.nb
        if val in ['G', 'g', 'green'] : return self.g.nb
        if val in ['B', 'b', 'blue']  : return self.b.nb
        return 0
    
    def __str__(self) -> str :
        """[RGB -> str]"""
        return f'RGB({self.r}, {self.g}, {self.b})'
        
    def __repr__(self) -> str :
        """[display RGB]"""
        return str(self)
        
### Définition du gestionnaire trigonométrique

class Point   : 
    """[objet / Point & Vecteur]"""
    
    def __init__(self, x : float = 0, y : float = 0, name : str = 'point', déf : str = '') :
        self.co       : tuple = (x, y)
        self.name       : str = name
        self.définition : str = déf
        
    def __str__(self) -> str :
        return self.name
    
    def info(self) -> str :
        return f'Point {self.name} de coordonnées ({self.co[0]}, {self.co[1]}) ({self.définition})'
        
    def __getitem__(self, val : int) :
        return self.co[val % 2]
        
    def __add__(self, other : 'Point') -> 'Point' :
        """[Point] Aditionne le point à un autre et modifie ses coordonnées."""
        x = self[0] + other[0]
        y = self[1] + other[1]
        return Point(x, y, self.name + other.name, f'add de {self.name} et {other.name}')
    
    def __sub__(self, other : 'Point') -> 'Point' :
        """[Point] Soustrait le point à un autre et modifie ses coordonnées."""
        x = self[0] - other[0]
        y = self[1] - other[1]
        return Point(x, y, self.name + other.name, f'sub de {self.name} et de {other.name}')
        
    def __mul__(self, other : 'Point') -> float :
        """[Point] Produit scalaire."""
        return self[0] * other[0] + self[1] * other[1]
    
    def __truediv__(self, val : float) -> 'Point' :
        """[Point] Augmenter les coordonnées du point d'une certaine valeur [1 = 100%, 0 = 0%]."""
        return Point(self[0] * val, self[1] * val, self.name, self.définition)
        
    def setName(self, val : str) -> None :
        self.name = val
        
    def x(self) -> float :
        """[Point] Retourne l'abscisse x du point."""
        return self.co[0]
    
    def y(self) -> float :
        """[Point] Retourne l'ordonnée y du point."""
        return self.co[1]
    
    def distance(self, A : 'Point') -> float :
        """[Point] Retourne la distance entre deux points."""
        dX : float = A[0] - self[0]
        dY : float = A[1] - self[1]
        return ((dX**2) + (dY**2))**(1/2)
    
    def projectionOrthogonale(S, A : 'Point', B : 'Point') -> 'Point' :
        """[Point] Projète le point [nommé 'S'] sur la droite formée par deux autres points [nommés 'A' et 'B']."""
        # Calculs des vecteurs
        vecteurAB = B - A
        vecteurAB.setName(f'vecteur {A.name}{B.name}')
        vecteurAS = S - A
        vecteurAS.setName(f'vecteur {A.name}{S.name}')
        # Produit Scalaire
        produitSc = vecteurAB * vecteurAS
        # Coefficient de projection
        normeCarrée = vecteurAB[0]**2 + vecteurAB[1]**2
        projection  = produitSc / normeCarrée
        # Calcul des coordonnées
        vecteurAP : Point = vecteurAB / projection
        vecteurAP.setName(f'projection sur {A.name}{B.name}')
        pointProj : Point = A + vecteurAP
        pointProj.setName(S.name + "\'")
        return pointProj

class Cercle  :
    """[objet / Cercle]"""
    
    ccc : float =  2**(1/2)
    
    def __init__(self) :
        self.rayon  : int   = 1
        self.points : dict  = {'!Z' : Point(0, 0, 'Z', 'origine du repère')}
        
    def __getitem__(self, key) -> Point :
        if not key in self.points : raise KeyError(f"le point '{key}' n'existe pas")
        return self.points[key]
        
    def placerPoint(self, angle : Angle, nom : str = 'pointCercle') -> None :
        if nom[0] == '!': raise ValueError(f"le nom '{nom}' est incorrect.")
        x : float = self['!Z'][0] + self.rayon * angle.cos()
        y : float = self['!Z'][1] + self.rayon * angle.sin()
        p : Point = Point(x, y, nom, f'correspondant à {angle}')
        self.points[nom] = p
    
    def ajoutPoint(self, point : Point) -> None :
        self.points[point.name] = point
    
    def placePoint(self, x : int, y : int, size : int) -> None :
        pX = (x / size * Cercle.ccc) - (Cercle.ccc / 2)
        pY = (y / size * Cercle.ccc) - (Cercle.ccc / 2)
        self.points['M'] =  Point(pX, pY, 'M', 'pixel de matrice')
    
    def indexPoint(self, point : Point, size : int) -> tuple :
        x = 0 + int((0.5 + point[0]) * size)
        y = 0 + int(abs(0.5 - point[1]) * size)
        return (x, y)
        
### Définition du gestionnaire de dégradé

class Dégradé :
    """[objet / Dégradé] Crée et stocke un dégradé."""

    def __init__(self, angle : int = 0, color1 : RGB = RGB(255, 0, 0), color2 : RGB = RGB(0, 0, 255), size : int = 100) :
        # Assertions
        if size < 16 : raise ValueError(f"taille ({size}) < 16, ce qui n'est pas autorisé")
        # Optimisation pour les angles pouvant être inversés.
        self.angle = Angle(angle % 180)
        if self.angle.get() < 180 :
            self.color1 = color1
            self.color2 = color2
        else            : 
            self.color1 = color2
            self.color2 = color1
        # Fin SI
        # Gestion de la taille du dégradé
        self.size   : int    = size
        # Gestion du cercle
        self.cercle : Cercle = Cercle()
        self.cercle.placerPoint(self.angle, 'L')
        self.cercle.placerPoint(self.angle.opposé(), 'N')
        self.cercle.placerPoint(Angle(135), 'A')
        self.cercle.placerPoint(Angle(45), 'B')
        self.cercle.placerPoint(Angle(315), 'C')
        self.cercle.placerPoint(Angle(225),  'D')
        if self.angle.get() < 90 : self.proj : str = 'B'
        else                     : self.proj : str = 'A'
        self.cercle.ajoutPoint(self.cercle[self.proj].projectionOrthogonale(self.cercle['L'], self.cercle['N']))
        # Création du dégradé
        self.image = self.créer()
        
    def créer(self) -> list :
        from math import dist
        """[Dégradé / Création] créé un dégradé à partir des termes initialisés plus tôt."""
        # Création d'une image vide
        img  = []
        startP : str   = f"{self.proj}\'"
        progCR : float = 2 - (2 * self.cercle['L'].distance(self.cercle[startP]))
        pointL : Point = self.cercle['L']
        pointN : Point = self.cercle['N']
        for i in range(self.size) :
            ligne = []
            for j in range (self.size) :
                self.cercle.placePoint(j, i, self.size)
                self.cercle.ajoutPoint(self.cercle['M'].projectionOrthogonale(pointL, pointN))
                project : float = self.cercle["M\'"].distance(self.cercle[startP])
                facteur : float = max(min(project / progCR, 1), 0) * 100
                ligne.append(RGB.mix(self.color1, self.color2, facteur))
            img.append(ligne)
        return img
    
    def __str__(self) -> str:
        """[Dégradé -> Str]"""
        txt = ''
        for ligne in self.image:
            txt += " ".join([f"{couleur}" for couleur in ligne])
        return txt
        
    def save(self, fichier : str = 'degrade_image'):
        """[Dégradé -> Image]"""
        from PIL import Image # nécessite le module Pillow
        # Créer une image avec Pillow
        img = Image.new("RGB", (self.size, self.size))
        pixels = img.load()
        # Parcourir l'image en liste et remplir les pixels de l'image Pillow
        for i in range(self.size):
            for j in range(self.size):
                rgb = self.image[i][j]
                pixels[j, i] = (rgb.r.nb, rgb.g.nb, rgb.b.nb)
        # Sauvegarder l'image sous forme de fichier PNG
        img.save(fichier + '.png')
        print(f"Image enregistrée sous le nom : {fichier}.png")
            
a = Dégradé(13, RGB(133, 92, 214), RGB(50, 133, 84), 64)
a.save(fichier = 'dégradéA')