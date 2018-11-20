import time

import numpy as np

import soundfile as sf
import pyaudio as pa

SOUND_INPUT_DEVICE = 2;
CHUNK_SIZE = 1024

# global
xs = np.array([]) #サウンド出力用
rms_buffSize = 0 #RMS窓のバッファ
sum_power = 0 #RMS窓でのパワーの合計

def callback(in_data, frame_count, time_info, status):
    global xs
    global rms_buffSize
    global sum_power

    # short型のデータバッファをfloatに
    in_float = np.frombuffer(in_data, dtype=np.int16).astype(np.float)
    # 値の範囲を-1.0 ~ 1,0に
    in_float[in_float > 0.0] /= float(2**15 - 1)
    in_float[in_float <= 0.0] /= float(2**15)

    rms_buffSize += in_float.size

    power = in_float*in_float
    sum_power += power.sum()

    # print("buffSize > ",rms_buffSize)
    # print("power > ",sum_power)
    rms = -1
    if rms_buffSize >= CHUNK_SIZE*4:
        rms = np.sqrt(sum_power/rms_buffSize)
        print(rms)
        sum_power = 0
        rms_buffSize = 0

    # 入力音をサウンドファイルとして出力するならコメントアウトを外す
    xs = np.r_[xs, in_float]

    return (in_data, pa.paContinue)

if __name__ == "__main__":
    # pyaudio
    p_in = pa.PyAudio()
    py_format = p_in.get_format_from_width(2)
    fs = 16000
    channels = 1
    chunk = CHUNK_SIZE

    # 入力ストリームを作成
    in_stream = p_in.open(format=py_format,
                          channels=channels,
                          rate=fs,
                          input=True,
                          frames_per_buffer=chunk,
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

    # 入力信号を保存
    sf.write("./pyaudio_output.wav", xs, fs)

    p_in.terminate()
