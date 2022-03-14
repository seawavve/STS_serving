import torch 

def get_length(sent1,sent2):
    print(sent1)
    print(sent2)
    return len(sent1) + len(sent2)

def predict_model():
    device = torch.device("cpu")
    PATH = 'model_tutorial.pt'
    model = torch.load(PATH,map_location=torch.device('cpu'))
    