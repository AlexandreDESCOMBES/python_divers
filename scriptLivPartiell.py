import shutil
import os

def remplacer_mot(fichier, ancien_mot, nouveau_mot):
    if not os.path.exists(fichier):
        print(f"❌ Le fichier '{fichier}' n'existe pas.")
        return

    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    print("📄 Contenu original :")
    print(contenu)

    if ancien_mot not in contenu:
        print(f"⚠️ Le mot '{ancien_mot}' n'a pas été trouvé dans le fichier.")
    else:
        contenu_modifie = contenu.replace(ancien_mot, nouveau_mot)
        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu_modifie)
        print(f"✅ Remplacement effectué : '{ancien_mot}' → '{nouveau_mot}'")

        # Afficher après modification
        with open(fichier, 'r', encoding='utf-8') as f:
            print("✏️ Nouveau contenu :")
            print(f.read())

def ignore_dossiers(indesirables):
    def _ignore(path, names):
        ignorés = []
        for nom in names:
            if nom in indesirables:
                ignorés.append(nom)
        return ignorés
    return _ignore

def copier_repertoire(source, destination, dossiers_a_exclure):
    if not os.path.exists(source):
        print(f"❌ Le dossier source '{source}' n'existe pas.")
        return

    try:
        shutil.copytree(
            source,
            destination,
            ignore=ignore_dossiers(dossiers_a_exclure)
        )
        print(f"📂 Copie réussie de '{source}' vers '{destination}' (sans {dossiers_a_exclure})")
    except FileExistsError:
        print(f"⚠️ Le dossier '{destination}' existe déjà.")
    except Exception as e:
        print(f"❌ Erreur pendant la copie : {e}")
        

# Exemple d'utilisation
source = "C:/Users/alex4/Documents/MIKROE/Projects/Livraison_Partielle"
base_destination = "C:/Users/alex4/Documents/MIKROE/Projects"
nouveau_nom = input("📝 Nom du nouveau dossier : ").strip()
destination = os.path.join(base_destination, nouveau_nom)
dossiers_a_exclure = ['.git'] 

fichier = os.path.join(destination, "CMakeLists.txt")

print(f"\n📁 Chemin attendu du fichier à modifier : {fichier}\n")

copier_repertoire(source, destination, dossiers_a_exclure)
remplacer_mot(fichier, "Livraison_Partielle", nouveau_nom)
