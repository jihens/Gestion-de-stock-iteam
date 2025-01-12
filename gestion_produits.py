from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import pymysql
from fpdf import FPDF
import random
from PIL import Image, ImageTk  # Pour afficher le logo

def gestion_produits_ui():
    window = Toplevel()
    window.title("Gestion des Produits")
    window.geometry("1000x700")
    window.configure(bg="#F0F0F0")

    numeric = '123456789'
    Alpha = 'ABCDEFGHIGKLMNYZWX'

    # Ajouter le logo
    logo_frame = Frame(window, bg="#020659")
    logo_frame.pack(fill="x")

    title_label = Label(logo_frame, text="Gestion des Produits", font=("Arial", 20, "bold"), fg="white", bg="#020659")
    title_label.pack(side="left", padx=20)

    # Connexion à la base de données
    def connection():
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='GestionDeStockPython',
            port=3306    
        )
        return conn

    # Fonction pour lire les données
    def read():
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT `Code_prod`, `Nom_prod`, `Description`, `Qantite`, `Prix_unit` FROM `produit` ORDER BY `Code_prod` DESC"
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results

    # Actualiser la table
    def refresh_table(data=None):
        for row in my_tree.get_children():
            my_tree.delete(row)
        if data is None:
            data = read()
        for array in data:
            my_tree.insert("", "end", values=array, tag="orow")
        my_tree.tag_configure('orow', background="#EEEEEE")

    # Exporter en PDF
    def export_pdf():
        try:
            data = read()
            if not data:
                messagebox.showwarning("Exportation PDF", "Aucun produit à exporter.")
                return

            file_path = asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf")],
                title="Enregistrer sous"
            )
            if not file_path:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Liste des Produits", ln=True, align='C')
            pdf.ln(10)

            headers = ["Code Produit", "Nom", "Description", "Quantité", "Prix"]
            for header in headers:
                pdf.cell(40, 10, header, 1)
            pdf.ln(10)

            for row in data:
                pdf.cell(40, 10, str(row[0]), 1)
                pdf.cell(60, 10, str(row[1]), 1)
                pdf.cell(70, 10, str(row[2]), 1)
                pdf.cell(20, 10, str(row[3]), 1)
                pdf.cell(20, 10, str(row[4]), 1)
                pdf.ln(10)

            pdf.output(file_path)
            messagebox.showinfo("Exportation PDF", "Produits exportés avec succès en PDF.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation en PDF : {e}")

    # Génération aléatoire d'un ID produit
    def generate_rand():
        item_id = ''
        for i in range(3):
            rand_no = random.randrange(0, len(numeric))
            item_id += numeric[rand_no]
        rand_no = random.randrange(0, len(Alpha))
        item_id += '-' + Alpha[rand_no]
        set_placeholder(item_id, 0)

    def set_placeholder(word, num):
        if 0 <= num < len(placeholderArray):
            placeholderArray[num].set(word)

    def save():
        conn = connection()
        cursor = conn.cursor()

        Code_prod = placeholderArray[0].get().strip()
        Nom_prod = placeholderArray[1].get().strip()
        Description = placeholderArray[2].get().strip()
        Qantite = placeholderArray[3].get().strip()
        Prix_unit = placeholderArray[4].get().strip()

        if not (Code_prod and Nom_prod and Description and Qantite and Prix_unit):
            messagebox.showwarning("", "Veuillez remplir tous les champs.")
            return

        try:
            cursor.execute("INSERT INTO `produit`(`Code_prod`, `Nom_prod`, `Description`, `Qantite`, `Prix_unit`) VALUES (%s, %s, %s, %s, %s)",
                           (Code_prod, Nom_prod, Description, Qantite, Prix_unit))
            conn.commit()
            messagebox.showinfo("", "Produit enregistré avec succès.")
        except Exception as e:
            messagebox.showerror("", f"Erreur lors de l'enregistrement : {e}")
        finally:
            conn.close()
            refresh_table()

    def update():
        conn = connection()
        cursor = conn.cursor()

        Code_prod = placeholderArray[0].get().strip()
        Nom_prod = placeholderArray[1].get().strip()
        Description = placeholderArray[2].get().strip()
        Qantite = placeholderArray[3].get().strip()
        Prix_unit = placeholderArray[4].get().strip()

        if not (Code_prod and Nom_prod and Description and Qantite and Prix_unit):
            messagebox.showwarning("", "Veuillez remplir tous les champs.")
            return

        try:
            cursor.execute("UPDATE `produit` SET `Nom_prod`=%s, `Description`=%s, `Qantite`=%s, `Prix_unit`=%s WHERE `Code_prod`=%s",
                           (Nom_prod, Description, Qantite, Prix_unit, Code_prod))
            conn.commit()
            messagebox.showinfo("", "Produit mis à jour avec succès.")
        except Exception as e:
            messagebox.showerror("", f"Erreur lors de la mise à jour : {e}")
        finally:
            conn.close()
            refresh_table()

    def delete():
        conn = connection()
        cursor = conn.cursor()

        Code_prod = placeholderArray[0].get().strip()

        if not Code_prod:
            messagebox.showwarning("", "Veuillez sélectionner un produit à supprimer.")
            return

        try:
            cursor.execute("DELETE FROM `produit` WHERE `Code_prod`=%s", (Code_prod,))
            conn.commit()
            messagebox.showinfo("", "Produit supprimé avec succès.")
        except Exception as e:
            messagebox.showerror("", f"Erreur lors de la suppression : {e}")
        finally:
            conn.close()
            refresh_table()

    def clear():
        for placeholder in placeholderArray:
            placeholder.set("")
        refresh_table()

    def search():
        search_text = search_var.get().strip()
        if not search_text:
            refresh_table()
            return

        data = read()
        filtered_data = [row for row in data if search_text.lower() in str(row).lower()]
        refresh_table(filtered_data)

    placeholderArray = [StringVar() for _ in range(5)]

    frame_buttons = Frame(window, bg="#8C182D", padx=10, pady=10)
    frame_buttons.pack(fill="x", pady=10)

    btnColor = "#8C0303"
    Button(frame_buttons, text="Ajouter", width=12, bg=btnColor, fg="white", command=save).grid(row=0, column=0, padx=5, pady=5)
    Button(frame_buttons, text="Modifier", width=12, bg=btnColor, fg="white", command=update).grid(row=0, column=1, padx=5, pady=5)
    Button(frame_buttons, text="Supprimer", width=12, bg=btnColor, fg="white", command=delete).grid(row=0, column=2, padx=5, pady=5)
    Button(frame_buttons, text="Exporter PDF", width=12, bg=btnColor, fg="white", command=export_pdf).grid(row=0, column=3, padx=5, pady=5)
    Button(frame_buttons, text="Rafraîchir", width=12, bg=btnColor, fg="white", command=refresh_table).grid(row=0, column=4, padx=5, pady=5)

    search_var = StringVar()
    Label(frame_buttons, text="Recherche :", bg="#8C182D", fg="white").grid(row=0, column=5, padx=5, pady=5)
    Entry(frame_buttons, textvariable=search_var, width=20).grid(row=0, column=6, padx=5, pady=5)
    Button(frame_buttons, text="Chercher", bg=btnColor, fg="white", command=search).grid(row=0, column=7, padx=5, pady=5)

    entries_frame = LabelFrame(window, text="Formulaire", padx=10, pady=10)
    entries_frame.pack(fill="x", padx=20, pady=10)

    labels = ["Code", "Nom", "Description", "Quantité", "Prix"]
    for i, label_text in enumerate(labels):
        Label(entries_frame, text=label_text, width=15).grid(row=i, column=0, padx=5, pady=5)
        Entry(entries_frame, width=50, textvariable=placeholderArray[i]).grid(row=i, column=1, padx=5, pady=5)

    Button(entries_frame, text="Générer Code Produit", bg=btnColor, fg="white", command=generate_rand).grid(row=0, column=2, padx=5, pady=5)

    style = ttk.Style()
    style.configure("Treeview", rowheight=25)

    my_tree = ttk.Treeview(window, columns=("Code_prod", "Nom_prod", "Description", "Qantite", "Prix_unit"), show="headings", height=15)
    for col in my_tree["columns"]:
        my_tree.column(col, anchor=W, width=150)
        my_tree.heading(col, text=col)

    my_tree.pack(pady=20, padx=20, fill="both", expand=True)

    refresh_table()

    window.resizable(False, False)
    window.mainloop()
