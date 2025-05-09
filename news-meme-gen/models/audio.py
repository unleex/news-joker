from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

import pandas as pd
import torch
from huggingsound import SpeechRecognitionModel
import transformers


class SageFredT5:
    def __init__(self, model_path="ai-forever/sage-fredt5-distilled-95m"):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_path)
        self.model = transformers.AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.model = self.model.to("cuda") if torch.cuda.is_available() else self.model

    def correct_text(self, sentence):
        inputs = self.tokenizer(sentence, max_length=None, padding="longest", truncation=False, return_tensors="pt")
        outputs = self.model.generate(**inputs.to(self.model.device), max_length=inputs["input_ids"].size(1) * 1.5)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]


class SpeechModel:
    def __init__(self):
        self.model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian")
        self.sage = SageFredT5()

    def __call__(self, path):
        transcriptions = self.model.transcribe([path])
        return self.sage.correct_text(transcriptions[0]['transcription'])


class STTGPT:

    def __init__(self, stt, gpt):
        self.stt = stt
        self.gpt = gpt
    
    def __call__(self, audio_path):
        return self.gpt(self.stt(audio_path))