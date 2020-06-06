from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from parser import *

barcodeImg = Image.open("barcode.jpeg")
width, height = barcodeImg.size

# Растянуть, сгладить.
coercedWidth = width * 4
barcodeImg = barcodeImg.resize((coercedWidth, height), Image.ANTIALIAS)

# Обрезать, перевести в ч/б, сохранить как массив. Инверсия, потому что в RGB черный это 0.
horizontalSlice = barcodeImg.crop((0, int(height / 2), coercedWidth, int(height / 2) + 1)).convert('L')
horizontalData = 255 - np.asarray(horizontalSlice, dtype="int32")[0]
averageValue = np.average(np.asarray(horizontalSlice, dtype="int32")[0])  # Среднее значение

plt.plot(horizontalData)
plt.show()

# Чтобы определить "ширину одного бита" выделим последовательность,
# сохраняя позиции пересечения средней линии.

pos1, pos2 = -1, -1
bitSequence = ''

for p in range(coercedWidth - 2):
    if horizontalData[p] < averageValue < horizontalData[p + 1]:
        bitSequence += '1'
        if pos1 == -1:
            pos1 = p
        if bitSequence == '101':
            pos2 = p
            break
    if horizontalData[p] > averageValue > horizontalData[p + 1]:
        bitSequence += '0'

bitWidth = int((pos2 - pos1) / 3)

bits = ''
for p in range(coercedWidth - 2):
    if horizontalData[p] > averageValue > horizontalData[p + 1]:
        interval = p - pos1
        cnt = interval / bitWidth
        bits += '1' * int(round(cnt))
        pos1 = p
    elif horizontalData[p] < averageValue < horizontalData[p + 1]:
        interval = p - pos1
        cnt = interval / bitWidth
        bits += '0' * int(round(cnt))
        pos1 = p

# 11 bit encoding
bitsSeparated = [bits[i: i + 11] for i in range(0, len(bits), 11)]

str_out = ""
for sym in bitsSeparated:
    if CODE128B[sym] == 'Start':
        continue
    if CODE128B[sym] == 'Stop':
        break
    str_out += CODE128B[sym]
    print("  ", sym, CODE128B[sym])

print("Str:", str_out)