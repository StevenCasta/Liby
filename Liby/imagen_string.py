import base64
from pymongo import MongoClient
import gridfs
from os import remove

from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

import cv2
from PIL import Image


class ImagenBase64(object):
    """docstring for ImagenBase64."""

    def __init__(self):
        super(ImagenBase64).__init__()
        self.imagen = None

    def imagenString(self, imagen):#imagen es direccion del archivo
        with open(imagen, "rb") as imagenes_file:
        	stringimg = base64.b64encode(imagenes_file.read())

        return stringimg

    def stringImagen(self, encoded_string):
        # Pillow
        ima_IO = BytesIO(base64.b64decode(encoded_string))
        img_PIL = Image.open(ima_IO)
        self.imagen = img_PIL

        return img_PIL

    def guardarImagen(self, nombre):
        cv2.imwrite(nombre,self.imagen)
        cv2.destroyAllWindows()

    def guardarImg(self, nombre, strimg):
        ima_IO = BytesIO(base64.b64decode(strimg))
        img_PIL = Image.open(ima_IO)
        img_PIL.save(nombre)

    def eliminarImagen(self, nombre):
        remove(nombre)


#img = r'/home/diegogomez/Escritorio/LABORATORIO/PORTADAS/1984.jpg'
#if __name__ == '__main__':
#    imagenstring = ImagenBase64()
#    cadena = imagenstring.imagenString('./PORTADAS/1984.jpg')
#    print(cadena)
