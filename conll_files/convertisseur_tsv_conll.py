import os
import re

class ConvertisseurTSVtoConll:
    def __init__(self, fichier_tsv):
        """
        Initialise le convertisseur
        Args:
            fichier_tsv (str): Chemin vers le fichier .tsv à convertir
        """
        self.chemin = fichier_tsv
        self.texte = None
        self._lire_fichier_tsv()
    
    def _nettoyer_texte(self, texte):
        """
        Nettoie le texte en enlevant les balises XML et les numéros
        """
        # Enlève les balises XML et leur contenu
        texte = re.sub(r'<[^>]+>', '', texte)
        
        # Enlève les caractères spéciaux et les espaces multiples
        texte = texte.replace('\\t', ' ')  # Remplace \t par un espace
        texte = re.sub(r'\s+', ' ', texte)  # Remplace les espaces multiples par un seul espace
        
        # Enlève les numéros au début et à la fin des phrases
        texte = re.sub(r'^\d+\s*', '', texte)  # Numéros au début
        texte = re.sub(r'\s*\d+\s*$', '', texte)  # Numéros à la fin
        
        return texte.strip()
    
    def _lire_fichier_tsv(self):
        """
        Lit le fichier TSV et extrait le texte
        """
        texte_complet = []
        
        with open(self.chemin, 'r', encoding='utf-8') as f:
            for ligne in f:
                ligne = ligne.strip()
                
                # Ignore les lignes vides et les en-têtes
                if not ligne or ligne.startswith('#FORMAT') or ligne.startswith('#T_CH'):
                    continue
                
                # Si c'est une ligne de texte
                if ligne.startswith('#Text='):
                    # Extrait le texte après #Text=
                    texte = ligne[6:].strip()  # Enlève '#Text='
                    texte = self._nettoyer_texte(texte)
                    if texte:
                        texte_complet.append(texte)
        
        self.texte = ' '.join(texte_complet)
        # Nettoie une dernière fois pour enlever les numéros entre les phrases
        self.texte = re.sub(r'\s*\d+\s*', ' ', self.texte)
        self.texte = re.sub(r'\s+', ' ', self.texte)
    
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
                                          Si non spécifié, utilise le même nom avec _tsv_to_conll.conll
        """
        if fichier_sortie is None:
            # Prend le nom du fichier d'entrée sans extension
            nom_base = os.path.splitext(os.path.basename(self.chemin))[0]
            fichier_sortie = f"{nom_base}_tsv_to_conll.conll"
        
        lignes_conll = self._convertir_en_format_conll()
        
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            for ligne in lignes_conll:
                f.write(f"{ligne}\n")

# Test du convertisseur
if __name__ == '__main__':
    convertisseur = ConvertisseurTSVtoConll('c:/Users/ananb/Downloads/poo/essai.tsv')
    convertisseur.generer_conll()
    print("Conversion terminée. Le fichier CONLL a été créé: essai_tsv_to_conll.conll")
