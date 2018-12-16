# MicrowaveEventListener

電子レンジ(Panasonic NE-S26E6)の報知音を検知するためのシステム．他の型での電子レンジでは対応不可．

## 実行環境
- 言語
  - Python3.6
- ライブラリ
  - Python
    - time
    - numpy
    - PyAudio
    - soundfile
- デバイス
  - オーディオインタフェース
    - DUO_CAPTURE 44.1kHz
  - ピエゾセンサ
    - Shadow SH711

## 実行方法

本システムの実行手順は以下の通りである.

1. pythonの環境を整えた後，オーディオインタフェースとピエゾセンサを接続し，soundDevice.pyで対象デバイス番号を確認し，**MicroWaveEventListener.py**の**SOUND_INPUT_DEVICE**の値をその番号に変更
```
python soundDevice.py
```
2. **MicroWaveEventListener.py**の**BROKER**をMQTTBrokerが立っているアドレスに指定(本研究では[mosquitto][mosquitto]を使用してLAN内でBrokerを立てて実行している)
3. 以下のコマンドで実行
```
python MicroWaveEventListener.py
```
4. なにかキー入力をすると終了

MicroWaveEventListener.pyの内部パラメータ**OUT**をTrueにすると，実行終了後に計測した音響信号をwavファイルとして出力する．その場合の実行コマンドは
```
python MicroWaveEventListener.py <出力ファイル名>
```
とすること.出力されたファイルはdataフォルダ直下に書き込まれる.

## ディレクトリ構造
- data
  - 出力ファイルを保存するディレクトリ
- **MicroWaveEventListener.py**
  - 報知音を検知するメインプログラム.
- soundDevice.py
  - 接続サウンドデバイスの確認
- RMSPlotter.py
  - 渡したサウンドファイルのRMS値をプロットするプログラム
- SpectreFeatureProtter.py
  - 渡したサウンドファイルの時間ごとのスペクトログラムの面積の変化と，それによる閾値処置をかけた2kHz付近の振幅スペクトルの強さをプロットするプログラム
- SpectrePlotter.py
  - 渡したファイルの波形とスペクトラムを表示するプログラム．画面下に表示される信号波形の好きなところをクリックするとその時間地点におけるスペクトラムを上に表示する．窓幅1024のハミング窓，サンプリングレートは44.1kHzで固定しているので，それ以外のパラメータのサウンドファイルに使う場合は中身を変えること．
- WavePlotter.py
  - 渡したファイルの信号波形をプロットするプログラム

## 参考にしたページ
- [Pythonで音響信号処理][ref1]

<!-- ref link -->
[mosquitto]:https://mosquitto.org/ "mosquitto"

[ref1]:https://qiita.com/wrist/items/5759f894303e4364ebfd "Pythonで音響信号処理"
