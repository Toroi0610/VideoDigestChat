def whisper_transcribe(audio_path):
    # Whisper APIを使って文字起こしを行う
    from openai import OpenAI
    client = OpenAI()
    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    # テキストを取得する
    transcript = transcription.text

    return transcript

def whisper_cpp_transcribe(audio_path):
    # Whisper cppを使って文字起こしを行う
    import pkgutil
    import re
    from pathlib import Path

    # patch whisper on file not find error
    # https://github.com/carloscdias/whisper-cpp-python/pull/12
    try:
       from whisper_cpp_python import Whisper
    except FileNotFoundError:
        regex = r"(\"darwin\":\n\s*lib_ext = \")\.so(\")"
        subst = "\\1.dylib\\2"

        print("fixing and re-importing whisper_cpp_python...")
        # load whisper_cpp_python and substitute .so with .dylib for darwin
        package = pkgutil.get_loader("whisper_cpp_python")
        whisper_path = Path(package.path)
        whisper_cpp_py = whisper_path.parent.joinpath("whisper_cpp.py")
        content = whisper_cpp_py.read_text()
        result = re.sub(regex, subst, content, 0, re.MULTILINE)
        whisper_cpp_py.write_text(result)

        from whisper_cpp_python import Whisper

    whisper = Whisper(model_path="../../whisper.cpp/models/ggml-tiny.bin")
    transcription = whisper.transcribe(open(audio_path, "rb"))

    # テキストを取得する
    transcript = transcription.text

    return transcript


