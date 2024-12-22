import re
import os
from datetime import datetime

def creer_fichier_aa(texte_brut, fichier_aa):
    """
    Crée un fichier .aa à partir du texte brut
    """
    # Création de la structure XML de base
    timestamp = int(datetime.now().timestamp() * 1000)
    
    # Début du fichier XML
    contenu_aa = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<annotations>
<metadata corpusHashcode="114555-43065693"/>
<unit id="TXT_IMPORTER_{timestamp}">
<metadata>
<author>TXT_IMPORTER</author>
<creation-date>{timestamp}</creation-date>
<lastModifier>n/a</lastModifier>
<lastModificationDate>0</lastModificationDate>
</metadata>
<characterisation>
<type>paragraph</type>
<featureSet/>
</characterisation>
<positioning>
<start>
<singlePosition index="0"/>
</start>
<end>
<singlePosition index="{len(texte_brut)}"/>
</end>
</positioning>
</unit>
'''
    
    # Recherche des segments "maman chat" et "chaton"
    patterns = {
        'maman chat': r'\b(?:maman\s+chat|la\s+maman|sa\s+m[èe]re)\b',
        'chaton': r'\b(?:chaton|petit\s+chat|chatons?)\b'
    }
    
    unit_id = 1
    for type_segment, pattern in patterns.items():
        for match in re.finditer(pattern, texte_brut, re.IGNORECASE):
            # Ajout d'une unité pour chaque segment trouvé
            contenu_aa += f'''<unit id="segment_{unit_id}">
<metadata>
<author>auto</author>
<creation-date>{timestamp + unit_id}</creation-date>
<lastModifier>n/a</lastModifier>
<lastModificationDate>0</lastModificationDate>
</metadata>
<characterisation>
<type>{type_segment}</type>
<featureSet/>
</characterisation>
<positioning>
<start>
<singlePosition index="{match.start()}"/>
</start>
<end>
<singlePosition index="{match.end()}"/>
</end>
</positioning>
</unit>
'''
            unit_id += 1
    
    # Fin du fichier XML
    contenu_aa += '</annotations>'
    
    # Écriture du fichier .aa
    with open(fichier_aa, 'w', encoding='utf-8') as f:
        f.write(contenu_aa)
    
    return fichier_aa

def convertir_aa_vers_tsv(fichier_aa, fichier_sortie=None):
    """
    Convertit un fichier .aa en format TSV
    """
    if fichier_sortie is None:
        nom_base = os.path.splitext(os.path.basename(fichier_aa))[0]
        fichier_sortie = os.path.join('c:/Users/ananb/Downloads/poo/conversions_aa_tsv', f"{nom_base}.tsv")
    
    # Lecture du fichier .aa
    with open(fichier_aa, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Lecture du texte brut original
    with open('c:/Users/ananb/Downloads/poo/essai_brut.txt', 'r', encoding='utf-8') as f:
        texte_complet = f.read()
    
    # Écriture du fichier TSV
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        # En-têtes
        f.write("#FORMAT=WebAnno TSV 3.3\n")
        f.write("#T_CH=de.tudarmstadt.ukp.dkpro.core.api.coref.type.CoreferenceLink|referenceRelation|referenceType\n\n")
        
        # Écriture du texte complet
        f.write(f"#Text={texte_complet}\n")
        
        # Traitement du texte
        position = 0
        index = 1
        buffer = ""
        
        # Patterns pour la détection des segments
        patterns = {
            'maman chat': [
                r'\b(?:maman\s+chat|la\s+maman|sa\s+m[èe]re)\b',
                r'\b(?:maman|m[èe]re)\b(?:\s+chat)?'
            ],
            'chaton': [
                r'\b(?:chaton|petit\s+chat|chatons?)\b',
                r'\b(?:petit\s+chat|bébé\s+chat)\b'
            ]
        }
        
        # Fonction pour vérifier si un mot fait partie d'un segment
        def verifier_segment(mot, debut, fin):
            contexte = texte_complet[max(0, debut-20):min(len(texte_complet), fin+20)]
            for type_segment, pattern_list in patterns.items():
                for pattern in pattern_list:
                    for match in re.finditer(pattern, contexte, re.IGNORECASE):
                        if match.start() <= 20 and match.end() >= 20:  # Le mot est dans le segment
                            return type_segment
            return "_"
        
        for char in texte_complet:
            if char.isspace():
                if buffer:
                    # Vérifier si le mot fait partie d'un segment annoté
                    debut = position - len(buffer)
                    fin = position
                    type_segment = verifier_segment(buffer, debut, fin)
                    
                    # Écriture de la ligne TSV
                    f.write(f"{index}\t{debut}-{fin}\t{buffer}\t{type_segment}\t_\t\n")
                    index += 1
                    buffer = ""
                position += 1
            else:
                buffer += char
                position += 1
        
        # Traiter le dernier mot s'il existe
        if buffer:
            debut = position - len(buffer)
            fin = position
            type_segment = verifier_segment(buffer, debut, fin)
            f.write(f"{index}\t{debut}-{fin}\t{buffer}\t{type_segment}\t_\t\n")
    
    print(f"Conversion terminée. Fichier TSV créé : {fichier_sortie}")

# Test de la conversion
if __name__ == "__main__":
    try:
        # Lecture du texte brut
        with open('c:/Users/ananb/Downloads/poo/essai_brut.txt', 'r', encoding='utf-8') as f:
            texte_brut = f.read()
        
        # Création du fichier .aa 
        fichier_aa = 'c:/Users/ananb/Downloads/poo/conversions_aa_tsv/essai_brut.aa'
        print(f"\nCréation du fichier .aa : {fichier_aa}")
        creer_fichier_aa(texte_brut, fichier_aa)
        
        # Conversion en TSV
        print(f"\nConversion en TSV...")
        convertir_aa_vers_tsv(fichier_aa)
        
    except Exception as e:
        print(f"Erreur lors de la conversion : {str(e)}")
        import traceback
        print(traceback.format_exc())
