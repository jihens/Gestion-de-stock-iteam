from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from database import execute_query, fetch_query

def gestion_clients_ui():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        rows = fetch_query("SELECT * FROM clients")
        for row in rows:
            tree.insert("", "end", values=row)

    def ajouter_client():
        code = code_var.get()
        nom = nom_var.get()
        adresse = adresse_var.get()

        if code and nom and adresse:
            execute_query("INSERT INTO clients (id, nom, adresse) VALUES (%s, %s, %s)",
                          (code, nom, adresse))
            refresh_table()
            messagebox.showinfo("Succès", "Client ajouté avec succès")
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

    root = Toplevel()
    root.title("Gestion des Clients")
    root.geometry("800x400")

    Label(root, text="Gestion des Clients", font=("Arial", 16)).pack(pady=10)

    # Formulaire
    code_var, nom_var, adresse_var = StringVar(), StringVar(), StringVar()

    Label(root, text="Code Client").pack()
    Entry(root, textvariable=code_var).pack()
    Label(root, text="Nom Client").pack()
    Entry(root, textvariable=nom_var).pack()
    Label(root, text="Adresse Client").pack()
    Entry(root, textvariable=adresse_var).pack()

    Button(root, text="Ajouter Client", command=ajouter_client).pack(pady=10)

    # Tableau
    tree = ttk.Treeview(root, columns=("Code", "Nom", "Adresse"), show="headings")
    tree.heading("Code", text="Code")
    tree.heading("Nom", text="Nom")
    tree.heading("Adresse", text="Adresse")
    tree.pack(fill="both", expand=True)

    refresh_table()
    root.mainloop()
