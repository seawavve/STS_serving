from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import torch
import time
from pydantic import BaseModel
from multiprocessing import Pool
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
import json

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


@app.post("/item/")
async def get_text(item:Item):
    start = time.time()
    db = item.dict()
    length = len(db['sentence_1']) + len(db['sentence_2'])
    end = time.time()
    runtime = end - start
    return {'length_result':length, 'runtime(sec)':runtime}

def get_length(sent1,sent2):
    return len(sent1) + len(sent2)

@app.post("/files/")
async def get_json(file: bytes = File(...)):
    start = time.time()
    p=Pool() # 비어 있을 시, cpu_count()가 인자로 들어감
    json_data = json.loads(file)
    json_data = json_data['results']
    ret1 = p.apply_async(get_length,(json_data[0]['sentence1'], json_data[0]['sentence2'],))
    ret2 = p.apply_async(get_length,(json_data[1]['sentence1'], json_data[1]['sentence1'],))
    
    end = time.time()
    runtime = end - start
    p.close()
    p.join()
    return {'runtime(sec)':runtime, 'json_contents': json_data, 'ret1': ret1.get(), 'ret2':ret2.get()}

