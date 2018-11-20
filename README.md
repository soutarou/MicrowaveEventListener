# MicrowaveEventListener

京都産業大学実験住宅における電子レンジ(Panasonic NE-S26E6)の報知音を検知するためのシステム

- 実行環境
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


- ディレクトリ構造
  - data
    - 出力ファイルを保存するディレクトリ
  - MicroWaveEventListener.py
    - 報知音を検知するメインプログラム
  - soundDevice.py
    - 接続サウンドデバイスの確認用
