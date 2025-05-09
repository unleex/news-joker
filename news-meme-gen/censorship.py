import torch
import numpy as np
import pandas as pd
from torch import nn
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.exceptions import NotFittedError

# 1. Загрузка необходимых компонентов -------------------------------------------------

class TextClassifier(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=128,
            num_layers=1,
            bidirectional=True,
            batch_first=True
        )
        self.classifier = nn.Sequential(
            nn.Linear(2*128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 2)
        )
        
    def forward(self, x):
        x = x.unsqueeze(1)  # [batch_size, 1, input_size]
        _, (hidden, _) = self.lstm(x)
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.classifier(hidden)

# 2. Функция для загрузки модели и векторизатора ----------------------------------------
def load_resources(model_path='/kaggle/working/text_classifier.pth',
                   vectorizer_path='/kaggle/working/vectorizer.pkl'):
    try:
        # Загрузка векторизатора с проверкой
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
            
        # Проверка, что векторизатор обучен
        if not hasattr(vectorizer, 'vocabulary_'):
            raise NotFittedError("Vectorizer not fitted!")
            
        # Загрузка модели с обработкой предупреждения безопасности
        model = TextClassifier(input_size=len(vectorizer.get_feature_names_out()))
        model.load_state_dict(
            torch.load(model_path, map_location='cpu', weights_only=True)
        )
        model.eval()
        
        return model, vectorizer
        
    except Exception as e:
        raise RuntimeError(f"Error loading resources: {str(e)}")

model, vectorizer = load_resources(
            model_path='models/text_classifier(1).pth',
            vectorizer_path='models/vectorizer.pkl'
        )

def predict(text, model, vectorizer):
    try:
        # Преобразование текста
        text_vector = vectorizer.transform([text])
        
        # Конвертация в тензор
        tensor = torch.tensor(text_vector.toarray(), dtype=torch.float32)
        
        # Предсказание
        with torch.no_grad():
            output = model(tensor)
            probabilities = torch.softmax(output, dim=1)
            
        return {
            'class': torch.argmax(probabilities).item(),
            'probabilities': probabilities.numpy()[0].tolist()
        }
        
    except Exception as e:
        raise RuntimeError(f"Prediction error: {str(e)}")


def must_be_censored(text,thresh=0.5):
    res = predict(text,model, vectorizer)['probabilities'][0]
    print(f"must be censored prob: {res}")
    return res > thresh


# 4. Пример использования -------------------------------------------------------
if __name__ == "__main__":
    try:
        # Загрузка модели и векторизатора
        
        
        # Тестовый пример
        test_text = input()
        result = predict(test_text, model, vectorizer)
        
        print("Результат классификации:")
        print(f"Класс: {result['class']}")
        print(f"Вероятности: {dict(zip([0,1], result['probabilities']))}")
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")