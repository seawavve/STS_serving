import torch 
from sentence_transformers.readers import InputExample
from sentence_transformers import SentenceTransformer

def get_length(sent1,sent2):
    print(sent1)
    print(sent2)
    return len(sent1) + len(sent2)

def cosine_similarity_manual(x, y, small_number=1e-8):
  result =  torch.dot(x, y) / (torch.linalg.norm(x) * torch.linalg.norm(y) + small_number)
  return result

def predict_model(sent1,sent2):
    # sent1 = '무엇보다도 호스트분들이 너무 친절하셨습니다.'
    # sent2 = '무엇보다도, 호스트들은 매우 친절했습니다.'
    # predict = 0
    
    # device = torch.device("cpu")
    # PATH = 'model_tutorial.pt'
    # model = torch.load(PATH,map_location=torch.device('cpu'))
    sts_infer_input = InputExample(texts=[sent1, sent2], label=0)
    model_path = "training_sts-Huffon-sentence-klue-roberta-base-2022-03-16_16-35-50"
    model = SentenceTransformer(model_path)
    # embedding 계산
    corpus_embeddings = model.encode(sts_infer_input.texts[0], convert_to_tensor=True)
    query_embeddings = model.encode(sts_infer_input.texts[1], convert_to_tensor=True)
    print(corpus_embeddings.shape)
    print(query_embeddings.shape)

    score = cosine_similarity_manual(corpus_embeddings,query_embeddings)
    print(score)

    if score >= 0.6:
        pred = 1
    else:
        pred = 0

    # print(pred)
    
    