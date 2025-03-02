import streamlit as st
from PIL import Image, ImageDraw

def reduce_colors_with_pillow(image, num_colors):
    # Convertir l'image en mode 'P' avec une palette de couleurs
    reduced_image = image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)
    # Convertir l'image en mode 'RGB' pour l'affichage
    reduced_image = reduced_image.convert("RGB")
    return reduced_image

def add_brick_grid(image, line_thickness=1, grid_color="black", scale_factor=8):
    # Augmenter la taille de l'image pour un décalage plus fin
    width, height = image.size
    enlarged_image = image.resize((width * scale_factor, height * scale_factor), Image.NEAREST)

    # Dessiner la grille
    draw = ImageDraw.Draw(enlarged_image)
    for y in range(0, height * scale_factor, scale_factor):
        for x in range(0, width * scale_factor, scale_factor):
            if (y // scale_factor) % 2 == 0:
                draw.rectangle([x, y, x + scale_factor, y + scale_factor], outline=grid_color, width=line_thickness)
            else:
                draw.rectangle([x - (scale_factor // 2), y, x + (scale_factor // 2), y + scale_factor], outline=grid_color, width=line_thickness)

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
            line_thickness = st.number_input("Épaisseur des lignes de la grille", min_value=1, value=1)
            grid_color = st.color_picker("Couleur de la grille", "#000000")

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
                final_image = add_brick_grid(reduced_image, line_thickness=line_thickness, grid_color=grid_color, scale_factor=8)
                st.image(final_image, caption="Image avec grille en mur de brique", use_column_width=True)

if __name__ == "__main__":
    main()
