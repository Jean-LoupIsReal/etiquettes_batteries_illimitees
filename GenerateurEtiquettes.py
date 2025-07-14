from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.platypus import Paragraph , KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
import pandas as pd
import numpy as np
import json
import os
from Etiquette import Etiquette
class GenerateurEtiquettes:
    style_description = ParagraphStyle
    style_code = ParagraphStyle
    etiquette = Etiquette


    def __init__(self, marge_externe = 5 * mm, dimentions_page = A4):
        self.marge_externe = marge_externe
        self.largeur_page, self.hauteur_page = dimentions_page
    
    # Dessine les lignes exterieurs des etiquettes sur le canva pour pas qu'elle ne fasse plusieurs instance sur la meme ligne,
    # cause problemes avec pointille.
    def dessiner_grille(self, c, hauteur_etiquette, largeur_etiquette):
        c.setDash(6, 3)
        c.setStrokeColor(colors.black)
        for i in range(self.nb_par_ligne + 1):
            x = self.marge_externe + i * largeur_etiquette
            c.line(x, self.hauteur_page - hauteur_etiquette * self.nb_par_colonne - self.marge_externe, x, self.hauteur_page - self.marge_externe)
        for i in range(self.nb_par_colonne + 1):
            y = self.hauteur_page - self.marge_externe - i * hauteur_etiquette
            c.line(self.marge_externe, y, self.largeur_page - self.marge_externe, y)

    # Imprime le prix sur le c
    def print_prix_separe(self, c, prix, x_etiquette, y_etiquette):
        # Transforme le prix en int pour enlever les décimales.
        prix_dollars = int(prix)
        prix_cents = round((prix - prix_dollars) * 100)
        # Declare largeur des sections
        largeur_dollar = (self.etiquette.dimensions["l_section_prix"] - 2 * self.etiquette.dimensions["marge_interne_x"]) * 2/3
        largeur_cent = largeur_dollar/2
        # Déclare les paragraphes
        paragraph_dollars = Paragraph(f"{prix_dollars}", self.etiquette.styles["style_prix_dollar"])
        paragraph_cent = Paragraph(f",{prix_cents}$", self.etiquette.styles["style_prix_cent"])
        paragraph_cent.wrapOn(c, largeur_dollar)
        paragraph_dollars.wrapOn(c, largeur_cent)
        # Calcul emplacement prix.
        x_pos_dollars = x_etiquette + self.etiquette.dimensions["largeur"] + self.etiquette.dimensions["marge_interne_x"]
        y_pos_dollars = y_etiquette + self.etiquette.dimensions["h_section_prix"] * 3/5
        # Calcul emplacement cents.
        x_pos_cent = x_pos_dollars + largeur_dollar + self.etiquette.dimensions["marge_interne_x"]
        y_pos_cent = y_pos_dollars + paragraph_dollars.height / 2  - paragraph_cent.height / 2
        # Imprime prix et cents.
        paragraph_dollars.drawOn(c, x_pos_dollars, y_pos_dollars)
        paragraph_cent.drawOn(c, x_pos_cent, y_pos_cent)
        
        
    def test_grande_etiquette(self, data, variante = False):
        c = canvas.Canvas("test.pdf", pagesize=(self.largeur_page, self.hauteur_page))
        # Marges et dimensions
        self.etiquette = Etiquette()
            
        self.nb_par_ligne = int((self.largeur_page - 2 * self.marge_externe) / self.etiquette.dimensions["largeur"])
        self.nb_par_colonne = int((self.hauteur_page - 2 * self.marge_externe) / self.etiquette.dimensions["hauteur"]) # Ajustable selon hauteur
        self.nb_par_page = self.nb_par_ligne * self.nb_par_colonne

        # Lignes exterieures 
        self.dessiner_grille(c, self.etiquette.dimensions["hauteur"], self.etiquette.dimensions["largeur"], self.nb_par_ligne, self.nb_par_colonne)     
        
        c.setDash(1,0)
        c.setStrokeColor(colors.gray)
        i = 0
        
        for row in data.iterrows():
            if i > 0 and i % self.nb_par_page == 0:
                c.showPage()
                # Lignes exterieures 
                self.dessiner_grille(c, self.etiquette.dimensions["hauteur"], self.etiquette.dimensions["largeur"], self.nb_par_ligne, self.nb_par_colonne)

            col = i % self.nb_par_ligne
            lig = (i % self.nb_par_page) // self.nb_par_ligne

            x = self.marge_externe + col * self.etiquette.dimensions["largeur"]
            y = self.hauteur_page - self.marge_externe - (lig + 1) * self.etiquette.dimensions["hauteur"]
           

            # Déclare Hauteur (du bas au haut)
            h_code_bar = self.etiquette.dimensions["h_code_bar"]
            y_produit = y + h_code_bar + (self.etiquette.dimensions["h_section_code"] - h_code_bar)/2
            y_ligne_bas = y + self.etiquette.dimensions["h_section_code"]
            if(variante):
                y_prix = y_ligne_bas + self.etiquette.dimensions["h_section_prix"]/2
                y_ligne_haut = y_ligne_bas + self.etiquette.dimensions["h_section_prix"]
                h_desc = y_ligne_haut + self.etiquette.dimensions["h_section_desc"]/2
            else:    
                h_desc = y_ligne_bas + self.etiquette.dimensions["h_section_desc"]/2
                y_ligne_haut = y_ligne_bas + self.etiquette.dimensions["h_section_desc"]
                y_prix = y_ligne_haut + self.etiquette.dimensions["h_section_prix"]/2

            # Prix (très gros)
            p_prix = Paragraph(f"{row[1].Coûtant:.2f} $", self.etiquette.styles["style_prix"])
            p_prix.wrapOn(c, self.etiquette.dimensions["largeur"] , y_prix)
            p_prix.drawOn(c, x, y_prix)
            
            # Ligne haut
            c.setDash(1,0)
            c.setStrokeColor(colors.gray)
            c.line(x, y_ligne_haut, x+self.etiquette.dimensions["largeur"], y_ligne_haut)

            # Description
            p_desc = Paragraph(str(row[1].Description), self.etiquette.styles["style_description"])
            p_desc.wrapOn(c, self.etiquette.dimensions["largeur"] - self.etiquette.dimensions["marge_interne_x"] * 2, (h_desc - 2 * self.etiquette.dimensions["marge_interne_y"]) * 3/4 )
            # S'assure si l'self.etiquette a besoin d'ecofrais
            if not np.isnan(row[1].Ecofrais):
                combined_string = "Inclus " + str(row[1].Ecofrais) + "$ d'écofrais"
                pEf = Paragraph(combined_string, self.etiquette.styles["style_description"])
                pEf.wrapOn(c, self.etiquette.dimensions["largeur"] - self.etiquette.dimensions["marge_interne_x"] * 2, 20 * mm)
                # Change la hauteur de la description pour la garder centré
                h_desc -= pEf.height/2
                # Dessine les ecofrais
                pEf.drawOn(c, x + self.etiquette.dimensions["marge_interne_x"], h_desc + p_desc.height/2)
            # Dessine la description
            p_desc.drawOn(c, x + self.etiquette.dimensions["marge_interne_x"], h_desc - p_desc.height/2)

            # Ligne bas
            c.line(x, y_ligne_bas, x + self.etiquette.dimensions["largeur"], y_ligne_bas)

            # Code du produit
            p_code = Paragraph(str(row[0]),self.etiquette.styles["style_code"])
            h = self.etiquette.dimensions["h_section_code"] - h_code_bar - self.etiquette.dimensions["marge_interne_y"] * 2
            w = self.etiquette.dimensions["largeur"] - self.etiquette.dimensions["marge_interne_x"] * 2
            # S'assure que le code du produit reste dans le frame
            framed_code = KeepInFrame(w, h, [p_code], mode='shrink')
            framed_code.wrapOn(c, w, h)
            framed_code.drawOn(c, x + self.etiquette.dimensions["marge_interne_x"], y_produit)

            # Code-barres
            if pd.notna(row[0]):
                barcode = code128.Code128(str(row[0]), barHeight= h_code_bar, humanReadable=False)
                barcode.drawOn(c, x + (self.etiquette.dimensions["largeur"] - barcode.width) / 2, y + 1)
            i += 1
        pass

    def generer_pdf_etiquettes(self, data, nom_fichier_pdf="etiquettes.pdf", variante = False, type_etiquette= "petite_etiquette"):
        pdf_path = f"{nom_fichier_pdf}"# Marges et dimensions
        c = canvas.Canvas(pdf_path, pagesize=(self.largeur_page, self.hauteur_page))
        self.etiquette = Etiquette(type_etiquette)

        self.nb_par_ligne = int((self.largeur_page - 2 * self.marge_externe) / self.etiquette.dimensions["largeur"])
        self.nb_par_colonne = int((self.hauteur_page - 2 * self.marge_externe) / self.etiquette.dimensions["hauteur"]) # Ajustable selon hauteur
        self.nb_par_page = self.nb_par_ligne * self.nb_par_colonne
        # Lignes exterieures 
        self.dessiner_grille(c, self.etiquette.dimensions["hauteur"], self.etiquette.dimensions["largeur"])     
        # Regarde quel etiquettes il faut enregistrer
        self.generer_petites_etiquettes(c, data, variante)

        # Création du pdf
        c.save()
        print(f"✅ PDF enregistré à : {nom_fichier_pdf}")

    def generer_petites_etiquettes(self, c, data, variante = False):
        

        
        c.setDash(1,0)
        c.setStrokeColor(colors.gray)
        i = 0
        
        for row in data.iterrows():
            if i > 0 and i % self.nb_par_page == 0:
                c.showPage()
                # Lignes exterieures 
                self.dessiner_grille(c, self.etiquette.dimensions["hauteur"], self.etiquette.dimensions["largeur"])

            col = i % self.nb_par_ligne
            lig = (i % self.nb_par_page) // self.nb_par_ligne

            x = self.marge_externe + col * self.etiquette.dimensions["largeur"]
            y = self.hauteur_page - self.marge_externe - (lig + 1) * self.etiquette.dimensions["hauteur"]
            y_code_bar = self.etiquette.dimensions["h_code_bar"]
            # Déclare Hauteur (du bas au haut)
            
            y_produit = y + y_code_bar + (self.etiquette.dimensions["h_section_code"] - y_code_bar)/2
            y_ligne_bas = y + self.etiquette.dimensions["h_section_code"]
            if(variante):
                y_prix = y_ligne_bas + self.etiquette.dimensions["h_section_prix"]/2
                y_ligne_haut = y_ligne_bas + self.etiquette.dimensions["h_section_prix"]
                h_desc = y_ligne_haut + self.etiquette.dimensions["h_section_desc"]/2
            else:    
                h_desc = y_ligne_bas + self.etiquette.dimensions["h_section_desc"]/2
                y_ligne_haut = y_ligne_bas + self.etiquette.dimensions["h_section_desc"]
                y_prix = y_ligne_haut + self.etiquette.dimensions["h_section_prix"]/2

            # Prix (très gros)
            #c.setFont("Helvetica-Bold", 30)
            #c.drawCentredString(x + largeur_etiquette / 2, h_prix, f"{row[1].Coûtant:.2f} $")
            p_prix = Paragraph(f"{row[1].Coûtant:.2f} $", self.etiquette.styles["style_prix"])
            p_prix.wrapOn(c, self.etiquette.dimensions["largeur"] , y_prix)
            p_prix.drawOn(c, x, y_prix)
            
            # Ligne haut
            c.setDash(1,0)
            c.setStrokeColor(colors.gray)
            c.line(x, y_ligne_haut, x+self.etiquette.dimensions["largeur"], y_ligne_haut)

            # Description
            p_desc = Paragraph(str(row[1].Description), self.etiquette.styles["style_description"])
            p_desc.wrapOn(c, self.etiquette.dimensions["largeur"] - self.etiquette.dimensions["marge_interne_x"] * 2, (h_desc - 2 * self.etiquette.dimensions["marge_interne_y"]) * 3/4 )
            # S'assure si l'self.etiquette a besoin d'ecofrais
            if not np.isnan(row[1].Ecofrais):
                combined_string = "Inclus " + str(row[1].Ecofrais) + "$ d'écofrais"
                pEf = Paragraph(combined_string, self.etiquette.styles["style_description"])
                pEf.wrapOn(c, self.etiquette.dimensions["largeur"] - self.etiquette.dimensions["marge_interne_x"] * 2, 20 * mm)
                # Change la hauteur de la description pour la garder centré
                h_desc -= pEf.height/2
                # Dessine les ecofrais
                pEf.drawOn(c, x + self.etiquette.dimensions["marge_interne_x"], h_desc + p_desc.height/2)
            # Dessine la description
            p_desc.drawOn(c, x + self.etiquette.dimensions["marge_interne_x"], h_desc - p_desc.height/2)

            # Ligne bas
            c.line(x, y_ligne_bas, x + self.etiquette.dimensions["largeur"], y_ligne_bas)

            # Code du produit
            p_code = Paragraph(str(row[0]),self.etiquette.styles["style_code"])
            h = self.etiquette.dimensions["h_section_code"] - y_code_bar - self.etiquette.dimensions["marge_interne_y"] * 2
            w = self.etiquette.dimensions["largeur"] - self.etiquette.dimensions["marge_interne_x"] * 2
            # S'assure que le code du produit reste dans le frame
            framed_code = KeepInFrame(w, h, [p_code], mode='shrink')
            framed_code.wrapOn(c, w, h)
            framed_code.drawOn(c, x + self.etiquette.dimensions["marge_interne_x"], y_produit)

            # Code-barres
            if pd.notna(row[0]):
                barcode = code128.Code128(str(row[0]), barHeight= y_code_bar, humanReadable=False)
                barcode.drawOn(c, x + (self.etiquette.dimensions["largeur"] - barcode.width) / 2, y + 1)
            i += 1
            
    def paragraphe_ajuste_produit(self, text, width):
        # Démarrer avec la taille de police souhaitée
        font_size = self.style_code.fontSize
        height_max = 12

        # On commence avec une copie du style
        while font_size >= 4:
            dynamic_style = ParagraphStyle(
                name='ProduitDynamic',
                parent=self.style_code,
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
    g.generer_pdf_etiquettes(df, "etiquettes.pdf", True)