from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

import pandas as pd
import torch
# from huggingsound import SpeechRecognitionModel
# import transformers


class NaebNet:

    def __init__(self, text_model, audio_model, image_model):
        self.text_model = text_model
        self.audio_model = audio_model
        self.image_model = image_model

    def text(self, prompt: str):
        return self.text_model(prompt)
    
    def audio(self, audio_path):
        return self.audio_model(audio_path)
    
    def image(self, image_path, save_to):
        self.image_model(image_path, save_to)