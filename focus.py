from rembg import remove
from PIL import Image

# Charger l'image
input_image = Image.open("image.jpg")

# Supprimer l'arrière-plan
output_image = remove(input_image)

# Sauvegarder ou afficher
output_image.show()
output_image.save("result.png")