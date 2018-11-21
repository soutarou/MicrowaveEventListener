import time
import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

RMS_SIZE = 512

def main():
    rms = np.array([])

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

    powData = in_float*in_float

    N = 1024*4

    v = np.ones(N)/N
    sumData = np.convolve(powData, v, mode='same')  # グラフを描く都合上'same'で。

    sqrtData = np.sqrt(sumData)

    plt.plot(sqrtData)
    plt.show()          # グラフ表示

if __name__ == '__main__':
    main()
