# parse args before loading big libs
import argparse, re
parser = argparse.ArgumentParser(description="Music visualizer")
parser.add_argument("song", help="The input wav file")
parser.add_argument("-r", "--res", dest="res", default="3840x2160", help="Resolution (format: WIDTHxHEIGHT, you can also type 4k, 2k, 1080p, and so on.)")
parser.add_argument("-q", "--quiet", dest="info", action="store_false", help="Include this argument to not show info about the frame rate, sample rate, and other info.")
parser.add_argument("-o", "--output", dest="out", default="output.mp4", help="The output file (has to end in mp4, default: output.mp4)")
args = parser.parse_args()

if not args.song.endswith(".wav"):
    print("You need to input a wav file.")
    print("To convert your file to wav, it is easiest to run `ffmpeg -i "+args.song+" "+re.sub("\\..*",".wav",args.song)+"`,")
    print("Then input your new wav file.")
    exit(1)

if not args.out.endswith(".mp4"):
    print("This visualizer only outputs mp4s at the moment.")
    print("Please set the output file to end in mp4, for example: "+re.sub("\\..*",".mp4",args.out))
    exit(1)

print("Hang on! I'm initializing variables right now.")
print("I will have a progress bar when I'm rendering.")

import librosa, math, os, shutil, cv2, random, string, numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from tqdm import tqdm

_r=args.res.lower()
if _r=="8k":
    width, height = (8192,4096)
elif _r=="7k":
    width, height = (7168,3584)
elif _r=="6k":
    width, height = (6144,3240)
elif _r=="5k":
    width, height = (5120,2880)
elif _r=="4k":
    width, height = (3840,2160)
elif _r=="3k":
    width, height = (2880,1620)
elif _r=="2k":
    width, height = (2048,1080)
elif _r=="1k":
    width, height = (1024,768)
elif _r=="1080p":
    width, height = (1920,1080)
elif _r=="720p":
    width, height=(1280,720)
else:
    try:
        width, height = (int(args.res.split("x")[0]),int(args.res.split("x")[1]))
    except:
        print("There was an error when parsing.")
        exit(1)

time_series, sample_rate = librosa.load(args.song)
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
dur = librosa.get_duration(y=time_series, sr=sample_rate)

if args.info:
    print("Sample rate: "+str(sample_rate))
    print("Song duration: "+str(dur)+" seconds")
    print("Exact frame rate: "+str(len(stft[0])/dur))
    print("Frame rate for opencv: "+str(len(stft[0])//dur))

temp = "".join(random.choice(string.ascii_letters+string.digits) for i in range(10))

video = VideoWriter("/tmp/opencvtemp"+temp+".mp4", VideoWriter_fourcc(*"mp4v"), float(len(stft[0])//dur), (width, height))
width50=width/50
hheight=height/2
hwidth=width/2

m = len(stft)//360
for k in tqdm(range(len(stft[0])), desc="Rendering"):
# for k in tqdm(range(50), desc="Rendering"):
    lst = []
    frame = np.zeros((height, width, 3),dtype=np.uint8)
    for i in range(360):
        lst.append([math.cos(math.radians(i))*(stft[i*m,k]**0.5+5)*width50+hwidth,math.sin(math.radians(i))*(stft[i*m,k]**0.5+5)*width50+hheight])
    cv2.polylines(frame, [np.array(lst,np.int32).reshape((-1, 1, 2))], isClosed = True, color = (255,255,255), thickness = 1)
    video.write(frame)
video.release()

os.system("ffmpeg-bar -y -i /tmp/opencvtemp"+temp+".mp4 -i "+args.song+" -vf \"fade=t=out:st="+str(math.floor(dur)-2)+":d=2\" "+args.out)
os.remove("/tmp/opencvtemp"+temp+".mp4")
