import os

class ConvertisseurTXTtoConll:
    def __init__(self, fichier_txt):
        """
        Initialise le convertisseur
        Args:
            fichier_txt (str): Chemin vers le fichier .txt à convertir
        """
        self.chemin = fichier_txt
        self.texte = None
        self._lire_fichier_txt()
        
        # Crée le dossier conll_files s'il n'existe pas
        os.makedirs('conll_files', exist_ok=True)
    
    def _lire_fichier_txt(self):
        """
        Lit le fichier TXT
        """
        with open(self.chemin, 'r', encoding='utf-8') as f:
            self.texte = f.read()
    
    def _convertir_en_format_conll(self):
        """
        Convertit le texte en format CONLL
        Returns:
            list: Liste des lignes au format CONLL
        """
        lignes_conll = []
        phrases = self.texte.split('.')  # Sépare le texte en phrases
        
        for i, phrase in enumerate(phrases, 1):
            phrase = phrase.strip()
            if not phrase:  # Ignore les phrases vides
                continue
                
            # Ajoute les métadonnées de la phrase
            lignes_conll.append(f"# sent_id = {i}")
            lignes_conll.append(f"# text = {phrase}.")
            
            # Traite chaque mot de la phrase
            mots = phrase.split()
            for j, mot in enumerate(mots, 1):
                # Format CONLL : ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
                ligne_conll = f"{j}\t{mot}\t_\t_\t_\t_\t_\t_\t_\t_"
                lignes_conll.append(ligne_conll)
            
            # Ajoute une ligne vide entre les phrases
            lignes_conll.append("")
        
        return lignes_conll
    
    def generer_conll(self, fichier_sortie=None):
        """
        Génère le fichier CONLL
        Args:
            fichier_sortie (str, optional): Nom du fichier de sortie. 
                                          Si non spécifié, utilise le même nom avec _ac_to_conll.conll
        """
        if fichier_sortie is None:
            # Prend le nom du fichier d'entrée sans extension
            nom_base = os.path.splitext(os.path.basename(self.chemin))[0]
            fichier_sortie = os.path.join('conll_files', f"{nom_base}_ac_to_conll.conll")
        
        lignes_conll = self._convertir_en_format_conll()
        
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            for ligne in lignes_conll:
                f.write(f"{ligne}\n")

# Test du convertisseur
if __name__ == '__main__':
    convertisseur = ConvertisseurTXTtoConll('essai_brut.txt')
    convertisseur.generer_conll()
    print("Conversion terminée. Le fichier CONLL a été créé: conll_files/essai_brut_ac_to_conll.conll")
