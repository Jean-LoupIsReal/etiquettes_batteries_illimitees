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
        
        with open('FichierDonnees/infoEtiquettes.json', 'r') as file:
            json_all_type_etiquettes = json.load(file)
        etiquette = json_all_type_etiquettes[type_etiquette]
        self.dimensions = {}
        for dim_name, dim_config in etiquette.items():
            if dim_name != "styles" :
                self.dimensions[dim_name] = dim_config * mm

        self.dimensions["marge_interne_x"] = etiquette["marge_interne_x"]
        self.dimensions["marge_interne_y"] = etiquette["marge_interne_y"]

        self.styles = {}
        for style_name, style_config in etiquette["styles"].items():
            self.styles[style_name] = ParagraphStyle(
                style_name,
                fontName = style_config["fontName"],
                fontSize = style_config["fontSize"],
                alignment = ALIGNMENTS.get(style_config["alignment"], TA_LEFT),
                leading = style_config["fontSize"] * style_config["leading_mult"]
            )
    


