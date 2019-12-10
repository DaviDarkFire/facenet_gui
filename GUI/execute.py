#!/usr/bin/python
from fltk import *
from PIL import Image
import glob
import os

global caixa
global escolha #1 para treino e 0 para classificação
global path

def fileOrFolder(path): #return 1 if file and 0 if folder
    return os.path.isfile(path)


def convert_jpeg(path): #convert image files to jpg
    for filename in os.listdir(path):
        if(filename.endswith(".png") or filename.endswith(".bmp") or filename.endswith(".gif")):
            im = Image.open(path+filename)
            rgb_im = im.convert('RGB')
            rgb_im.save(path+filename[-3:]+"jpg")
            os.remove(path+filename)


def train(path):
    os.system("python facenet/src/classifier.py TRAIN "+os.path.realpath(path)+" "+os.path.realpath("facenet/model/pesos.pb")+" "+os.path.realpath("facenet/model/classifier.pkl")+" --batch_size 1000")

def classify(path):
    os.system("python facenet/src/classifier.py CLASSIFY "+os.path.realpath(path)+" "+os.path.realpath("facenet/model/pesos.pb")+" "+os.path.realpath("facenet/model/classifier.pkl")+" --batch_size 1000 > out.txt")



def clicked_file(widget):
    global caixa
    global path
    file_browser = Fl_File_Chooser(".", "*", Fl_File_Chooser.SINGLE, "Selecione a imagem ou vídeo")
    #file_browser = Fl_File_Chooser(".", "*", Fl_File_Chooser.DIRECTORY, "Selecione o arquivo de video")
    file_browser_label = Fl_Box(16,4,25,5, "Arquivo:")
    file_browser.show()
    while file_browser.visible():
        Fl.wait() 

    caixa.box(FL_DOWN_BOX)

    img = Fl_JPEG_Image(file_browser.value())
    caixa.image(img)
    caixa.label("")

    caixa.redraw()

    path = file_browser.value()

    

def clicked_folder(widget):
    global path
    file_browser = Fl_File_Chooser(".", "*", Fl_File_Chooser.DIRECTORY, "Selecione a pasta com imagens e/ou vídeos")
    #file_browser = Fl_File_Chooser(".", "*", Fl_File_Chooser.DIRECTORY, "Selecione o arquivo de video")
    file_browser_label = Fl_Box(16,4,25,5, "Pasta")
    file_browser.show()
    while file_browser.visible():
        Fl.wait()

    path = file_browser.value()

    caixa.box(FL_DOWN_BOX)

    text = ""
    
    for filename in os.listdir(path):
        text = text+filename+"\n"

    caixa.label(text)
    caixa.redraw()

   

def clicked_vai(widget):
    global escolha #1 para treino e 0 para classificação
    
    if escolha:
        train(path)
    else
        classify(path)




def main():
    global caixa
    global escolha
    window = Fl_Window(600, 400)
    window.label("Facenet")

    button1 = Fl_Button(400, 160, 120, 20)
    button1.label("PASTA")
    button1.callback(clicked_folder)

    button2 = Fl_Button(400, 200, 120, 20)
    button2.label("ARQUIVO")
    button2.callback(clicked_file)

    button2 = Fl_Button(400, 240, 120, 20)
    button2.label("Vai")

    button2.callback(clicked_vai)

    train = Fl_Round_Button(370, 120, 20, 5, "Treinar")
    classify = Fl_Round_Button(450, 120, 20, 5, "Classificar")
    train.type(FL_RADIO_BUTTON)
    classify.type(FL_RADIO_BUTTON)


    caixa = Fl_Box(50,100,300,200)
    caixa.box(FL_UP_BOX)
    caixa.label("Neste campo serão apresentadas \n imagens e informações \n de classificação do algoritmo.")

    window.end()
    window.show()
    Fl.run()



if __name__ == '__main__':
    main()

