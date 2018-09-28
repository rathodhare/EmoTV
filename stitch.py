import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from PIL import Image ,ImageDraw, ImageFont

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

if __name__ == '__main__':

    fontname = "Arial.ttf"
    fontsize = 11   
    text = "example@gmail.com"

    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"
    font_path = "/Library/Fonts/Times New Roman.ttf"
    wordcloud = WordCloud(font_path=font_path, width = 1000, height = 500).generate('australian american english french russian')
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    #font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)

    img.save("D:/image.png")
