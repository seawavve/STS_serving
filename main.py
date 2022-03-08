from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    sentence_1: str
    sentence_2: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
def get_text(item:Item):
    item_dict = item.dict()
    print(item_dict)
    # get 2 line text
    # image = np.array(Image.open(file.file))
    # model = config.STYLES[style]
    # output, resized = inference.inference(model, image)
    # name = f"/storage/{str(uuid.uuid4())}.jpg"
    # cv2.imwrite(name, output)
    return item

# model inference