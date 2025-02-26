import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def reduce_colors(image, num_colors):
    # Convertir l'image en tableau numpy
    image_array = np.array(image)

    # Redimensionner l'image en un tableau 2D de pixels
    pixels = image_array.reshape(-1, 3)

    # Appliquer KMeans pour réduire le nombre de couleurs
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Remplacer chaque pixel par la couleur du centroïde le plus proche
    reduced_colors = kmeans.cluster_centers_[kmeans.labels_]
    reduced_image_array = reduced_colors.reshape(image_array.shape)

    # Convertir le tableau numpy en image
    reduced_image = Image.fromarray(np.uint8(reduced_image_array))
    return reduced_image

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

        # Redimensionner l'image
        new_width = st.number_input("Nouvelle largeur", min_value=1, max_value=width, value=width)
        new_height = st.number_input("Nouvelle hauteur", min_value=1, max_value=height, value=height)
        resized_image = image.resize((new_width, new_height))
        st.image(resized_image, caption="Image redimensionnée", use_column_width=True)

        # Réduire le nombre de couleurs
        new_num_colors = st.number_input("Nombre de couleurs souhaité", min_value=1, max_value=num_colors, value=num_colors)
        reduced_image = reduce_colors(resized_image, new_num_colors)
        st.image(reduced_image, caption="Image avec couleurs réduites", use_column_width=True)

if __name__ == "__main__":
    main()
