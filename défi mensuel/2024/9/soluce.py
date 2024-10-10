class Point():
    """## classe Point
    - note : une classe est un objet personnalisé
    """
    
    def __init__(self, x : float = 0, y : float = 0):
        """
        ## classe Point - Initialisation de l'objet
        - crée un objet « point » contenant deux cordonnées, accessible via "nom.x" et "nom.y".
        """
        self.x = x
        self.y = y
    
class Triangle():
    
    def __init__(self, p1 : Point, p2 : Point, p3 : Point):
        """
        ## classe Triangle - Initialisation de l'objet
        - crée un objet « triangle » constitué de trois points (classe Point), accessible via "nom.a", "nom.b" et "nom.c".
        """
        self.a = p1
        self.b = p2
        self.c = p3
        
    def airePolySym(self, point : Point, p1 : Point, p2 : Point):
        """
        ## classe Triangle - Appartenance d'un point à une droite
        - retourne l'aire d'un polygonne formé par un premier point générique et deux points donnés formant une droite, le dernier point étant le symétrique du premier via la droite formée par les deux suivants.
        - note : si aire = 0, alors le point appartient à la droite ; si aire ≠ 0, le point est situé d'un côté ou de l'autre de la droite (si positif droite, ou négatif gauche, dépend de l'ordre des points donnés).
        """
        aire = ((p2.x - point.x) * (p1.y - point.y) - (p2.y - point.y) * (p1.x - point.x))
        return aire
    
    def dans_triangle(self, point : Point):
        """
        ## classe Triangle - Appartenance d'un point à un triangle
        - vérifie si un point est dans un triangle en vérifiant si le point est situé à droite (avec aire ≥ 0) des trois côtés du triangle.
        """
        if self.airePolySym(point, self.a, self.b)  >= 0 and self.airePolySym(point, self.b, self.c)  >= 0 and self.airePolySym(point, self.c, self.a) >= 0:
            return True # vrai
        return False # faux
    
# Code de démonstration
monTriangle = Triangle(Point(0, 0), Point(2, 2), Point(4, 0))
print(monTriangle.dans_triangle(Point(1, 0)))
print(monTriangle.dans_triangle(Point(2, 3)))