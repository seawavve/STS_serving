import torch 
from sentence_transformers.readers import InputExample
from sentence_transformers import SentenceTransformer

def cosine_similarity(x, y, small_number=1e-8):
  result =  torch.dot(x, y) / (torch.linalg.norm(x) * torch.linalg.norm(y) + small_number)
  return result

def predict_model(sent1,sent2):
    sts_infer_input = InputExample(texts=[sent1, sent2], label=0)
    model_path = "training_sts-Huffon-sentence-klue-roberta-base-2022-03-16_16-35-50"
    model = SentenceTransformer(model_path)
    
    corpus_embeddings = model.encode(sts_infer_input.texts[0], convert_to_tensor=True)
    query_embeddings = model.encode(sts_infer_input.texts[1], convert_to_tensor=True)
    score = cosine_similarity(corpus_embeddings,query_embeddings)

    if score >= 0.6:
        pred = 1
    else:
        pred = 0
    return (float(score),pred)

    
    
