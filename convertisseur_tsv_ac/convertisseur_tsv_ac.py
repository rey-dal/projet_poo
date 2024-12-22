import re
import os

class ConvertisseurTSVtoAC:
    def __init__(self, fichier_tsv):
        """
        Initialise le convertisseur
        Args:
            fichier_tsv (str): Chemin vers le fichier .tsv à convertir
        """
        self.chemin = fichier_tsv
        self.segments = []
        self._lire_fichier_tsv()
    
    def _lire_fichier_tsv(self):
        """
        Lit le fichier TSV et extrait les segments de texte
        """
        with open(self.chemin, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
        
        segment_courant = None
        texte_courant = None
        
        for ligne in lignes:
            ligne = ligne.strip()
            
            # Ignore les lignes vides et les en-têtes de format
            if not ligne or ligne.startswith('#FORMAT') or ligne.startswith('#T_CH'):
                continue
            
            # Si c'est une ligne de texte
            if ligne.startswith('#Text='):
                # Si on avait un segment précédent, on l'ajoute à la liste
                if segment_courant is not None and texte_courant is not None:
                    self.segments.append((segment_courant, texte_courant))
                
                # Extrait le numéro et le texte
                match = re.match(r'#Text=(\d+)\\t(.*)', ligne)
                if match:
                    segment_courant = match.group(1)
                    texte_courant = match.group(2)
            
        # N'oublie pas d'ajouter le dernier segment
        if segment_courant is not None and texte_courant is not None:
            self.segments.append((segment_courant, texte_courant))
    
    def generer_ac(self, fichier_sortie=None):
        """
        Génère le fichier AC
        Args:
            fichier_sortie (str, optional): Nom du fichier de sortie. 
                                          Si non spécifié, utilise le même nom avec _tsv_to_ac.ac
        """
        if fichier_sortie is None:
            # Prend le nom du fichier d'entrée sans extension et ajoute _tsv_to_ac.ac
            nom_base = os.path.splitext(self.chemin)[0]
            fichier_sortie = f"convertisseur_tsv_ac/{os.path.basename(nom_base)}_tsv_to_ac.ac"
        
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            for numero, texte in self.segments:
                f.write(f"{numero}\t{texte}\n")

# Test du convertisseur
if __name__ == '__main__':
    convertisseur = ConvertisseurTSVtoAC('essai.tsv')
    convertisseur.generer_ac()
    print("Conversion terminée. Le fichier AC a été créé: essai_tsv_to_ac.ac")
