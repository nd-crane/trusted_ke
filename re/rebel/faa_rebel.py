from transformers import AutoConfig, AutoModelForSeq2SeqLM, AutoTokenizer
from time import time
import torch
import pandas as pd
import sys

def load_models():
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    if torch.cuda.is_available():
        _ = model.to("cuda:0") # comment if no GPU available
    _ = model.eval()
    dataset = pd.read_csv('../../data/FAA_data/Maintenance_Text_data_nona.csv')
    return (tokenizer, model, dataset)

def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets


tokenizer, model, dataset = load_models()

# Need hyperparameter search
length_penalty = 10
num_beams = 2
num_return_sequences = 1

gen_kwargs = {
    "max_length": 256,
    "length_penalty": length_penalty,
    "num_beams": num_beams,
    "num_return_sequences": num_return_sequences,
}

results_dict = {"index":[],"input":[], "sentence":[], "head":[], "relation":[], "tail":[]}

for i in range(len(dataset)):
    text = dataset["c119"].iat[i].lower()
    model_inputs = tokenizer(text, max_length=256, padding=True, truncation=True, return_tensors = 'pt')
    generated_tokens = model.generate(
        model_inputs["input_ids"].to(model.device),
        attention_mask=model_inputs["attention_mask"].to(model.device),
        **gen_kwargs,
    )

    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)
    #print('Input text')

    #print(text)

    #print('Prediction text')
    decoded_preds = [text.replace('<s>', '').replace('</s>', '').replace('<pad>', '') for text in decoded_preds]
    print(decoded_preds)

    for idx, sentence in enumerate(decoded_preds):
        triplets = extract_triplets(sentence)
        print(f'Prediction triplets sentence {idx}')
        print(extract_triplets(sentence))
        for triplet in triplets:
            results_dict["index"].append(i)
            results_dict["input"].append(text)
            results_dict["sentence"].append(sentence)
            results_dict["head"].append(triplet["head"])
            results_dict["relation"].append(triplet["type"])
            results_dict["tail"].append(triplet["tail"])
            print(triplet)
            
    length = 50
    fill = "#"
    prefix = "Entries Processed:"
    suffix = ""
    percent = ("{0:.1f}").format(100 * (i / float(len(dataset))))
    filled_length = int(length * i // len(dataset))
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}', )
    sys.stdout.flush()
            
pd.DataFrame(results_dict).to_csv("../../data/FAA_data/rebel/rebel_results_main.csv")