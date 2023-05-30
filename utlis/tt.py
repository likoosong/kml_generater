import pytesseract
from PIL import Image
# 读取图片
im = Image.open('img_1.png')
# 识别文字，并指定语言
string = pytesseract.image_to_string(im, lang='chi_sim')
print(string)


# mail.eth.edu.kg
# 4096.00 MB 优化云 - 144.202.96.41

