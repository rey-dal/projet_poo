import re
import os

class ConvertisseurACtoTSV:
    def __init__(self, fichier_ac):
        """
        Initialise le convertisseur
        Args:
            fichier_ac (str): Chemin vers le fichier .ac à convertir
        """
        self.chemin = fichier_ac
        with open(fichier_ac, 'r', encoding='utf-8') as f:
            self.contenu = f.read()
        
    def extraire_segments(self):
        """
        Extrait les segments de texte du fichier .ac
        Returns:
            list: Liste des segments de texte avec leurs numéros
        """
        segments = []
        # Pattern pour trouver les segments numérotés
        pattern = r'(\d+)\t(.*?)(?=\n\d+\t|\Z)'
        matches = re.finditer(pattern, self.contenu, re.DOTALL)
        
        for match in matches:
            numero = match.group(1)
            texte = match.group(2).strip()
            segments.append((numero, texte))
        
        return segments
    
    def generer_tsv(self, fichier_sortie=None):
        """
        Génère le fichier TSV
        Args:
            fichier_sortie (str, optional): Nom du fichier de sortie. 
                                          Si non spécifié, utilise le même nom avec _ac_to_tsv.tsv
        """
        if fichier_sortie is None:
            # Prend le nom du fichier d'entrée sans extension et ajoute _ac_to_tsv.tsv
            nom_base = os.path.splitext(self.chemin)[0]
            fichier_sortie = f"convertisseur_ac_tsv/{os.path.basename(nom_base)}_ac_to_tsv.tsv"

        segments = self.extraire_segments()
        
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            # Écriture des en-têtes
            f.write("#FORMAT=WebAnno TSV 3.3\n")
            f.write("#T_CH=de.tudarmstadt.ukp.dkpro.core.api.coref.type.CoreferenceLink|referenceRelation|referenceType\n\n")
            
            for numero, texte in segments:
                # Écriture du texte avec son numéro
                f.write(f"\n#Text={numero}\\t{texte}\n")
                
                # Traitement des mots du segment
                mots = texte.split()
                position = 0
                
                for i, mot in enumerate(mots, 1):
                    # Calcul des positions de début et fin pour chaque mot
                    debut = texte.find(mot, position)
                    fin = debut + len(mot)
                    position = fin
                    
                    # Écriture de la ligne TSV pour chaque mot
                    f.write(f"{i}\t{debut}-{fin}\t{mot}\t_\t_\t\n")

# Test du convertisseur
if __name__ == '__main__':
    convertisseur = ConvertisseurACtoTSV('essai.ac')
    convertisseur.generer_tsv()
    print("Conversion terminée. Le fichier TSV a été créé: essai_ac_to_tsv.tsv")
