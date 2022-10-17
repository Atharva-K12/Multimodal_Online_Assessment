import whisper


# use openAI whisper to convert speech to text

def useWhisper(audioFile):
    model = whisper.load_model("base")
    result = model.transcribe(audioFile,fp16=False)
    print(result["text"])
    

if __name__ == "__main__":
    useWhisper("m1.mp3")




    