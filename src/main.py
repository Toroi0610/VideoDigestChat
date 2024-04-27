import os

import gradio as gr
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.services.transcription_service import process_video
from src.services.summary_service import generate_summary
from src.services.chat_service import generate_chat_response

openai_api_key = os.environ["OPENAI_API_KEY"]

def get_text_template(transcript, summary):

    return f"""
{transcript}

つまり，上記は以下のことを言っています．
{summary}
"""

def video_to_summary(video, model_name):
    """Process and transcribe the video at a given url"""
    # Setting qa_chain as a global variable
    global transcript
    global qa_chain

    transcript = process_video(video)
    summary = generate_summary(transcript=transcript)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    text = get_text_template(transcript, summary)
    splits = text_splitter.split_text(text)
    vectordb = FAISS.from_texts(splits, embeddings)
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name=model_name, temperature=0, openai_api_key=openai_api_key),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
    )
    return summary


def response(message, history):
    return qa_chain.run(message)



if __name__ == "__main__":
    transcribe_interface = gr.Interface(
        fn=video_to_summary,
        inputs=[
            gr.Video(label="動画をアップロード"),
            gr.components.Radio(
                [
                    'gpt-3.5-turbo',
                    'gpt-3.5-turbo-16k',
                    'gpt-4'
                ]
            )
        ],
        outputs=gr.Textbox(label="transcript"),
        title="VideoDigestChat"
    )

    chat_interface = gr.ChatInterface(
        fn=response,
        title="Chat",
        description="Chat with AI about the video you just summraized."
    )
    demo = gr.TabbedInterface([transcribe_interface, chat_interface], ["Transcribe & Summarize", "Chat"])
    demo.queue()
    demo.launch()
