#coding:utf-8
import freetype
import numpy as np
from PIL import Image
face = freetype.Face("tyc-num.ttf")
face.set_char_size( 48*64 )
face.load_char('广')
bitmap = face.glyph.bitmap
print bitmap.width
print bitmap.rows
print len(bitmap.buffer )
img = np.array(bitmap.buffer)
img.resize((bitmap.rows,bitmap.width))
im =Image.fromarray(np.uint8(img))
im.save("t.jpg")
