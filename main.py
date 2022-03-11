from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import torch
import math
import time
from pydantic import BaseModel
from multiprocessing import Pool

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


# @app.post("/items/")
# async def get_text(item:Item):
#     start = time.time()
#     db = item.dict()
#     length = len(db['sentence_1']) + len(db['sentence_2'])
#     end = time.time()
#     runtime = end - start
#     return {'length_result':length, 'runtime(sec)':runtime}

def get_length(sent1,sent2):
    return len(sent1) + len(sent2)

@app.post("/items/")
async def get_json(item:Item):
    start = time.time()
    p=Pool()
    db = item.dict()
    
    length = len(db['sentence_1']) + len(db['sentence_2'])
    ret1 = 1
    ret2 = 2
    ret1 = p.apply(get_length,(db['sentence_1'],db['sentence_2'],))
    ret2 = p.apply(get_length,(db['sentence_1'],db['sentence_1'],))
    
    
    end = time.time()
    runtime = end - start
    p.close()
    p.join()
    return {'length_result':length, 'runtime(sec)':runtime,'ret1': ret1, 'ret2':ret2}
