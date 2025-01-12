from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import csv

def connection():
    # Connection to the database
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='GestionDeStockPython',
        port=3306
    )

def gestion_commandes_ui():
    window = Toplevel()
    window.title("Gestion des Commandes")
    window.geometry("1000x700")
    window.configure(bg="#F0F0F0")

    # Add the logo frame (same style as gestion_produits)
    logo_frame = Frame(window, bg="#020659")
    logo_frame.pack(fill="x")

    title_label = Label(logo_frame, text="Gestion des Commandes", font=("Arial", 20, "bold"), fg="white", bg="#020659")
    title_label.pack(side="left", padx=20)
    
    

     # Fetch product codes from the database
    def get_product_codes():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Code_prod FROM produit")
        codes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return codes

    # Command table refresh function
    def refresh_command_table():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM commande")
        rows = cursor.fetchall()
        conn.close()

        for row in tree_commandes.get_children():
            tree_commandes.delete(row)
        for cmd in rows:
            tree_commandes.insert("", "end", values=cmd, tag="cmd_row")
        tree_commandes.tag_configure('cmd_row', background="#EEEEEE")

    def ajouter_commande():
        code_cmd = placeholderArrayCmd[0].get()
        code_prod = placeholderArrayCmd[1].get()
        quantite_cmd = placeholderArrayCmd[2].get()

        if code_cmd and code_prod and quantite_cmd:
            conn = connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT Qantite FROM produit WHERE Code_prod = %s", (code_prod,))
                produit = cursor.fetchone()

                if produit:
                    quantite_actuelle = produit[0]
                    if int(quantite_cmd) <= quantite_actuelle:
                        cursor.execute("INSERT INTO commande (Code_cmd, Code_prod, Quantite_cmd) VALUES (%s, %s, %s)",
                                    (code_cmd, code_prod, quantite_cmd))
                        nouvelle_quantite = quantite_actuelle - int(quantite_cmd)
                        cursor.execute("UPDATE produit SET Qantite = %s WHERE Code_prod = %s",
                                    (nouvelle_quantite, code_prod))
                        conn.commit()
                        messagebox.showinfo("Succès", "Commande ajoutée avec succès et stock mis à jour.")
                    else:
                        messagebox.showerror("Erreur", "Quantité insuffisante en stock.")
                else:
                    messagebox.showerror("Erreur", "Produit introuvable.")
            except pymysql.Error as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
            finally:
                conn.close()
            refresh_command_table()
            clear_command_form()
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

    def modifier_commande():
        selected_item = tree_commandes.focus()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une commande à modifier")
            return

        values = tree_commandes.item(selected_item, 'values')
        code_cmd = values[0]
        new_code_prod = placeholderArrayCmd[1].get()
        new_quantite_cmd = placeholderArrayCmd[2].get()

        if new_code_prod and new_quantite_cmd:
            conn = connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE commande SET Code_prod = %s, Quantite_cmd = %s WHERE Code_cmd = %s",
                               (new_code_prod, new_quantite_cmd, code_cmd))
                conn.commit()
                messagebox.showinfo("Succès", "Commande modifiée avec succès")
            except pymysql.Error as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
            finally:
                conn.close()
            refresh_command_table()
            clear_command_form()
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

    def supprimer_commande():
        selected_item = tree_commandes.focus()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une commande à supprimer")
            return

        values = tree_commandes.item(selected_item, 'values')
        code_cmd = values[0]

        conn = connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM commande WHERE Code_cmd = %s", (code_cmd,))
            conn.commit()
            messagebox.showinfo("Succès", "Commande supprimée avec succès")
        except pymysql.Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
        finally:
            conn.close()
        refresh_command_table()

    def afficher_statistiques():
        conn = connection()
        cursor = conn.cursor()

        # Query to get product names and the total quantity ordered
        cursor.execute("""
            SELECT p.Nom_prod, SUM(c.Quantite_cmd) AS Total
            FROM commande c
            JOIN produit p ON c.Code_prod = p.Code_prod
            GROUP BY p.Nom_prod
        """)
        
        data = cursor.fetchall()
        conn.close()

        # Extract product names and quantities
        produits = [row[0] for row in data]  # Product names
        quantites = [row[1] for row in data]  # Total quantities ordered

        # Display with seaborn and matplotlib
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=produits, y=quantites, palette="coolwarm")

        plt.xlabel("Nom du Produit", fontsize=14)
        plt.ylabel("Quantité Commandée", fontsize=14)
        plt.title("Produits les plus commandés", fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def afficher_historique():
        historique_root = Toplevel(window)  # Using the window as the parent window
        historique_root.title("Historique des Commandes")
        historique_root.geometry("700x500")

        tree_historique = ttk.Treeview(historique_root, columns=("Code Commande", "Code Produit", "Quantité"), show="headings")
        tree_historique.heading("Code Commande", text="Code Commande")
        tree_historique.heading("Code Produit", text="Code Produit")
        tree_historique.heading("Quantité", text="Quantité")

        tree_historique.column("Code Commande", anchor=W, width=150)
        tree_historique.column("Code Produit", anchor=W, width=150)
        tree_historique.column("Quantité", anchor=W, width=150)

        tree_historique.pack(fill=BOTH, expand=True, padx=10, pady=10)

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM commande")
        rows = cursor.fetchall()
        conn.close()

        for cmd in rows:
            tree_historique.insert("", "end", values=cmd)

        def exporter_csv():
            with open("historique_commandes.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Code Commande", "Code Produit", "Quantité"])
                writer.writerows(rows)
            messagebox.showinfo("Succès", "Historique exporté en CSV avec succès")

        Button(historique_root, text="Exporter en CSV", command=exporter_csv, bg="#196E78", fg="white", width=15).pack(pady=10)

    def clear_command_form():
        placeholderArrayCmd[0].set("")
        placeholderArrayCmd[1].set("")  # Reset Combobox
        placeholderArrayCmd[2].set("")

    # Button layout with standard ttk styling
    frame_buttons_commandes = Frame(window, bg="#8C182D", padx=10, pady=10)
    frame_buttons_commandes.pack(fill="x", pady=10)

    Button(frame_buttons_commandes, text="Ajouter", width=12, command=ajouter_commande, bg="#8C182D", fg="white").grid(row=0, column=0, padx=5, pady=5)
    Button(frame_buttons_commandes, text="Modifier", width=12, command=modifier_commande, bg="#8C182D", fg="white").grid(row=0, column=1, padx=5, pady=5)
    Button(frame_buttons_commandes, text="Supprimer", width=12, command=supprimer_commande, bg="#8C182D", fg="white").grid(row=0, column=2, padx=5, pady=5)
    Button(frame_buttons_commandes, text="Statistiques", width=12, command=afficher_statistiques, bg="#8C182D", fg="white").grid(row=0, column=3, padx=5, pady=5)
    Button(frame_buttons_commandes, text="Historique", width=12, command=afficher_historique, bg="#8C182D", fg="white").grid(row=0, column=4, padx=5, pady=5)


    # Add form for entering command details
    frame_form_commandes = LabelFrame(window, text="Détails de la commande", padx=20, pady=20)
    frame_form_commandes.pack(fill="x", padx=20, pady=10)

    labels = ["Code Commande", "Code Produit", "Quantité"]
    placeholderArrayCmd = [StringVar(), StringVar(), StringVar()]

    for i, label in enumerate(labels):
        Label(frame_form_commandes, text=label, width=15).grid(row=i, column=0, padx=5, pady=5)

        if label == "Code Produit":
            # Replace Entry with Combobox for product codes
            product_codes = get_product_codes()
            combobox = ttk.Combobox(frame_form_commandes, textvariable=placeholderArrayCmd[1], values=product_codes, state="readonly", width=47)
            combobox.grid(row=i, column=1, padx=5, pady=5)
        else:
            Entry(frame_form_commandes, width=50, textvariable=placeholderArrayCmd[i]).grid(row=i, column=1, padx=5, pady=5)

    # Treeview for showing commands
    frame_table_commandes = Frame(window, padx=10, pady=10)
    frame_table_commandes.pack(fill=BOTH, expand=True, padx=20, pady=20)

    tree_commandes = ttk.Treeview(frame_table_commandes, columns=("Code Commande", "Code Produit", "Quantité"), show="headings")
    tree_commandes.heading("Code Commande", text="Code Commande")
    tree_commandes.heading("Code Produit", text="Code Produit")
    tree_commandes.heading("Quantité", text="Quantité")

    tree_commandes.column("Code Commande", anchor=W, width=150)
    tree_commandes.column("Code Produit", anchor=W, width=150)
    tree_commandes.column("Quantité", anchor=W, width=150)

    tree_commandes.pack(fill=BOTH, expand=True)

    refresh_command_table()

    window.mainloop()

# Call the function to run the UI
# gestion_commandes_ui()  # Uncomment this line to run the function
