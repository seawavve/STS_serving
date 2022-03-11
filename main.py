from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import torch
import math
import time
from pydantic import BaseModel

app = FastAPI()
db = dict()

class Item(BaseModel):
    sentence_1: str
    sentence_2: str

# @app.get("/")
# async def show_2sent():
    
#     sents = db
#     return sents

# @app.get("/predict")
# async def predict(db):
#     PATH = 'model_tutorial.pt'
#     model = torch.load(PATH)
#     model.eval()
#     logits = model(db.values())
#     return logits
# #     model = 'model_tutorial.pt'
# #     predict_result = inference.inference(model,db.values())
# #     return {'sentences':db,'predict_result':predict_result}


@app.post("/items/")
def get_text(item:Item):
    start = time.time()
    db = item.dict()
    length = len(db['sentence_1']) + len(db['sentence_2'])
    end = time.time()
    runtime = end - start
    return {'length_result':length, 'runtime(sec)':runtime}

# model inference