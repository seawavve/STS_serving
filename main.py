# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import torch
import time
from pydantic import BaseModel
import multiprocessing
from multiprocessing import Pool
from fastapi import FastAPI, File, UploadFile
import json
from content import predict_model

app = FastAPI()
db = dict()

class Item(BaseModel):
    sentence_1: str
    sentence_2: str

@app.post("/pred/file/")
async def predict_json(file: bytes = File(...)):
    start = time.time()
    cpu_count = multiprocessing.cpu_count()
    print(cpu_count)
    p=Pool() # 비어 있을 시, cpu_count()가 인자로 들어감
    preds=list()
    scores=list()
    sentences=list()

    json_data = json.loads(file)
    json_data = json_data['results']

    for i in range(len(json_data)//1):
        texts = json_data[i:i+1]
        # Singleprocessing with 1 Processor
        result1 = p.apply_async(predict_model,(texts[0]['sentence1'],texts[0]['sentence2'],))
        score1,pred1 = result1.get()

        sentences.append([texts[0]['sentence1'],texts[0]['sentence2']])
        preds.append(pred1)
        scores.append(score1)

    end = time.time()
    runtime = end - start
    p.close()
    p.join()
    return {'sentences':sentences,'preds':preds,'scores':scores, 'runtime(sec)':runtime}


@app.post("/pred/file/multi/")
async def predict_json_multiprocessing(file: bytes = File(...)):
    start = time.time()
    cpu_count = multiprocessing.cpu_count()
    p=Pool() # 비어 있을 시, cpu_count()가 인자로 들어감
    preds=list()
    scores=list()
    sentences=list()

    json_data = json.loads(file)
    json_data = json_data['results']
    
    for i in range(len(json_data)//2): 
        texts = json_data[(i*2):(i*2)+2]
        # Multiprocessing with 2 Processor
        result1 = p.apply_async(predict_model,(texts[0]['sentence1'],texts[0]['sentence2'],))
        result2 = p.apply_async(predict_model,(texts[1]['sentence1'],texts[1]['sentence2'],))

        score1,pred1 = result1.get()
        score2,pred2 = result2.get()

        sentences.extend([[texts[0]['sentence1'],texts[0]['sentence2']],[texts[1]['sentence1'],texts[1]['sentence2']]])
        preds.extend([pred1,pred2])
        scores.extend([score1,score2])
    
    end = time.time()
    runtime = end - start
    p.close()
    p.join()
    return {'sentences':sentences,'preds':preds,'scores':scores, 'runtime(sec)':runtime}

@app.post("/pred/sentences")
async def predict_sentences(item:Item):
    start = time.time()
    texts = item.dict() 
    sent1 = texts['sentence_1']
    sent2 = texts['sentence_2']
    score,pred = predict_model(sent1,sent2)
    end = time.time()
    runtime = end - start
    return {'sentence_1':sent1, 'sentence_2':sent2, 'score':score, 'pred':pred, 'runtime(sec)':runtime}

