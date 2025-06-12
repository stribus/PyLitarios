import pyautogui as pg
import base64
import io
from PIL import Image
import time

botaoWhatsB64 ='iVBORw0KGgoAAAANSUhEUgAAAB0AAAAZCAIAAABCYLJOAAACnklEQVR4nLWVO0xTYRSAz397aXvvpZY+oBBCkRC0GicTgpOPYHgnJKALiQwuuKBNoBYWIQ6ERQcZdMGRDdANShsHkMXBRV1o1Zq0gDT3Fvrgvn9TmtRSoPZaPcPNOef/z5dzzyM/oowmKEMwhlqi4mll8y29FQDeieyTZGhHlVCZXAB4bbo8SDly5uLh7v3EF6JMKGC4bchkmpOMiYEsuEY6SPNNE0alYrnF+Kn+Qq7jgZ25Speebvpj2h9l8+vgF1hAJ7gyp5QOBQDLQNXk7JYEan7fMIbCvjkeVpvbtXUy+SHFLu4LIQGLGGccGAEqzPek6JGhy9bVae1IKSkAoAl6lfWtsCsSFrMXKluZylZmP5DYfbF31JfM5w/cOn3ddNP0ZnzTE/Sk1TQAGAnjdfON2ebZ5z+eRcTIWYHFuBVI73VOzHyfCQvhnJNXeR+3+jn1adzp8Ya8IhZOjS02v3er7wS4QFgIu2hXr603/ygiRtZY32D1wFmxxbjdtu41zgcA9xzDo/WjDYaG/NNAPNBh7dTMpQgqqaR4lQeAbTEqY4WTjq2AoAq8yjMEo40rYsmIDFl9YXeBldiR+hGKoIZqhiw6S9avYBkddV8DV8GyDpFmXRUAsDI7FhprMp5fvrI8XDvscT7ODgZDMEk1qXkeNg/et51r83GrALAn/XwUdPfZ+miC8rN+AGi3tPu5jKKZayVtfv53pILlt7E3Wb3R0Nhv7x8PejRzdaBroVuCh0EXfclFuzbi6zE5BgB20t5j62kzX5v6NnWg7GvPF6EdcWf+4nxEiETF7bkLc2kls28EEEuxJfeWO7fH2rgKlie/TuTMV9GXoEXKfi9K5WL4S8FF65DYSJI1JNL4G1iFxPqxQf4H7/Gp8r/q+wv+NAYnxXDS1QAAAABJRU5ErkJggg=='

def b64_to_img(b64):
    imgdata = base64.b64decode(b64)
    return Image.open(io.BytesIO(imgdata))

botaoWhats = b64_to_img(botaoWhatsB64)


x, y = pg.locateCenterOnScreen(botaoWhats, confidence=0.9)

if x is not None and y is not None:
    print(f"Botão encontrado em {x}, {y}")
else:
    print("Botão não encontrado")
    exit()
    
pg.moveTo(x, y, duration=1)
pg.mouseDown(duration=2)
pg.mouseUp()

