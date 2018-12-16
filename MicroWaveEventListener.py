import time
import numpy as np
import soundfile as sf
import pyaudio as pa
import math
import sys
import paho.mqtt.client as mqtt

# 使うサウンドデバイス番号に合わせて変える
# サウンドデバイス番号の確認はsoundDevice.pyで行う
SOUND_INPUT_DEVICE = 2;
CHUNK_SIZE = 1024
HAM_WIN = np.hamming(CHUNK_SIZE)

FS = 44100
CHANNELS = 1

BROKER = "192.168.11.4"
PORT = 1883
TOPIC = "nmServer/notify"

OUT = False
DEBUG = False

xs = np.array([]) #サウンド出力用
rmsDatas = np.array([]) #rms値のcsv出力用

mqttClient = mqtt.Client(protocol=mqtt.MQTTv311)

mwEventFlag = False
flagSetTime = 0
mwCompleteFlag = False
completeTime = 0

eventNotify = False
notifyTime = 0

def nowMili():
    return int(time.time()*1000)

def queue(data,input):
    dst = np.roll(data,-1)
    dst[-1] = input
    return dst

def eventHandle(sinFreqMag):
    global mwEventFlag
    global flagSetTime
    global mwCompleteFlag
    global completeTime
    threshold = 0.0007

    now = nowMili()
    # print(sinFreqMag)
    if now - completeTime > 1000:
        mwCompleteFlag = False

    if not mwEventFlag:
        if sinFreqMag >= threshold:
            mwEventFlag = True
            flagSetTime = now
    else:
        if sinFreqMag < threshold:
            mwEventFlag = False
            lapse = now - flagSetTime
            print("lapse > ",lapse)
            if 200 < lapse < 400:
                if not mwCompleteFlag:
                    print("報知音検知")
                    mqttClient.publish(TOPIC, "MICROWAVE/warmComplete/1")
                    mwCompleteFlag = True
                completeTime = now


def callback(in_data, frame_count, time_info, status):

    # short型のデータバッファをfloatに
    in_float = np.frombuffer(in_data, dtype=np.int16).astype(np.float)
    # 値の範囲を-1.0 ~ 1,0に変換
    in_float[in_float > 0.0] /= float(2**15 - 1)
    in_float[in_float <= 0.0] /= float(2**15)

    fSp = np.fft.fft(HAM_WIN*in_float,n=None)
    ampSp = np.abs(fSp/(CHUNK_SIZE/2))
    ampSum = ampSp[:int(CHUNK_SIZE/2)].sum()

    # 2kHz付近の強さ
    sinBaseFreq = int(2000/(FS/CHUNK_SIZE))
    sinFreqMag = 0

    if ampSum < 0.055:
        roop = 5
        for i in range(roop):
            sinFreqMag += ampSp[int(sinBaseFreq + i - roop/2)]

    if DEBUG:
        print("スペクトログラム面積 > ",ampSum)
        print(sinFreqMag)

    eventHandle(sinFreqMag)


    if OUT:
        global xs
        global rmsDatas
        xs = np.r_[xs, in_float]
        rmsDatas = np.r_[rmsDatas, rmsDB]

    return (in_data, pa.paContinue)

if __name__ == "__main__":

    args = sys.argv

    if OUT and len(args) < 2:
            print("ラベル名を指定してください.")
            print(" > python MicroWaveEventListener.py microwave")
            exit()

    mqttClient.connect(BROKER, port=PORT, keepalive=60)

    p_in = pa.PyAudio()
    py_format = p_in.get_format_from_width(2)

    # 入力ストリームを作成
    in_stream = p_in.open(format=py_format,
                          channels=CHANNELS,
                          rate=FS,
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
        sf.write(wavPath, xs, FS)
        # csvPath = "./data/" + args[1] + "_data.csv"
        # np.savetxt(csvPath, rmsDatas, delimiter=",")

    p_in.terminate()
    mqttClient.disconnect()
