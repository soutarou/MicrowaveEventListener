import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

FS = 44100

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
    t = np.arange(0, in_float.size*dt, dt) # 時間軸

    plt.ylim([-0.25,0.25])
    plt.plot(t,in_float)
    plt.ylabel('Amplitude', fontsize=10)
    plt.xlabel("Time[sec]", fontsize=10)
    plt.show()          # グラフ表示

if __name__ == '__main__':
    main()
