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
