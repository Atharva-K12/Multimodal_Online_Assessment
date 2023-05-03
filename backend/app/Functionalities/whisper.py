import whisper

def audioToText(audioFile):
    model = whisper.load_model("base")
    result = model.transcribe(audioFile,fp16=False)
    print(result['text'])
    return result['text']
