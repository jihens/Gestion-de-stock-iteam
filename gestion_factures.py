from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

def connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='GestionDeStockPython',
        port=3306
    )

def gestion_factures_ui():
    window = Toplevel()
    window.title("Gestion des Factures")
    window.geometry("1000x700")
    window.configure(bg="#F0F0F0")

    logo_frame = Frame(window, bg="#020659")
    logo_frame.pack(fill="x")

    title_label = Label(logo_frame, text="Gestion des Factures", font=("Arial", 20, "bold"), fg="white", bg="#020659")
    title_label.pack(side="left", padx=20)

    def refresh_invoice_table():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM factures")
        rows = cursor.fetchall()
        conn.close()

        for row in tree_factures.get_children():
            tree_factures.delete(row)
        for fact in rows:
            tree_factures.insert("", "end", values=fact, tag="fact_row")
        tree_factures.tag_configure('fact_row', background="#EEEEEE")

    def ajouter_facture():
        code_facture = placeholderArrayFacture[0].get()
        montant = placeholderArrayFacture[2].get()
        code_cmd = commande_combobox.get()

        if code_facture and montant and code_cmd:
            date_facture = datetime.now().strftime('%Y-%m-%d')
            conn = connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO factures (Code_facture, Date_facture, Montant) VALUES (%s, %s, %s)",
                               (code_facture, date_facture, montant))
                cursor.execute("INSERT INTO commande_facture (Code_facture, Code_cmd) VALUES (%s, %s)",
                               (code_facture, code_cmd))
                conn.commit()
                messagebox.showinfo("Succès", "Facture ajoutée avec succès")
            except pymysql.Error as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
            finally:
                conn.close()
            refresh_invoice_table()
            clear_facture_form()
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

    def modifier_facture():
        selected_item = tree_factures.focus()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à modifier")
            return

        values = tree_factures.item(selected_item, 'values')
        code_facture = values[0]
        new_montant = placeholderArrayFacture[2].get()

        if new_montant:
            conn = connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE factures SET Montant = %s WHERE Code_facture = %s",
                               (new_montant, code_facture))
                conn.commit()
                messagebox.showinfo("Succès", "Facture modifiée avec succès")
            except pymysql.Error as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
            finally:
                conn.close()
            refresh_invoice_table()
            clear_facture_form()
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

    def supprimer_facture():
        selected_item = tree_factures.focus()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à supprimer")
            return

        values = tree_factures.item(selected_item, 'values')
        code_facture = values[0]

        conn = connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM factures WHERE Code_facture = %s", (code_facture,))
            cursor.execute("DELETE FROM commande_facture WHERE Code_facture = %s", (code_facture,))
            conn.commit()
            messagebox.showinfo("Succès", "Facture supprimée avec succès")
        except pymysql.Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
        finally:
            conn.close()
        refresh_invoice_table()

    def afficher_commandes_facture():
        selected_item = tree_factures.focus()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture pour voir les commandes")
            return

        values = tree_factures.item(selected_item, 'values')
        code_facture = values[0]

        commandes_root = Toplevel(window)
        commandes_root.title(f"Commandes liées à la facture {code_facture}")
        commandes_root.geometry("600x400")

        tree_commandes_facture = ttk.Treeview(commandes_root, columns=("Code Commande", "Quantité"), show="headings")
        tree_commandes_facture.heading("Code Commande", text="Code Commande")
        tree_commandes_facture.heading("Quantité", text="Quantité")

        tree_commandes_facture.column("Code Commande", anchor=W, width=150)
        tree_commandes_facture.column("Quantité", anchor=W, width=150)

        tree_commandes_facture.pack(fill=BOTH, expand=True, padx=10, pady=10)

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.Code_cmd, c.Quantite_cmd
            FROM commande c
            JOIN commande_facture cf ON c.Code_cmd = cf.Code_cmd
            WHERE cf.Code_facture = %s
        """, (code_facture,))
        rows = cursor.fetchall()
        conn.close()

        for cmd in rows:
            tree_commandes_facture.insert("", "end", values=cmd)

    def clear_facture_form():
        for var in placeholderArrayFacture:
            var.set("")
        commande_combobox.set('')

    def generate_invoice_pdf():
        selected_item = tree_factures.focus()
        if selected_item:
            selected_invoice_data = tree_factures.item(selected_item, "values")
            # Passer selected_invoice_data à la fonction PDF
            pdf_filename = f"facture_{selected_invoice_data[0]}.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica-Bold", 16)
            c.drawString(200, height - 50, "Facture")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 100, f"Code Facture: {selected_invoice_data[0]}")
            c.drawString(50, height - 120, f"Date Facture: {selected_invoice_data[1]}")
            c.drawString(50, height - 140, f"Montant: {selected_invoice_data[2]}")
            c.save()
            messagebox.showinfo("PDF généré", f"Le PDF de la facture a été généré : {pdf_filename}")

    def exporter_facture_pdf():
        pdf_filename = "factures_list.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "Liste des Factures")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 100, "Code Facture")
        c.drawString(200, height - 100, "Date Facture")
        c.drawString(350, height - 100, "Montant")
        y_position = height - 120
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Code_facture, Date_facture, Montant FROM factures")
        rows = cursor.fetchall()
        conn.close()

        c.setFont("Helvetica", 12)
        for row in rows:
            c.drawString(50, y_position, row[0])
            c.drawString(200, y_position, str(row[1]))  # Convertir la date en chaîne
            c.drawString(350, y_position, str(row[2]))
            y_position -= 20

        c.save()
        messagebox.showinfo("PDF Exporté", f"Le PDF des factures a été exporté : {pdf_filename}")

    # Buttons for facture actions
    frame_buttons_factures = Frame(window, bg="#8C182D", padx=10, pady=10)
    frame_buttons_factures.pack(fill="x", pady=10)

    Button(frame_buttons_factures, text="Ajouter", width=12, command=ajouter_facture, bg="#8C182D", fg="white").grid(row=0, column=0, padx=5, pady=5)
    Button(frame_buttons_factures, text="Modifier", width=12, command=modifier_facture, bg="#8C182D", fg="white").grid(row=0, column=1, padx=5, pady=5)
    Button(frame_buttons_factures, text="Supprimer", width=12, command=supprimer_facture, bg="#8C182D", fg="white").grid(row=0, column=2, padx=5, pady=5)
    Button(frame_buttons_factures, text="Voir Commandes", width=15, command=afficher_commandes_facture, bg="#8C182D", fg="white").grid(row=0, column=3, padx=5, pady=5)
    Button(frame_buttons_factures, text="Générer PDF", width=12, command=lambda: generate_invoice_pdf(selected_invoice_data), bg="#8C182D", fg="white").grid(row=0, column=4, padx=5, pady=5)
    Button(frame_buttons_factures, text="Exporter PDF", width=12, command=exporter_facture_pdf, bg="#8C182D", fg="white").grid(row=0, column=5, padx=5, pady=5)



  # Form for entering facture details
    frame_form_factures = LabelFrame(window, text="Détails de la Facture", padx=20, pady=20)
    frame_form_factures.pack(fill="x", padx=20, pady=10)

    labels_factures = ["Code Facture", "Montant", "Commande associée"]
    placeholderArrayFacture = [StringVar(), StringVar(), StringVar()]

    # Add labels and entry fields for Code Facture and Montant
    for i, label in enumerate(labels_factures[:2]):  
        Label(frame_form_factures, text=label, width=15).grid(row=i, column=0, padx=5, pady=5)
        Entry(frame_form_factures, width=50, textvariable=placeholderArrayFacture[i]).grid(row=i, column=1, padx=5, pady=5)

    # Add label for Commande associée (Code Commande)
    Label(frame_form_factures, text="Commande associée", width=15).grid(row=2, column=0, padx=5, pady=5)

    # ComboBox for selecting Commande (Code Commande)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Code_cmd FROM commande")
    rows = cursor.fetchall()
    conn.close()
    commandes = [row[0] for row in rows]

    commande_combobox = ttk.Combobox(frame_form_factures, values=commandes, width=47)
    commande_combobox.grid(row=2, column=1, padx=5, pady=5)

    # Add frame for facture table
    frame_table_factures = Frame(window, padx=10, pady=10)
    frame_table_factures.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    tree_factures = ttk.Treeview(frame_table_factures, columns=("Code Facture", "Date Facture", "Montant"), show="headings")
    tree_factures.heading("Code Facture", text="Code Facture")
    tree_factures.heading("Date Facture", text="Date Facture")
    tree_factures.heading("Montant", text="Montant")

    tree_factures.column("Code Facture", anchor=W, width=150)
    tree_factures.column("Date Facture", anchor=W, width=150)
    tree_factures.column("Montant", anchor=W, width=150)

    tree_factures.pack(fill=BOTH, expand=True)
    refresh_invoice_table()

    window.mainloop()

