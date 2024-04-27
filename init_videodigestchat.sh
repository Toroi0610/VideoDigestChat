#!/bin/bash

# プロジェクトのディレクトリとファイルを生成するスクリプト

# srcディレクトリ内のディレクトリ構造を作成
mkdir -p src/api
mkdir -p src/services

# API関連ファイル
touch src/api/whisper_api.py
touch src/api/gpt3_api.py

# サービス関連ファイル
touch src/services/transcription_service.py
touch src/services/summary_service.py
touch src/services/chat_service.py

# メインファイル
cat << EOF > src/main.py
import gradio as gr
from services.transcription_service import process_video
from services.summary_service import generate_summary
from services.chat_service import generate_chat_response

def main(video, question):
    transcript = process_video(video)
    summary = generate_summary(transcript)
    response = generate_chat_response(transcript, question)
    return summary, response

iface = gr.Interface(
    fn=main,
    inputs=[gr.inputs.Video(label="動画をアップロード"), gr.inputs.Textbox(label="質問を入力")],
    outputs=[gr.outputs.Textbox(label="要約"), gr.outputs.Textbox(label="チャット応答")],
    title="VideoDigestChat"
)

if __name__ == "__main__":
    iface.launch()
EOF

# API ファイルの基本テンプレート
echo "def whisper_transcribe(audio_path):" > src/api/whisper_api.py
echo "    # ここにWhisper APIを使った文字起こしのコードを記述" >> src/api/whisper_api.py

echo "def call_gpt3(text):" > src/api/gpt3_api.py
echo "    # ここにGPT-3.5 Turbo APIを使ったテキスト処理のコードを記述" >> src/api/gpt3_api.py

# サービス ファイルの基本テンプレート
echo "def process_video(video_path):" > src/services/transcription_service.py
echo "    # ここに動画の文字起こし処理を記述" >> src/services/transcription_service.py

echo "def generate_summary(transcript):" > src/services/summary_service.py
echo "    # ここに要約生成処理を記述" >> src/services/summary_service.py

echo "def generate_chat_response(transcript, question):" > src/services/chat_service.py
echo "    # ここにチャット応答生成処理を記述" >> src/services/chat_service.py

# 初期化完了メッセージ
echo "VideoDigestChat project structure within src has been initialized successfully."
