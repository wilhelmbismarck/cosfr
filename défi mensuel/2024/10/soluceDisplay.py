import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import soluce

class Display:
    def __init__(self, degrade_instance):
        self.degrade_instance : soluce.Dégradé = degrade_instance

    def display(self):
        # Configurer la figure
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        # Afficher l'image
        img = Image.new("RGB", (self.degrade_instance.size, self.degrade_instance.size))
        pixels = img.load()
        ccc = soluce.Cercle.ccc
        for i in range(self.degrade_instance.size):
            for j in range(self.degrade_instance.size):
                rgb = self.degrade_instance.image[i][j]
                pixels[j, i] = (rgb['r'], rgb['g'], rgb['b'])
        plt.imshow(img, extent = (-0.7, 0.7, -0.7, 0.7))
        
        # Tracer le cercle
        cercle = plt.Circle((0, 0), 1, color='lightblue', fill=False, linestyle='--')
        ax.add_artist(cercle)

        # Extraire les points de l'instance Dégradé
        points : dict = self.degrade_instance.cercle.points
        # Tracer les points avec leur nom
        point : soluce.Point
        for point in points.items():
            pt : soluce.Point = point[1]
            #print(pt.info())
            ax.plot(pt[0], pt[1], 'ro')  # Afficher le point
            ax.text(pt[0] + 0.05, pt[1] + 0.05, pt.name, fontsize=12, ha='center')  # Afficher le nom à côté

        # 1. Tracer le carré ABCD
        # Liste des sommets du carré
        square_vertices = ['A', 'B', 'C', 'D']
        square_coords = [points[vertex] for vertex in square_vertices]

        # Boucler pour tracer les côtés du carré
        for i in range(len(square_coords)):
            x_values = [square_coords[i][0], square_coords[(i+1) % 4][0]]
            y_values = [square_coords[i][1], square_coords[(i+1) % 4][1]]
            ax.plot(x_values, y_values, 'g-', label="Carré ABCD" if i == 0 else "")

        # 2. Tracer la droite LN
        if 'L' in points and 'N' in points:
            x_ln = [points['L'][0], points['N'][0]]
            y_ln = [points['L'][1], points['N'][1]]
            ax.plot(x_ln, y_ln, 'b--', label="Droite LN")

        # 3. Tracer la droite AA'/BB' (A' ou B' est la projection de A ou B sur LN)
        line = self.degrade_instance.proj
        if line in points and f'{line}\'' in points :
            x_aa_prime = [points[line][0], points[f"{line}'"][0]]
            y_aa_prime = [points[line][1], points[f"{line}'"][1]]
            ax.plot(x_aa_prime, y_aa_prime, 'r-.', label=f"Droite {line}{line}'")

        # Définir les limites des axes
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        # Titre et légende
        plt.title(f"Affichage du cercle, carré, droites LN et {line}{line}'")
        plt.legend()

        # Afficher le graphique
        plt.show()

# Exemple d'utilisation
# Supposons que degrade_instance est une instance de la classe Dégradé
# qui contient les points déjà définis dans son cercle
display = Display(soluce.a)
display.display()