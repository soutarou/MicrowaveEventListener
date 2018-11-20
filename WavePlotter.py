import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():

    args = sys.argv

    path = args[1]

    wf = wave.open(path , "r" )
    buf = wf.readframes(wf.getnframes())
    # バイナリデータを16bit整数に変換
    data = np.frombuffer(buf, dtype="int16")
    np.savetxt("./data/wavfile.csv", data, delimiter=",")
    plt.plot(data)
    plt.show()          # グラフ表示

if __name__ == '__main__':
    main()
