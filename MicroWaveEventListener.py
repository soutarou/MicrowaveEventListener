import time

import numpy as np

import soundfile as sf
import pyaudio as pa

import sys

# 使うサウンドデバイス番号に合わせて変える
# サウンドデバイス番号の確認はsoundDevice.pyで行う
SOUND_INPUT_DEVICE = 0;
CHUNK_SIZE = 1024
RMS_BUFFSIZE = CHUNK_SIZE*4

OUT = True

# global
xs = np.array([]) #サウンド出力用
rmsDatas = np.array([]) #rms値のcsv出力用
powerQueue = np.zeros(4) # chunkでの内積合計のキュー
sum_rms_power = 0 #RMS窓での内積の合計

def queue(data,input):
    dst = np.roll(data,-1)
    dst[-1] = input
    return dst

def callback(in_data, frame_count, time_info, status):
    global powerQueue
    global sum_rms_power

    # short型のデータバッファをfloatに
    in_float = np.frombuffer(in_data, dtype=np.int16).astype(np.float)
    # 値の範囲を-1.0 ~ 1,0に変換
    in_float[in_float > 0.0] /= float(2**15 - 1)
    in_float[in_float <= 0.0] /= float(2**15)

    #chunk内の内積を計算
    power = in_float*in_float
    sum_power = power.sum()

    #RMS窓内の内積を計算
    sum_rms_power += sum_power
    sum_rms_power -= powerQueue[0]

    #chunkの内積をキューに追加し、先頭の要素を削除
    powerQueue = queue(powerQueue,sum_power)

    #RMS値を計算
    rms = np.sqrt(sum_rms_power/RMS_BUFFSIZE)

    if OUT:
        global xs
        global rmsDatas
        xs = np.r_[xs, in_float]
        rmsDatas = np.r_[rmsDatas, rms]

    return (in_data, pa.paContinue)

if __name__ == "__main__":

    args = sys.argv

    if OUT and len(args) < 2:
            print("ラベル名を指定してください.")
            print(" > python MicroWaveEventListener.py microwave")
            exit()

    p_in = pa.PyAudio()
    py_format = p_in.get_format_from_width(2)
    fs = 16000
    channels = 1

    # 入力ストリームを作成
    in_stream = p_in.open(format=py_format,
                          channels=channels,
                          rate=fs,
                          input=True,
                          frames_per_buffer=CHUNK_SIZE,
                          input_device_index=SOUND_INPUT_DEVICE,
                          stream_callback=callback)

    in_stream.start_stream()

    # input loop
    # 何か入力したら終了
    while in_stream.is_active():
        c = input('>> ')
        if c:
            break
        time.sleep(0.1)
    else:
        in_stream.stop_stream()
        in_stream.close()

    if OUT:
        # 入力信号を保存
        wavPath = "./data/" + args[1] + "_sound.wav"
        csvPath = "./data/" + args[1] + "_rms.csv"
        sf.write(wavPath, xs, fs)
        np.savetxt(csvPath, rmsDatas, delimiter=",")

    p_in.terminate()
