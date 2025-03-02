import streamlit as st
from PIL import Image, ImageDraw

def reduce_colors_with_pillow(image, num_colors):
    reduced_image = image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)
    reduced_image = reduced_image.convert("RGB")
    return reduced_image

def resize_and_crop(image, new_width, new_height):
    width, height = image.size
    aspect_ratio = width / height

    if new_width / aspect_ratio <= new_height:
        new_size = (new_width, int(new_width / aspect_ratio))
    else:
        new_size = (int(new_height * aspect_ratio), new_height)

    resized_image = image.resize(new_size, Image.LANCZOS)

    left = (resized_image.width - new_width) / 2
    top = (resized_image.height - new_height) / 2
    right = (resized_image.width + new_width) / 2
    bottom = (resized_image.height + new_height) / 2

    cropped_image = resized_image.crop((left, top, right, bottom))
    return cropped_image

def add_brick_grid(image, line_thickness=1, grid_color="black", scale_factor=64):
    width, height = image.size
    enlarged_image = image.resize((width * scale_factor, height * scale_factor), Image.NEAREST)

    draw = ImageDraw.Draw(enlarged_image)
    for y in range(0, height * scale_factor, scale_factor):
        for x in range(0, width * scale_factor, scale_factor):
            if (y // scale_factor) % 2 == 0:
                draw.rectangle([x, y, x + scale_factor, y + scale_factor], outline=grid_color, width=line_thickness)
            else:
                draw.rectangle([x - (scale_factor // 2), y, x + (scale_factor // 2), y + scale_factor], outline=grid_color, width=line_thickness)

    return enlarged_image

def main():
    st.title("Enfilage de perles")

    uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        width, height = image.size
        num_colors = len(set(image.getdata()))
        st.write(f"{width}px x {height}px - {num_colors} couleurs")

        with st.form("image_processing_form"):
            new_width = st.number_input("Nb perle en largeur", min_value=1, max_value=width, value=width)
            new_height = st.number_input("NB perle en  hauteur", min_value=1, max_value=height, value=height)
            new_num_colors = st.number_input("Nombre de couleurs", min_value=1, max_value=num_colors, value=num_colors)
            line_thickness = st.number_input("Épaisseur de la grille", min_value=1, value=1)
            grid_color = st.color_picker("Couleur de la grille", "#000000")

            submitted = st.form_submit_button("Soumettre")

            if submitted:
                processed_image = resize_and_crop(image, new_width, new_height)
                reduced_image = reduce_colors_with_pillow(processed_image, new_num_colors)

                final_image = add_brick_grid(
                    image=reduced_image,
                    line_thickness=line_thickness,
                    grid_color=grid_color,
                    scale_factor=64
                )

                st.image(final_image, caption="Perles", use_column_width=True)

if __name__ == "__main__":
    main()
