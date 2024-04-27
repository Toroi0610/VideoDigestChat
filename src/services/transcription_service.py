import gradio as gr

from src.api.transcribe_api import whisper_cpp_transcribe, whisper_transcribe

def process_video(video_file):
    """
    この関数はアップロードされた動画ファイルを受け取り、
    BytesIOオブジェクトに保存し、そのオブジェクトを返します。
    """

    # ここでBytesIOオブジェクトを使って何か処理を行う
    # 例えば、ビデオの分析、文字起こし、変換など
    # transcript = whisper_cpp_transcribe(video_file)
    transcript = whisper_transcribe(video_file)

    return transcript


if __name__ == "__main__":
    iface = gr.Interface(
        fn=process_video,
        inputs=gr.components.File(label="動画をアップロードしてください", type="binary"),
        outputs="text",
        title="動画アップロードテスト"
    )

    iface.launch()
