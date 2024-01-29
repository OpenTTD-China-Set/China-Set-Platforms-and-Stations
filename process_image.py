from PIL import Image, ImageOps
import glob

def add_to_bottom(image1, image2):
        # Create a new image with a width of the original image and a height of the original image * 2
    new_image = Image.new('RGBA', (image1.width, image1.height * 2))
    # copy the original image to the top of the new image
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (0, image1.height))
    return new_image

def mirror_image(path):
    # mirror and add the mirrored image to the bottom of the original image
    for file in glob.glob(f'{path}/stn_*32bpp.png'):
        image = Image.open(file)
        original_image = image.copy()
        image = ImageOps.mirror(image)
        image = add_to_bottom(original_image, image)
        image.save(file)