# ==========================================
# GESTION STOCK PNEUS - VERSION MAC / APPLE
# Compatible macOS (Apple Silicon M1/M2/M3)
# Python 3.12+
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os

FICHIER_STOCK = "stock_pneus.json"
FICHIER_MOUVEMENTS = "mouvements_stock.json"


class GestionPneus:

    def __init__(self, root):

        self.root = root
        self.root.title("Gestion Stock Pneus")
        self.root.geometry("1400x850")
        self.root.configure(bg="#ECECEC")

        self.stock = self.charger_json(FICHIER_STOCK)
        self.mouvements = self.charger_json(FICHIER_MOUVEMENTS)

        self.creer_interface()

    # =========================================================
    # CHARGEMENT JSON
    # =========================================================

    def charger_json(self, fichier):

        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}

        return {}

    # =========================================================
    # SAUVEGARDE
    # =========================================================

    def sauvegarder_stock(self):

        with open(FICHIER_STOCK, "w", encoding="utf-8") as f:
            json.dump(self.stock, f, indent=4, ensure_ascii=False)

    def sauvegarder_mouvements(self):

        with open(FICHIER_MOUVEMENTS, "w", encoding="utf-8") as f:
            json.dump(self.mouvements, f, indent=4, ensure_ascii=False)

    # =========================================================
    # INTERFACE
    # =========================================================

    def creer_interface(self):

        # ==========================
        # TITRE
        # ==========================

        titre = tk.Label(
            self.root,
            text="GESTION STOCK PNEUS",
            font=("Helvetica", 24, "bold"),
            bg="#ECECEC",
            fg="#222"
        )

        titre.pack(pady=15)

        # ==========================
        # FRAME AJOUT
        # ==========================

        frame = tk.LabelFrame(
            self.root,
            text="Entrée Stock",
            padx=15,
            pady=15,
            bg="#ECECEC",
            font=("Helvetica", 12, "bold")
        )

        frame.pack(fill="x", padx=20, pady=10)

        # MARQUE

        tk.Label(frame, text="Marque", bg="#ECECEC").grid(row=0, column=0)

        self.entree_marque = tk.Entry(frame, width=20)
        self.entree_marque.grid(row=0, column=1, padx=5)

        # DIMENSION

        tk.Label(frame, text="Dimension", bg="#ECECEC").grid(row=0, column=2)

        self.entree_dimension = tk.Entry(frame, width=20)
        self.entree_dimension.grid(row=0, column=3, padx=5)

        # TYPE

        tk.Label(frame, text="Type", bg="#ECECEC").grid(row=1, column=0)

        self.combo_type = ttk.Combobox(
            frame,
            width=35,
            state="readonly",
            values=[
                "Été - Neuf",
                "Été - Occasion",
                "Hiver - Neuf",
                "Hiver - Occasion",
                "4 Saisons - Neuf",
                "4 Saisons - Occasion",
                "Runflat - Neuf",
                "Runflat - Occasion",
                "SUV - Neuf",
                "SUV - Occasion",
                "Moto - Neuf",
                "Moto - Occasion",
                "Poids Lourd - Neuf",
                "Poids Lourd - Occasion",
                "Autre"
            ]
        )

        self.combo_type.grid(row=1, column=1, padx=5)
        self.combo_type.current(0)

        # QUANTITE

        tk.Label(frame, text="Quantité", bg="#ECECEC").grid(row=1, column=2)

        self.entree_qty = tk.Spinbox(frame, from_=1, to=10000, width=10)
        self.entree_qty.grid(row=1, column=3)

        # PRIX

        tk.Label(frame, text="Prix (€)", bg="#ECECEC").grid(row=1, column=4)

        self.entree_prix = tk.Entry(frame, width=12)
        self.entree_prix.grid(row=1, column=5)

        # BOUTON AJOUT

        btn_add = tk.Button(
            frame,
            text="Ajouter",
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 11, "bold"),
            command=self.ajouter_pneu
        )

        btn_add.grid(row=1, column=6, padx=15)

        # ==========================
        # RECHERCHE
        # ==========================

        frame_search = tk.Frame(self.root, bg="#ECECEC")
        frame_search.pack(fill="x", padx=20)

        tk.Label(
            frame_search,
            text="Recherche :",
            bg="#ECECEC"
        ).pack(side="left")

        self.entree_recherche = tk.Entry(frame_search, width=40)
        self.entree_recherche.pack(side="left", padx=10)

        self.entree_recherche.bind(
            "<KeyRelease>",
            lambda e: self.rafraichir_tableau()
        )

        # ==========================
        # TABLEAU STOCK
        # ==========================

        columns = (
            "Marque",
            "Dimension",
            "Type",
            "Quantité",
            "Prix",
            "Valeur"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:

            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # ==========================
        # BOUTONS
        # ==========================

        frame_btn = tk.Frame(self.root, bg="#ECECEC")
        frame_btn.pack(pady=10)

        tk.Button(
            frame_btn,
            text="Sortir / Vente",
            bg="#FF9800",
            fg="white",
            command=self.sortir_pneu
        ).pack(side="left", padx=10)

        tk.Button(
            frame_btn,
            text="Supprimer",
            bg="#F44336",
            fg="white",
            command=self.supprimer_pneu
        ).pack(side="left", padx=10)

        tk.Button(
            frame_btn,
            text="Historique",
            bg="#2196F3",
            fg="white",
            command=self.afficher_historique
        ).pack(side="left", padx=10)

        self.rafraichir_tableau()

    # =========================================================
    # AJOUT PNEU
    # =========================================================

    def ajouter_pneu(self):

        marque = self.entree_marque.get().strip().upper()
        dimension = self.entree_dimension.get().strip().upper()
        type_pneu = self.combo_type.get()

        try:
            qty = int(self.entree_qty.get())
            prix = float(self.entree_prix.get())

        except:
            messagebox.showerror("Erreur", "Valeur invalide")
            return

        if not marque or not dimension:
            messagebox.showwarning("Erreur", "Champs obligatoires")
            return

        key = f"{marque}-{dimension}-{type_pneu}"

        if key in self.stock:

            self.stock[key]["quantite"] += qty

        else:

            self.stock[key] = {
                "marque": marque,
                "dimension": dimension,
                "type": type_pneu,
                "quantite": qty,
                "prix": prix
            }

        # ==========================
        # HISTORIQUE
        # ==========================

        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.mouvements[date_now] = {
            "action": "ENTREE",
            "marque": marque,
            "dimension": dimension,
            "type": type_pneu,
            "quantite": qty,
            "prix": prix
        }

        self.sauvegarder_stock()
        self.sauvegarder_mouvements()

        self.rafraichir_tableau()

        messagebox.showinfo(
            "Succès",
            f"{qty} pneu(x) ajouté(s)"
        )

    # =========================================================
    # SORTIE PNEU
    # =========================================================

    def sortir_pneu(self):

        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Attention",
                "Sélectionnez un pneu"
            )
            return

        values = self.tree.item(selection[0], "values")

        marque = values[0]
        dimension = values[1]
        type_p = values[2]

        key = f"{marque}-{dimension}-{type_p}"

        qty_sortie = simpledialog.askinteger(
            "Sortie",
            f"Quantité à sortir pour {marque} ?",
            minvalue=1
        )

        if not qty_sortie:
            return

        if self.stock[key]["quantite"] >= qty_sortie:

            self.stock[key]["quantite"] -= qty_sortie

            if self.stock[key]["quantite"] <= 0:
                del self.stock[key]

            # ==========================
            # HISTORIQUE
            # ==========================

            date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            self.mouvements[date_now] = {
                "action": "SORTIE",
                "marque": marque,
                "dimension": dimension,
                "type": type_p,
                "quantite": qty_sortie
            }

            self.sauvegarder_stock()
            self.sauvegarder_mouvements()

            self.rafraichir_tableau()

            messagebox.showinfo(
                "Succès",
                f"{qty_sortie} pneu(x) sorti(s)"
            )

        else:

            messagebox.showerror(
                "Erreur",
                "Stock insuffisant"
            )

    # =========================================================
    # SUPPRESSION
    # =========================================================

    def supprimer_pneu(self):

        selection = self.tree.selection()

        if not selection:
            return

        values = self.tree.item(selection[0], "values")

        key = f"{values[0]}-{values[1]}-{values[2]}"

        if messagebox.askyesno(
                "Confirmation",
                "Supprimer ce pneu ?"
        ):

            del self.stock[key]

            self.sauvegarder_stock()

            self.rafraichir_tableau()

    # =========================================================
    # TABLEAU
    # =========================================================

    def rafraichir_tableau(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        recherche = self.entree_recherche.get().upper()

        for key, pneu in self.stock.items():

            texte = f"{pneu['marque']} {pneu['dimension']} {pneu['type']}"

            if recherche and recherche not in texte.upper():
                continue

            valeur = pneu["quantite"] * pneu["prix"]

            tag = "normal"

            if pneu["quantite"] <= 4:
                tag = "faible"

            self.tree.insert(
                "",
                "end",
                values=(
                    pneu["marque"],
                    pneu["dimension"],
                    pneu["type"],
                    pneu["quantite"],
                    f"{pneu['prix']:.2f} €",
                    f"{valeur:.2f} €"
                ),
                tags=(tag,)
            )

        self.tree.tag_configure(
            "faible",
            background="#FFD6D6"
        )

    # =========================================================
    # HISTORIQUE
    # =========================================================

    def afficher_historique(self):

        fenetre = tk.Toplevel(self.root)

        fenetre.title("Historique des mouvements")
        fenetre.geometry("1000x500")

        colonnes = (
            "Date",
            "Action",
            "Marque",
            "Dimension",
            "Type",
            "Quantité"
        )

        tree = ttk.Treeview(
            fenetre,
            columns=colonnes,
            show="headings"
        )

        for col in colonnes:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill="both", expand=True)

        for date, mouvement in self.mouvements.items():

            tree.insert(
                "",
                "end",
                values=(
                    date,
                    mouvement["action"],
                    mouvement["marque"],
                    mouvement["dimension"],
                    mouvement["type"],
                    mouvement["quantite"]
                )
            )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    app = GestionPneus(root)

    root.mainloop()