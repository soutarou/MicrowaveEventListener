import time
import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import math

fig = plt.figure()

N = 1024
FS = 44100
HAM_WIN = np.hamming(N)

magnitude = np.array([])
sinFreq = np.array([])

def main():
    args = sys.argv

    path = args[1]

    wf = wave.open(path , "r" )
    buf = wf.readframes(wf.getnframes())
    # バイナリデータを16bit整数に変換
    data = np.frombuffer(buf, dtype="int16")

    # short型のデータバッファをfloatに
    in_float = np.frombuffer(data, dtype=np.int16).astype(np.float)
    # 値の範囲を-1.0 ~ 1,0に変換
    in_float[in_float > 0.0] /= float(2**15 - 1)
    in_float[in_float <= 0.0] /= float(2**15)

    dt = 1/FS
    t1 = np.arange(0, in_float.size*dt, N*dt) # 時間軸
    t2 = np.arange(0, in_float.size*dt, N*dt) # 時間軸
    t3 = np.arange(0, in_float.size*dt, dt) # 時間軸

    global magnitude
    global sinFreq

    sinBaseFreq = int(2000/(FS/N))

    for i in range(int(in_float.size/N)):
        start = int(i*N)

        f = HAM_WIN*in_float[start:start+N]
        fSp = np.fft.fft(f,n=None)
        ampSp = np.abs(fSp/(N/2))
        ampSum = ampSp[:int(N/2)].sum()
        db = 20*math.log10(ampSum)
        magnitude = np.r_[magnitude,ampSum]
        sinFreqMag = 0.000001
        sinFreqDB = 0
        if ampSum < 0.055:
            roop = 5
            for i in range(roop):
                sinFreqMag += ampSp[int(sinBaseFreq + i - roop/2)]
        # sinFreq = np.r_[sinFreq,sinFreqDB]
        sinFreq = np.r_[sinFreq,sinFreqMag]

    # PowerSpectreArea
    # plt.subplot(3,1,1)
    # plt.ylim([0.0,0.6])
    # plt.plot(t1,magnitude)
    # plt.ylabel('SpectrumArea', fontsize=10)
    # 20kFreqPower
    # plt.subplot(2,1,1)
    plt.ylim([0.0,0.006])
    plt.plot(t2,sinFreq)
    plt.ylabel('Magnitude', fontsize=10)
    # 元信号
    # plt.subplot(2,1,2)
    # plt.ylim([-0.25,0.25])
    # plt.plot(t3,in_float)
    # plt.ylabel('Amplitude', fontsize=10)
    plt.xlabel("Time[sec]", fontsize=10)
    plt.show()


if __name__ == '__main__':
    main()
