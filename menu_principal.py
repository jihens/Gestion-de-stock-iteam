from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from gestion_produits import gestion_produits_ui
from gestion_commandes import gestion_commandes_ui
from gestion_factures import gestion_factures_ui

def main_menu():
    root = Tk()
    root.title("Menu Principal - Gestion de Stock")
    root.geometry("600x600")
    root.configure(bg="#F0F0F0")

    # Label pour afficher les messages de retour (succès ou erreur)
    message_label = Label(root, text="", font=("Arial", 12), fg="#8C182D", bg="#F0F0F0")
    message_label.pack(pady=10)

    def update_message(message):
        message_label.config(text=message)

    # Fonction pour quitter l'application
    def quitter_application():
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment quitter ?"):
            root.quit()

    # Fonction pour afficher les informations sur l'application
    def afficher_a_propos():
        messagebox.showinfo("À propos", "Application de gestion de stock version 1.0\nDéveloppée par Fares Choura Et Jihene Farihani.")

    # Fonction pour appliquer un thème
    def apply_theme(theme):
        if theme == "clair":
            root.configure(bg="#F0F0F0")
            message_label.config(bg="#F0F0F0", fg="#8C182D")
        elif theme == "sombre":
            root.configure(bg="#333333")
            message_label.config(bg="#333333", fg="#FFFFFF")

    # Barre de menu stylisée avec icônes
    menu_bar = Menu(root, bg="#010440", fg="white")

    # Menu "Fichier"
    file_menu = Menu(menu_bar, tearoff=0, bg="#020659", fg="white", activebackground="#8C0303", activeforeground="white")
    file_menu.add_command(label="\ud83d\udce6 Gestion des Produits", command=gestion_produits_ui)
    file_menu.add_command(label="\ud83d\uded2 Gestion des Commandes", command=gestion_commandes_ui)
    file_menu.add_command(label="\ud83d\udcc4 Gestion des Factures", command=gestion_factures_ui)
    file_menu.add_separator()
    file_menu.add_command(label="\ud83d\udeaa Quitter", command=quitter_application)
    menu_bar.add_cascade(label="Fichier", menu=file_menu)

    # Menu "Aide"
    help_menu = Menu(menu_bar, tearoff=0, bg="#020659", fg="white", activebackground="#8C0303", activeforeground="white")
    help_menu.add_command(label="\u2139\ufe0f À propos", command=afficher_a_propos)
    menu_bar.add_cascade(label="Aide", menu=help_menu)

    # Menu "Thème"
    theme_menu = Menu(menu_bar, tearoff=0, bg="#020659", fg="white", activebackground="#8C0303", activeforeground="white")
    theme_menu.add_command(label="\ud83c\udf1e Thème Clair", command=lambda: apply_theme("clair"))
    theme_menu.add_command(label="\ud83c\udf11 Thème Sombre", command=lambda: apply_theme("sombre"))
    menu_bar.add_cascade(label="Thème", menu=theme_menu)

    # Ajout de la barre de menu
    root.config(menu=menu_bar)

    # Chargement d'une image
    try:
        img = Image.open("C:/Users/jihee/pyython/projet/iteam-removebg-preview.png")
        img = img.resize((300, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        Label(root, image=photo, bg="#F0F0F0").pack(pady=10)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        update_message(f"Erreur lors du chargement de l'image : {e}")

    Label(root, text="Menu Principal", font=("Arial", 18, "bold"), bg="#F0F0F0", fg="#8C182D").pack(pady=20)

    # Boutons principaux
    Button(root, text="\ud83d\udce6 Gestion des Produits", command=gestion_produits_ui, width=30, height=2, bg="#8C0303", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="\ud83d\uded2 Gestion des Commandes", command=gestion_commandes_ui, width=30, height=2, bg="#8C0303", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="\ud83d\udcc4 Gestion des Factures", command=gestion_factures_ui, width=30, height=2, bg="#8C0303", fg="white", font=("Arial", 12)).pack(pady=10)

    root.mainloop()
if __name__ == "__main__":
    main_menu()
