import os
import sys
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


extract_keyframes(sys.argv[1])  