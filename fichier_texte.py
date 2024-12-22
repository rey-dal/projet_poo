import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class FichierTexte:
    def __init__(self, chemin_fichier):
        """
        Initialise un objet FichierTexte
        Args:
            chemin_fichier (str): Chemin vers le fichier à traiter
        """
        self.chemin = chemin_fichier
        self.contenu = self._lire_fichier()

    def _lire_fichier(self):
        """Lit le contenu du fichier"""
        with open(self.chemin, 'r', encoding='utf-8-sig') as f:
            return f.read()

    def afficher_texte_brut(self):
        """
        Retourne le texte brut sans les balises XML et sans les numéros
        Returns:
            str: Texte sans balises et sans numéros
        """
        # Supprime toutes les balises XML
        texte = re.sub(r'<[^>]+>', '', self.contenu)
        # Supprime tous les numéros, qu'ils soient isolés ou collés aux mots
        texte = re.sub(r'\d+\.?\d*|\w+\.\d+|\w+\d+', '', texte)
        # Nettoie les espaces multiples
        texte = re.sub(r'\s+', ' ', texte)
        return texte.strip()

    def compter_caracteres(self):
        """
        Compte le nombre de caractères dans le texte brut
        Returns:
            int: Nombre de caractères
        """
        return len(self.afficher_texte_brut())

    def compter_mots(self):
        """
        Compte le nombre de mots dans le texte brut
        Returns:
            int: Nombre de mots
        """
        texte = self.afficher_texte_brut()
        return len(texte.split())

    def creer_nuage_mots(self, nom_fichier='nuage_mots.png'):
        """
        Crée un nuage de mots et le sauvegarde dans un fichier
        Args:
            nom_fichier (str): Nom du fichier de sortie pour l'image
        """
        texte = self.afficher_texte_brut().lower()
        wordcloud = WordCloud(width=800, height=400, 
                            background_color='white',
                            max_words=100,
                            contour_width=3,
                            contour_color='steelblue')
        wordcloud.generate(texte)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(nom_fichier)
        plt.close()

    def sauvegarder_texte_brut(self, nom_fichier=None):
        """
        Sauvegarde le texte brut dans un fichier
        Args:
            nom_fichier (str, optional): Nom du fichier de sortie. Si non spécifié,
                                       utilise le nom du fichier d'entrée avec '_brut.txt'
        """
        if nom_fichier is None:
            # Prend le nom du fichier d'entrée sans extension et ajoute _brut.txt
            nom_base = self.chemin.rsplit('.', 1)[0]
            nom_fichier = f"{nom_base}_brut.txt"
            
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write(self.afficher_texte_brut())

# Test de la classe
if __name__ == '__main__':
    ft = FichierTexte('essai.ac')
    
    # Affichage du texte brut et sauvegarde
    texte_brut = ft.afficher_texte_brut()
    ft.sauvegarder_texte_brut()  # Utilisera automatiquement 'essai_brut.txt'
    
    # Lecture du fichier de sortie pour vérification
    nom_sortie = 'essai_brut.txt'
    with open(nom_sortie, 'r', encoding='utf-8') as f:
        texte_sortie = f.read()
    
    print(f"Statistiques du texte nettoyé ({nom_sortie}) :")
    print(f"Nombre de caractères : {len(texte_sortie)}")
    print(f"Nombre de mots : {len(texte_sortie.split())}")
    
    print("\nVérification que les statistiques sont identiques :")
    print(f"Nombre de caractères (méthode de classe) : {ft.compter_caracteres()}")
    print(f"Nombre de mots (méthode de classe) : {ft.compter_mots()}")
    
    # Création du nuage de mots
    ft.creer_nuage_mots('nuage_mots.png')
    print("\nLe nuage de mots a été sauvegardé dans 'nuage_mots.png'")