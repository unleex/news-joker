#!pip install accelerate bitsandbytes transformers torch  НУЖНЫ БИБЛИОТЕКИ

# Исключительно ознакомительный пример.
# НЕ НАДО ТАК ИНФЕРИТЬ МОДЕЛЬ В ПРОДЕ.
# Когда есть https://github.com/vllm-project/vllm


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, T5ForConditionalGeneration, BitsAndBytesConfig 

model_saiga_name = "IlyaGusev/saiga_llama3_8b"
DEFAULT_SYSTEM_PROMPT = "Ты — русскоязычный стендап комик. Ты получаешь новостной заголовок и создаешь по нему шутку."
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_quant_type="nf8",
    bnb_8bit_use_double_quant=True,
)
model_saiga = AutoModelForCausalLM.from_pretrained(
    model_saiga_name,
    quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="cuda"
)
tokenizer_saiga = AutoTokenizer.from_pretrained(model_saiga_name)
generation_config_saiga = GenerationConfig.from_pretrained(model_saiga_name)

def saiga(prompt):
    prompt = tokenizer_saiga.apply_chat_template([{
        "role": "system",
        "content": DEFAULT_SYSTEM_PROMPT
    }, {
        "role": "user",
        "content": prompt
    }], tokenize=False, add_generation_prompt=True)
    data = tokenizer_saiga(prompt, return_tensors="pt", add_special_tokens=False)
    data = {k: v.to(model_saiga.device) for k, v in data.items()}
    output_ids = model_saiga.generate(**data, generation_config=generation_config_saiga)[0]
    output_ids = output_ids[len(data["input_ids"][0]):]
    output = tokenizer_saiga.decode(output_ids, skip_special_tokens=True).strip()
    return output


def saiga_three_times(prompt):
    result=[] 
    inputs = [prompt]*3
    for query in inputs:
        result += [saiga(query)]
    return result

model_name_sum = "IlyaGusev/rut5_base_sum_gazeta"
tokenizer_sum = AutoTokenizer.from_pretrained(model_name_sum)
model_sum = T5ForConditionalGeneration.from_pretrained(model_name_sum)

def summarize(
        article_text: str,
          max_output_length: int=50, 
          min_output_length: int=10, 
          max_tokenizer_length: int=60,
          ):
    input_ids = tokenizer_sum(
        [article_text],
        max_length=max_tokenizer_length,
        add_special_tokens=True,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )["input_ids"]


    output_ids = model_sum.generate(
        max_length=max_output_length,
        min_length=min_output_length,
        input_ids=input_ids,
        no_repeat_ngram_size=4
    )[0]

    summary = tokenizer_sum.decode(output_ids, skip_special_tokens=True)
    summary = summary.split(".")[0].strip() + "."
    return summary

def summarized_saiga(prompt, summarize_threshold = 52):
    len_tok  = len(tokenizer_saiga.encode(prompt))
    if len_tok > summarize_threshold:
        summ = summarize(prompt)
        print('summarizing..')
    else:
        summ = prompt
        print('not summarizing!')
    saiga_ans = saiga(summ)
    return saiga_ans

if __name__ == "__main__":
    prompt=input()  #СЮДА НОВОСТЬ
    result=[] # ЗДЕСЬ БУДЕТ РЕЗУЛЬТАТ

    result = summarized_saiga(prompt)
    print(result)