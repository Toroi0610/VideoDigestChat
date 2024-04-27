from src.api.summarize_api import call_gpt3

def generate_summary(transcript):
    # 要約生成処理を記述する
    response = call_gpt3(text=transcript)

    return response.choices[0].message.content
