from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from database import execute_query, fetch_query

def gestion_entrepots_ui():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        rows = fetch_query("SELECT * FROM entrepots")
        for row in rows:
            tree.insert("", "end", values=row)

    def ajouter_entrepot():
        code = code_var.get()
        nom = nom_var.get()
        localisation = localisation_var.get()

        if code and nom and localisation:
            execute_query("INSERT INTO entrepots (id, nom, localisation) VALUES (%s, %s, %s)",
                          (code, nom, localisation))
            refresh_table()
            messagebox.showinfo("Succès", "Entrepôt ajouté avec succès")
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

    root = Toplevel()
    root.title("Gestion des Entrepôts")
    root.geometry("800x400")

    Label(root, text="Gestion des Entrepôts", font=("Arial", 16)).pack(pady=10)

    # Formulaire
    code_var, nom_var, localisation_var = StringVar(), StringVar(), StringVar()

    Label(root, text="Code Entrepôt").pack()
    Entry(root, textvariable=code_var).pack()
    Label(root, text="Nom Entrepôt").pack()
    Entry(root, textvariable=nom_var).pack()
    Label(root, text="Localisation Entrepôt").pack()
    Entry(root, textvariable=localisation_var).pack()

    Button(root, text="Ajouter Entrepôt", command=ajouter_entrepot).pack(pady=10)

    # Tableau
    tree = ttk.Treeview(root, columns=("Code", "Nom", "Localisation"), show="headings")
    tree.heading("Code", text="Code")
    tree.heading("Nom", text="Nom")
    tree.heading("Localisation", text="Localisation")
    tree.pack(fill="both", expand=True)

    refresh_table()
    root.mainloop()
