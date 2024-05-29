import torch
from model.model_transformers import  UniRelModel
from predict import UniRel

local = False
if local:
    model_path = "./output/nyt/checkpoint-final"
    unirel = UniRel(model_path=model_path)
else:
    # Load model directly
    #Changed predict.py to accept the UniRel pretrained model
    model = UniRelModel.from_pretrained("vramesh/UniRel-nyt-checkpoint")
    unirel = UniRel(model_path=None, model=model)

# Sample Data to verify that it works, will replace with FAA Data
print(unirel.predict("In perhaps the most ambitious Mekong cruise attempt, Impulse Tourism, an operator based in Chiang Mai, Thailand, is organizing an expedition starting in November in Jinghong, a small city in the Yunnan province in China."))
print(unirel.predict("Adisham Hall in Sri Lanka was constructed between 1927 and 1931 at St Benedicts Monastery , Adisham , Haputhale , Sri Lanka in the Tudor and Jacobean style of architecture"))
print(unirel.predict(["Anson was born in 1979 in Hong Kong.",
    "In perhaps the most ambitious Mekong cruise attempt, Impulse Tourism, an operator based in Chiang Mai, Thailand, is organizing an expedition starting in November in Jinghong, a small city in the Yunnan province in China.",
    "Adisham Hall in Sri Lanka was constructed between 1927 and 1931 at St Benedicts Monastery , Adisham , Haputhale , Sri Lanka in the Tudor and Jacobean style of architecture"
]))
