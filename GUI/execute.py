#!/usr/bin/python
from fltk import *
from PIL import Image
from distutils.dir_util import copy_tree
import shutil
import glob
import os

global caixa
global path
global video_extensions
video_extensions = ["ebm","mkv","flv","vob","gif","avi","mov","wmv","mp4","m4p","m4v","peg","mpg","3gp"]

def is_video_file(file):
    return file[-3:] in video_extensions


def extract_keyframes(path):
    for subdir, dirs, files in os.walk(path):
        subsubdir = subdir.split("/")[-1]
        for filename in files:
            file = path+"/"+subsubdir+"/"+filename
            if(is_video_file(file)):
                os.system("ffmpeg -i "+file+" -vf 'select=eq(pict_type\,I)' -vsync vfr "+file[:-4]+"_%04d.jpg -hide_banner")



def convert_jpeg(path): #convert image files to jpg
    for subdir, dirs, files in os.walk(path):
        subsubdir = subdir.split("/")[-1]
        for filename in files:
            if(filename.endswith(".png") or filename.endswith(".bmp")):
                print(path+"/"+subsubdir+"/"+filename)
                im = Image.open(path+"/"+subsubdir+"/"+filename)
                rgb_im = im.convert('RGB')
                rgb_im.save(path+"/"+subsubdir+"/"+filename[:-3]+"jpg")
                os.remove(path+"/"+subsubdir+"/"+filename)


def treino(path):
    os.system("python facenet/src/classifier.py TRAIN "+os.path.realpath(path)+" "+os.path.realpath("facenet/model/pesos.pb")+" "+os.path.realpath("facenet/model/classifier.pkl")+" --batch_size 1000")

def classificar(path):
    os.system("python facenet/src/classifier.py CLASSIFY "+os.path.realpath(path)+" "+os.path.realpath("facenet/model/pesos.pb")+" "+os.path.realpath("facenet/model/classifier.pkl")+" --batch_size 1000 > out.txt")


def handle_folder():
    global path
    file_browser = Fl_File_Chooser(".", "*", Fl_File_Chooser.DIRECTORY, "Selecione a pasta com imagens e/ou vídeos")
    file_browser_label = Fl_Box(16,4,25,5, "Pasta")
    file_browser.show()

    while file_browser.visible():
        Fl.wait()
    
    if(file_browser.value() == None):
        return
    
    path = file_browser.value()
    extract_keyframes(path)
    text = ""
    for filename in os.listdir(path):
        text = text+filename+"\n"

    caixa.box(FL_DOWN_BOX)
    caixa.label(text)
    caixa.redraw()

def clicked_train(widget):
    global path
    handle_folder()


    if (path == " "):
        return

    facebank = os.path.realpath("facenet/facebank")
    if (path != facebank):
        for filename in os.listdir(path):
            copy_tree(path,facebank)

    treino(facebank)
    caixa.label("Rede atualizada com sucesso.")


def clicked_classify(widget):
    global path
    handle_folder()


    if (path == " "):
        return

    convert_jpeg(path)
    classificar(path)
    texto = ""
    with open("out.txt","r") as file:
        for line in file:
            texto = texto+line+"\n"
    caixa.label(texto)

def main():
    global caixa
    global train
    global path
    path = " "

    window = Fl_Window(600, 400)
    window.label("Facenet")

    button1 = Fl_Button(400, 130, 120, 50)
    button1.label("Treinar")
    button1.callback(clicked_train)

    caixa = Fl_Box(50,10,300,380)
    caixa.box(FL_UP_BOX)
    caixa.label("Neste campo serão apresentadas \n informações de treino e\n de classificação do algoritmo.")


    button2 = Fl_Button(400, 210, 120, 50)
    button2.label("Classificar")
    button2.callback(clicked_classify)

    window.end()
    window.show()
    Fl.run()



if __name__ == '__main__':
    main()

