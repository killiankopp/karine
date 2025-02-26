import streamlit as st
from PIL import Image, ImageDraw

def reduce_colors_with_pillow(image, num_colors):
    # Convertir l'image en mode 'P' avec une palette de couleurs
    reduced_image = image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)
    # Convertir l'image en mode 'RGB' pour l'affichage
    reduced_image = reduced_image.convert("RGB")
    return reduced_image

def add_brick_grid(image):
    # Doubler la taille de l'image
    width, height = image.size
    enlarged_image = image.resize((width * 2, height * 2), Image.NEAREST)

    # Dessiner la grille
    draw = ImageDraw.Draw(enlarged_image)
    for y in range(0, height * 2, 2):
        for x in range(0, width * 2, 2):
            if (y // 2) % 2 == 0:
                draw.rectangle([x, y, x + 2, y + 2], outline="black")
            else:
                draw.rectangle([x - 1, y, x + 1, y + 2], outline="black")

    return enlarged_image

def main():
    st.title("Application de traitement d'image")

    # Téléchargement de l'image
    uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Lire l'image
        image = Image.open(uploaded_file)
        st.image(image, caption="Image téléchargée", use_column_width=True)

        # Afficher les dimensions de l'image
        width, height = image.size
        st.write(f"Largeur: {width}, Hauteur: {height}")

        # Calculer le nombre de couleurs
        num_colors = len(set(image.getdata()))
        st.write(f"Nombre de couleurs: {num_colors}")

        # Formulaire pour les paramètres
        with st.form("image_processing_form"):
            new_width = st.number_input("Nouvelle largeur", min_value=1, max_value=width, value=width)
            new_height = st.number_input("Nouvelle hauteur", min_value=1, max_value=height, value=height)
            new_num_colors = st.number_input("Nombre de couleurs souhaité", min_value=1, max_value=num_colors, value=num_colors)

            # Bouton de soumission
            submitted = st.form_submit_button("Soumettre")

            if submitted:
                # Redimensionner l'image
                resized_image = image.resize((new_width, new_height))
                st.image(resized_image, caption="Image redimensionnée", use_column_width=True)

                # Réduire le nombre de couleurs
                reduced_image = reduce_colors_with_pillow(resized_image, new_num_colors)
                st.image(reduced_image, caption="Image avec couleurs réduites", use_column_width=True)

                # Ajouter la grille
                final_image = add_brick_grid(reduced_image)
                st.image(final_image, caption="Image avec grille en mur de brique", use_column_width=True)

if __name__ == "__main__":
    main()
