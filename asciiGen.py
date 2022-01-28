from PIL import Image, ImageOps
from numpy import char
from pyperclip import copy
from sympy import symbols, solve

#ASCII_CHARS = ['@', '#', '%', 'S', '?', '*', '+', ';', ':', ',', '.']
#ASCII_CHARS = ['⢀', '⠄', '⢈', '⢉', '⠎', '⠶', '⡲', '⢳', '⠿', '⣾', '⣿']
ASCII_CHARS = ['⠄', '⠖', '⡶', '⣿']
def dither(image, amountOfColors):
    image = ImageOps.grayscale(image)
    pixelList = list(image.getdata())
    x = image.size[0]
    y = image.size[1]
    ylimit = y*x-x
    xylimit = len(pixelList)-1

    for i, value in enumerate(pixelList):
        newValue = round(value/(255/amountOfColors))*(255/amountOfColors)
        quantError = value - newValue
        pixelList[i] = newValue
        if i < x:
            pixelList[i-x] += quantError*5/16
        if i < ylimit:
            pixelList[i+x] += quantError*3/16
        if i != 0:
            pixelList[i-1] += quantError*1/16
        if i != xylimit:
            pixelList[i+1] += quantError*7/16

    for i, value in enumerate(pixelList):
        pixelList[i] = round(value/(255/amountOfColors))*(255/amountOfColors)

    newImage = Image.new('L', (x, y))
    newImage.putdata(pixelList)
    return newImage

def resizeImage(image :Image, charAmount :int):
    x = symbols('x')
    ratio = image.size[0]/image.size[1]*1.8
    expr = (x*(ratio)*x)-charAmount
    sol = solve(expr)
    size = (round(sol[1]*ratio), round(sol[1]))
    ratios = (size[0]/image.size[0], size[1]/image.size[1])
    image = image.resize((round(image.size[0]*ratios[0]), round(image.size[1]*ratios[1])))
    return image

def genAscii(image):
    pixelList = list(image.getdata())
    ascii = ''
    for i1 in range(image.size[1]):
        offset = i1*image.size[0]
        for i2 in range(image.size[0]):
            ascii += ASCII_CHARS[round(pixelList[i2+offset]/(255/3))]
            #0.0392156862745098
        ascii += '\n'
    copy(ascii)
            

def main():
    path = input('Path to image: ')
    chars = int(input('Amount of chars (usually at least 50 under limit): '))
    
    try:
        image = Image.open('./images/'+path)
        
    except:
        print('Image path or -file is invalid!')
        tryAgain = input('Do you want to try again y/n: ')
        if tryAgain == 'y':
            main()
        return
    
    image = resizeImage(image, chars)
    image = dither(image, 3)
    genAscii(image)
    
main()