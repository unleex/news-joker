from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

import pandas as pd
import torch
# from huggingsound import SpeechRecognitionModel
# import transformers


class GigaChatModel():

    def __init__(
            self, 
            credentials: str, 
            system_prompt: str | None = None,
            temperature: float = 0.7,
            max_tokens: int = 100,
            verify_ssl_certs: bool = False
            ):
        self.model = GigaChat(
            credentials=credentials,
            verify_ssl_certs=verify_ssl_certs
        )
        self.payload = Chat(
            messages=[
                Messages(
                role=MessagesRole.SYSTEM,
                content=system_prompt
            ) 
            ] if system_prompt is not None else [],
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def __call__(self, text: str, remember: bool = True): 
        self.payload.messages.append(
            Messages(role=MessagesRole.USER, content=text)
            )
        try:
            response = self.model.chat(self.payload)
        except Exception as e:
            print(f"An exception occured from Gigachat API!: {e}")
        message = response.choices[0].message
        if remember:
            self.payload.messages.append(message)
        else:
            # remove prompt
            self.payload.messages.pop()
        return message.content


class GPT:

    def __init__(
            self, 
            model_path="IlyaGusev/saiga_llama3_8b", 
            system_prompt: str | None = None,
            ):
        # Use a pipeline as a high-level helper
        self.system_prompt = system_prompt
        self.pipe = transformers.pipeline("text-generation", model=model_path)

    def __call__(self, input: str):
        if self.system_prompt:
            input = f"{self.system_prompt}\n{input}"
        return self.pipe(input)
    
import transformers
import re
from typing import Optional, Union, List, Dict

class BaseTextProcessor:
    """Базовый класс для обработки текста"""
    _DEFAULT_DEVICE = "auto"
    
    def __init__(self, system_prompt: Optional[str] = None):
        self._system_template = system_prompt
        self._validation_registry = []
        
    def _preprocess_input(self, raw_text: str) -> str:
        if self._system_template:
            return f"[SYSTEM]{self._system_template}[/SYSTEM]\n[USER]{raw_text}[/USER]"
        return raw_text
    
    def _validate_parameters(self) -> None:
        for validator in self._validation_registry:
            validator()

class TextGenerationCore(BaseTextProcessor):
    """Ядро для генерации текста с расширенными функциями"""
    
    def __init__(
        self,
        model_path: str = "EgoriK007lol7/Saiga_llama3_8b_8bit",
        system_prompt: Optional[str] = None,
        generation_params: Optional[Dict] = None
    ):
        super().__init__(system_prompt)
        self._model_identifier = model_path
        self._generation_config = self._configure_generation(generation_params)
        self._initialize_pipeline()
        
    def _configure_generation(self, params: Optional[Dict]) -> Dict:
        default_params = {
            'max_length': 512,
            'temperature': 0.7,
            'top_p': 0.9,
            'repetition_penalty': 1.1
        }
        return {**default_params, **(params or {})}
    
    def _initialize_pipeline(self) -> None:
        self._text_engine = transformers.pipeline(
            task="text-generation",
            model=self._model_identifier,
            device=self._DEFAULT_DEVICE
        )
        
    def generate(self, input_text: str) -> List[Dict]:
        processed_input = self._preprocess_input(input_text)
        self._validate_parameters()
        return self._text_engine(processed_input, **self._generation_config)

class Saiga_tune(TextGenerationCore):
    
    def __init__(
        self,
        model_path: str = "EgoriK007lol7/Saiga_llama3_8b_8bit",
        system_prompt: Optional[str] = None,
        enable_creative_mode: bool = False
    ):
        generation_params = {'temperature': 0.9} if enable_creative_mode else None
        super().__init__(model_path, system_prompt, generation_params)
        self._register_validators()
        
    def _register_validators(self) -> None:
        self._validation_registry.append(self._check_model_compatibility)
        
    def _check_model_compatibility(self) -> None:
        if "llama3" not in self._model_identifier.lower():
            raise ValueError("Несовместимая архитектура модели")
            
    def __call__(self, input: str) -> str:
        outputs = self.generate(input)
        return self._postprocess_output(outputs[0]['generated_text'])
    
    def _postprocess_output(self, raw_output: str) -> str:
        return raw_output.split("[/USER]")[-1].strip()

class TextEvaluationEngine(BaseTextProcessor):
    
    def __init__(
        self,
        model_path: str = "Qwen/Qwen2.5-7B-Instruct-1M",
        system_prompt: Optional[str] = None,
        evaluation_mode: str = "detailed"
    ):
        super().__init__(system_prompt)
        self._scoring_model = model_path
        self._evaluation_strategy = evaluation_mode
        self._setup_evaluation_system()
        
    def _setup_evaluation_system(self) -> None:
        self._analyzer = transformers.pipeline(
            task="text-generation",
            model=self._scoring_model,
            device=self._DEFAULT_DEVICE
        )
        
    def _calculate_score(self, evaluation_text: str) -> float:
        numbers = re.findall(r"\d+\.?\d*", evaluation_text)
        return float(numbers[0])/10 if numbers else 0.0
        
    def evaluate(self, text_to_analyze: str) -> Dict:
        processed_input = self._preprocess_input(text_to_analyze)
        analysis_result = self._analyzer(processed_input)[0]['generated_text']
        return {
            'raw_evaluation': analysis_result,
            'numeric_score': self._calculate_score(analysis_result)
        }

class Qwen(TextEvaluationEngine):
    """Многофункциональная система оценки контента"""
    
    def __init__(
        self,
        model_path: str = "Qwen/Qwen2.5-7B-Instruct-1M",
        system_prompt: Optional[str] = None,
        evaluation_scale: str = "10-point"
    ):
        super().__init__(model_path, system_prompt)
        self._rating_scale = evaluation_scale
        self._configure_evaluation_prompts()
        
            
    def __call__(self, input: str) -> dict:
        return self.evaluate(input)
    
    def detailed_analysis(self, text: str) -> List[str]:

        result = self.evaluate(text)
        
        return result['raw_evaluation'].split("\n")