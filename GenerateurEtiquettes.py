from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.platypus import Paragraph , KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import pandas as pd
import numpy as np
import json

class GenerateurEtiquettes:
    style_description = ParagraphStyle
    style_produit = ParagraphStyle
    largeur_page, hauteur_page = A4

    def __init__(self, marge_externe = 5 * mm, dimentions_page = A4):
        self.marge_externe = marge_externe
        styles = getSampleStyleSheet()
        self.style_produit = ParagraphStyle(
                "produit",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
                fontSize=17
            )
        self.style_description = ParagraphStyle(
                "produit",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                fontName="Helvetica",
                leading=8,
                fontSize=8
            )
        self.largeur_page, self.hauteur_page = dimentions_page
        with open('dimEtiquette.json', 'r') as file:
            self.type_etiquettes = json.load(file)
            self.petite_etiquettes = self.type_etiquettes["petite_etiquette"]
            self.moyenne_etiquettes = self.type_etiquettes["moyenne_etiquette"]
            self.grande_etiquettes = self.type_etiquettes["grande_etiquette"]
    
    def dessiner_grille(self, c, hauteur_etiquette, largeur_etiquette, nb_par_ligne, nb_par_colonne):
        c.setDash(6, 3)
        c.setStrokeColor(colors.black)
        for i in range(nb_par_ligne + 1):
            x = self.marge_externe + i * largeur_etiquette
            c.line(x, self.hauteur_page - hauteur_etiquette * nb_par_colonne - self.marge_externe, x, self.hauteur_page - self.marge_externe)
        for i in range(nb_par_colonne + 1):
            y = self.hauteur_page - self.marge_externe - i * hauteur_etiquette
            c.line(self.marge_externe, y, self.largeur_page - self.marge_externe, y)

    # Imprime le
    def print_gros_prix(self, canvas, prix, type_etiquette):
        # Transforme le prix en int pour enlever les décimales
        # Calcul emplacement prix
        # Calcul emplacement cents
        # Imprime prix et cents
        pass


    def generer_pdf_grande_etiquette(self, data, fichier_pdf="etiquettes.pdf"):
        c = canvas.Canvas(fichier_pdf, pagesize=(self.largeur_page, self.hauteur_page))
        largeur_section1 = 100 * mm
        hauteur_section1 = 35 * mm
        
        depart_section1 = [0,0]
        section1 = [[depart_section1[0], depart_section1[1]],
                     [depart_section1[0] + largeur_section1, depart_section1[0] +hauteur_section1]]
        
        
        pass

    def generer_pdf_petite_etiquettes(self, data, fichier_pdf="etiquettes.pdf", inverse = False):
        c = canvas.Canvas(fichier_pdf, pagesize=(self.largeur_page, self.hauteur_page))

        # Marges et dimensions
        largeur_etiquette = self.petite_etiquettes["largeur"] * mm
        hauteur_etiquette = self.petite_etiquettes["hauteur"] * mm
        nb_par_ligne = int((self.hauteur_page - 2 * self.marge_externe) / largeur_etiquette)
        nb_par_colonne = int((self.hauteur_page - 2 * self.marge_externe) / hauteur_etiquette) # Ajustable selon hauteur

        h_section_prix = self.petite_etiquettes["h_section_prix"] * mm
        h_section_desc = self.petite_etiquettes["h_section_desc"] * mm
        h_section_code = self.petite_etiquettes["h_section_code"] * mm

        marge_interne_x = self.petite_etiquettes["marge_interne_x"]
        marge_interne_y = self.petite_etiquettes["marge_interne_y"]

        nb_par_page = nb_par_ligne * nb_par_colonne
        
        # Lignes exterieures 
        self.dessiner_grille(c, hauteur_etiquette, largeur_etiquette, nb_par_ligne, nb_par_colonne)     
        
        c.setDash(1,0)
        c.setStrokeColor(colors.gray)
        i = 0
        for row in data.iterrows():
            if i > 0 and i % nb_par_page == 0:
                c.showPage()
                # Lignes exterieures 
                self.dessiner_grille(c, hauteur_etiquette, largeur_etiquette, nb_par_ligne, nb_par_colonne)

            col = i % nb_par_ligne
            lig = (i % nb_par_page) // nb_par_ligne

            x = self.marge_externe + col * largeur_etiquette
            y = self.hauteur_page - self.marge_externe - (lig + 1) * hauteur_etiquette
            h_code_bar = self.petite_etiquettes["h_code_bar"] * mm
            # Déclare Hauteur (du bas au haut)
            
            h_produit = y + h_code_bar + (h_section_code - h_code_bar)/2
            h_ligne_bas = y + h_section_code
            if(inverse):
                h_prix = h_ligne_bas + marge_interne_y
                h_ligne_haut = h_ligne_bas + h_section_prix
                h_desc = h_ligne_haut + h_section_desc/2
            else:    
                h_desc = h_ligne_bas + h_section_desc/2
                h_ligne_haut = h_ligne_bas + h_section_desc
                h_prix = h_ligne_haut + marge_interne_y

            # Prix (très gros)
            c.setFont("Helvetica-Bold", 30)
            c.drawCentredString(x + largeur_etiquette / 2, h_prix, f"{row[1].Coûtant:.2f} $")
            
            # Ligne haut
            c.setDash(1,0)
            c.setStrokeColor(colors.gray)
            c.line(x, h_ligne_haut, x+largeur_etiquette, h_ligne_haut)

            # Declare la description
            p = Paragraph(str(row[1].Description), self.style_description)
            p.wrapOn(c, largeur_etiquette - marge_interne_x * 2, (h_desc - 2 * marge_interne_y) * 3/4 )
            
            if not np.isnan(row[1].Ecofrais):
                # Declare les ecofrais
                combined_string = "Inclus " + str(row[1].Ecofrais) + "$ d'écofrais"
                pEf = Paragraph(combined_string, self.style_description)
                pEf.wrapOn(c, largeur_etiquette - marge_interne_x * 2, 20 * mm)
                h_desc -= pEf.height/2
                # Dessine les ecofrais
                pEf.drawOn(c, x + marge_interne_x, h_desc + p.height/2)
            # Dessine la description
            p.drawOn(c, x + marge_interne_x, h_desc - p.height/2)

            # Ligne bas
            c.line(x, h_ligne_bas, x + largeur_etiquette, h_ligne_bas)

            # Code du produit
            p2 = Paragraph(str(row[0]),self.style_produit)
            h = h_section_code - h_code_bar - marge_interne_y * 2
            w = largeur_etiquette - marge_interne_x * 2
            # S'assure que le code reste dans le frame
            k = KeepInFrame(w, h, [p2], mode='shrink')
            k.wrapOn(c, w, h)
            k.drawOn(c, x + marge_interne_x, h_produit)

            # Code-barres
            if pd.notna(row[0]):
                barcode = code128.Code128(str(row[0]), barHeight= h_code_bar, humanReadable=False)
                barcode.drawOn(c, x + (largeur_etiquette - barcode.width) / 2, y + 1)
            i += 1
        try:
            c.save()
            print(f"✅ PDF enregistré à : {fichier_pdf}")
        except:
            print(f"erreur lors de la sauvegarde du fichier")
            
    def paragraphe_ajuste_produit(self, text, width):
        # Démarrer avec la taille de police souhaitée
        font_size = self.style_produit.fontSize
        height_max = 12

        # On commence avec une copie du style
        while font_size >= 4:
            dynamic_style = ParagraphStyle(
                name='ProduitDynamic',
                parent=self.style_produit,
                fontSize=font_size
            )
            p2 = Paragraph(text, dynamic_style)
            w, h = p2.wrap(width, 15 * mm)
            if h <= height_max:
                return p2
            font_size -= 0.5


# Exemple d’utilisation avec données fictives
if __name__ == "__main__":
    df = pd.DataFrame([
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Ecofrais": 0.45, "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4) avec une vraiment longue description", "Ecofrais": 0.45, "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Ecofrais": 0.45, "Coûtant": 1499.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4)", "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Coûtant": 149.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4)", "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Coûtant": 149.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4)", "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Coûtant": 149.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4)", "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Coûtant": 149.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4)", "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Coûtant": 149.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "ABCDE12345", "Description": "Batterie rechargeable AA (paquet de 4)", "Coûtant": 14.95},
        {"No. Produit": "34/78-85", "Description": "Batterie de char", "Coûtant": 149.95},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
        {"No. Produit": "123456", "Description": "Lampe à DEL ajustable", "Coûtant": 19.99},
        {"No. Produit": "789012", "Description": "Câble HDMI 2m 4K", "Coûtant": 8.50},
    ])
    g = GenerateurEtiquettes()
    g.generer_pdf_petite_etiquettes(df, "etiquettes.pdf", True)