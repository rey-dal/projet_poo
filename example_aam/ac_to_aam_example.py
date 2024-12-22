import re
import xml.etree.ElementTree as ET

class TextAnnotator:
    def __init__(self):
        """Initialise les motifs pour l'annotation de texte.
        Ce constructeur définit les motifs regex pour identifier les différents types de personnages
        et d'éléments d'action dans le texte.
        """
        # Types de caractères et motifs
        self.personnage_patterns = {
            'bébé chat': r'\b(petit\s+chat|chaton)\b',
            'maman chat': r'\b(maman\s+chat|mère)\b',
            'autres chats': r'\b(chat|chatons)\b'
        }

        self.patterns = {
            'action': r'\b(tomb[eéa]|pleur[ea]|march[ea]|dor[mst]|miaul[ea]|s\'énerve|sauvé|rentre)\b',
            'mentalState': r'\b(pleur[ea]|peur|mal|s\'énerve)\b',
            'directSpeech': r'<dialogue>([^<]+)</dialogue>',
            'attentionGetter': r'\b(boum|miaou)\b',
            'openingOrClosing': r'\b(Il\s+était\s+une\s+fois|Il\s+y\s+avait|fin)\b',
            'instantiation': r'\b(Le\s+gros\s+chat|Un\s+petit\s+chat)\b', 
            'resolution': r'\b(sauvé|rentre|descend|tombé)\b'
        }

    def create_annotation(self, text_id: str, text: str) -> ET.Element:
        """Crée une annotation pour un texte donné."""
        annotation = ET.Element('unit')
        annotation.set('id', text_id)

        features = ET.SubElement(annotation, 'features')
        seen_features = {}  # Utilisation d'un dictionnaire pour ajouter chaque caractéristique une seule fois

        # Analyser les types de caractères
        for char_type, pattern in self.personnage_patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if char_type not in seen_features:
                    feature = ET.SubElement(features, 'feature')
                    feature.set('name', 'personnage')
                    feature.text = char_type
                    seen_features[char_type] = feature  # Ajoutons uniquement la première occurrence

        # Analyser les autres motifs
        for pattern_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if pattern_type not in seen_features:
                    feature = ET.SubElement(features, 'feature')
                    feature.set('name', pattern_type)
                    feature.text = match.group()
                    seen_features[pattern_type] = feature  # Ajoutons uniquement la première occurrence

        return annotation

    def create_annotations(self, input_text: str) -> ET.Element:
        """Crée des annotations pour le texte donné."""
        annotations = ET.Element('annotations')

        # Diviser le texte en lignes
        lines = input_text.strip().split('\n')
        for line in lines:
            if line.strip():
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    text_id, text_content = parts
                    annotation = self.create_annotation(text_id.strip(), text_content.strip())
                    annotations.append(annotation)

        return annotations

def save_annotations(annotations: ET.Element, output_file: str):
    """Sauvegarde les annotations dans un fichier XML au format .aam."""
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<annotationModel>\n  <units>\n'
    
    # Générer la sortie au format AAM
    for unit in annotations.findall('unit'):
        xml_str += f'    <type name="personnage">\n      <featureSet>\n'
        feature_set = unit.find('features')
        personnage_features = []  # Stocker les caractéristiques des personnages séparément
        action_features = []     # Stocker les actions séparément
        for feature in feature_set.findall('feature'):
            feature_name = feature.get("name")
            if feature_name == "personnage":
                personnage_features.append(feature.text)
            else:
                xml_str += f'        <feature name="{feature_name}">\n'
                xml_str += f'          <possibleValues default="{feature.text}">\n'
                xml_str += f'            <value>{feature.text}</value>\n'
                xml_str += f'          </possibleValues>\n'
                xml_str += f'        </feature>\n'

        # Ajouter les caractéristiques des personnages dans featureSet
        for char in personnage_features:
            xml_str += f'        <feature name="personnage">\n'
            xml_str += f'          <possibleValues default="{char}">\n'
            xml_str += f'            <value>{char}</value>\n'
            xml_str += f'          </possibleValues>\n'
            xml_str += f'        </feature>\n'

        xml_str += f'      </featureSet>\n    </type>\n'
    
    xml_str += '  </units>\n</annotationModel>\n'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)

def process_text(input_text: str, output_file: str):
    """Fonction principale de traitement du texte."""
    annotator = TextAnnotator()
    annotations = annotator.create_annotations(input_text)
    save_annotations(annotations, output_file)

# Test
if __name__ == '__main__':
    input_text = """48\tLe gros chat est endormi avec ses petits chatons et l'autre chat il se promène. Et le chat est tombé sur le tapis. Le chat pleure et l'autre chat est réveillé.
49\tUn petit chat qui marchait et après boum et le chat fait Miaou Miaou et sa mère s'énerve et sa mère l'a sauvé et elle rentre chez elle avec ce petit chat.
52\t<titre>L'histoire <omission type="préposition"/> 6 chats </titre> <segmentation/> Ils habitent dans une maison <omission type="pronom"/> il y avait des marches <segmentation/> le petit chat il descendit les marches avec la maman chat <segmentation/> le lendemain le petit chat descend les marches et tombe dans les marches boum <segmentation/> sa maman a vu le petit chat tomber <omission type="préposition"/>"""
    
    process_text(input_text, "example_aam/aam_output_example.aam")  # Sauvegarde sous le nom tagsmk.aam
