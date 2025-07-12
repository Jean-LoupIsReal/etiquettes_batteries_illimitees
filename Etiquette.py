import os
import json
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import mm

ALIGNMENTS = {
    "CENTER": TA_CENTER,
    "RIGHT": TA_RIGHT,
    "LEFT": TA_LEFT
}

class Etiquette:
    style_description = ParagraphStyle
    style_code = ParagraphStyle
    style_prix_dollar = ParagraphStyle
    style_prix_cent = ParagraphStyle

    STYLE_DESCRIPTION = 0
    STYLE_CODE = 1
    STYLE_PRIX = 2
    STYLE_PRIX_DOLLAR = 2
    STYLE_PRIX_CENT = 3


    def __init__(self, type_etiquette):
        try:
            
            with open('infoEtiquettes.json', 'r') as file:
                json_all_type_etiquettes = json.load(file)
            etiquette = json_all_type_etiquettes[type_etiquette]

            self.largeur_etiquette = etiquette["largeur"] * mm
            self.hauteur_etiquette = etiquette["hauteur"] * mm

            self.h_section_prix = etiquette["h_section_prix"] * mm
            self.h_section_desc = etiquette["h_section_desc"] * mm
            self.h_section_code = etiquette["h_section_code"] * mm

            self.marge_interne_x = etiquette["marge_interne_x"]
            self.marge_interne_y = etiquette["marge_interne_y"]

        except:
            print("Le type d'etiquette (" + type_etiquette + ") n'existe pas dans la reference. Regarder fichier dimEtiquettes.json")
            os.system("pause")
            exit(1)

        #styles_sheet = getSampleStyleSheet()
        self.styles = {}
        for style_name, style_config in etiquette["styles"].items():
            self.styles[style_name] = ParagraphStyle(
                style_name,
                fontName = style_config["fontName"],
                fontSize = style_config["fontSize"],
                alignment = ALIGNMENTS.get(style_config["alignment"], TA_LEFT),
                leading = style_config["fontSize"] * style_config["leading_mult"]
            )
    


