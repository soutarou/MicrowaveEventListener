import time
import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import math

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
bx = fig.add_subplot(2,1,2)

N = 1024
FS = 44100
DT = 1/FS
HAM_WIN = np.hamming(N)
FREQ = np.fft.fftfreq(N, d=1.0/FS)

in_float = np.array([])

im1 = None
im2 = None

plotx = 0

def onclick(event):
    global plotx
    ix, iy,y = event.xdata, event.ydata,event.y

    if y < 240 and ix:
        plotx = ix

def plot(x):
    global im1,im2,plotx

    start = int((plotx/DT)%(in_float.size-N))

    ampSp = getAmpSpectrum(start)

    #スペクトログラム
    ax.set_ylim(0.0,0.003)
    # plt.ylim([-160,0])
    # plt.xlim([0,FS/2])
    if im1 == None:
        im1 = ax.plot(FREQ[:int(N/2)],ampSp[:int(N/2)])
    else:
        im1[0].set_data(FREQ[:int(N/2)],ampSp[:int(N/2)])
    # plt.plot(FREQ[:int(N/2)],logAmpSp[:int(N/2)])

    bx.clear()
    bx.vlines(plotx,-2, 2, "blue", linestyles='dashed')
    # bx.vlines(plotx+(N*DT),-2, 2, "blue", linestyles='dashed')
    # print("plotx > ",plotx," next > ",(plotx+(N*DT)))
    xmax = in_float.size*DT
    t = np.arange(0, in_float.size*DT, DT)
    bx.set_xlim(0.0,xmax)
    bx.set_ylim(-0.5,0.5)
    bx.plot(t,in_float)
    # if im2 == None:
    #     im2 = bx.plot(in_float)
    #     print(ax)
    # else:
    #     im2[0].set_data(np.arange(in_float.size),in_float)

def getAmpSpectrum(start):
    f = HAM_WIN*in_float[start:start+N]
    fSp = np.fft.fft(f,n=None)
    ampSp = np.abs(fSp/(N/2))
    # logAmpSp = 20*np.log10(ampSp)

    return ampSp

def main():
    args = sys.argv

    path = args[1]

    global in_float

    wf = wave.open(path , "r" )
    buf = wf.readframes(wf.getnframes())
    # バイナリデータを16bit整数に変換
    data = np.frombuffer(buf, dtype="int16")
    dt = 1/FS
    t = np.arange(0, data.size*dt, dt) # 時間軸

    # short型のデータバッファをfloatに
    in_float = np.frombuffer(data, dtype=np.int16).astype(np.float)
    # 値の範囲を-1.0 ~ 1,0に変換
    in_float[in_float > 0.0] /= float(2**15 - 1)
    in_float[in_float <= 0.0] /= float(2**15)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    ani = animation.FuncAnimation(fig,plot,interval = 300)

    plt.show()          # グラフ表示

if __name__ == '__main__':
    main()
