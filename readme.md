# STS Model Serving
FastAPI 프레임워크를 사용하여 sentence-klue-roberta-base 모델을 서빙했습니다. 본 모델은 두 문장의 유사도를 반환하는 STS(Sentence Textual Similarity) Task 모델입니다. 두 문장이 들어오면 이를 RestAPI로 inference 결과를 반환합니다. 위 코드는 모듈화 되어 있습니다.

## Code Description
`main.py`는 총 세 가지 기능을 제공합니다. 가장 기본적인 STS Model Serving 기능은 predict_json입니다. 대용량 데이터 처리를 위한 기능은 predict_json_multiprocessing과 predict_sentences입니다. 대용량 데이터를 inference 하는데에 효율적으로 처리하기 위해서 여러 프로세스를 병렬적으로 사용하는 멀티프로세싱 기능을 지원합니다. 일정 데이터 개수 이하의 데이터를 처리한다면 오버헤드 문제로 싱글프로세싱을 사용하는게 더 시간이 적게 드는 Case도 고려하여 predict_json을 개발했습니다. 데이터 양에 따라 나누어서 사용하시면 됩니다. json_data 형식은 sample_data.json 파일을 참고하세요.  
- predict_sentences  
  하나의 문장쌍을 입력받아 Inference 값을 반환하는 기능  
- predict_json_multiprocessing  
  json 파일로 여러 개의 문장쌍 데이터를 입력받아 Inference 값을 반환하는 기능  
- predict_json  
  json 파일로 여러 개의 문장쌍 데이터를 입력받아 MultiProcessing으로 Inference 값을 반환하는 기능  
  

`content.py`는 메인 코드를 돌리기 위한 모듈입니다. main에서 두 문장을 받아와 predict_model 함수에서 모델 Inference 값을 반환합니다. 모델을 불러와 두 문장이 학습된 모델에 맞추어 벡터로 변환하여 코사인 유사도 계산을 통해 문장 유사도 값을 도출합니다.  
- cosine_similarity  
  두 문장의 임베딩 벡터로 코사인 유사도를 구하는 함수   
- predict_model  
  모델 Inference 함수  
  


## How to Run
``` 
git clone https://github.com/seawavve/STS_serving
cd STS_serving
pip install -r requirements.txt
unzip training_sts-Huffon-sentence-klue-roberta-base-2022-03-16_16-35-50.zip
```
본 Repository를 clone하여 로컬에 생성합니다. 폴더에 들어가 requirements.txt 파일을 읽어 환경을 설정합니다. 모델 파일 압축을 해제하여 사용할 모델을 세팅합니다.

모델 파일 주소 ##########  
위 주소에서 모델 파일을 다운받아 Repository내에 추가합니다.  

```
uvicorn main:app --reload
```
FastAPI Code를 실행합니다. `http://127.0.0.1:8000/docs#/` URL 로 Swagger UI에 접속해 세 가지 모듈 중에 원하는 기능을 실행합니다. 기본 기능은 predict_sentences입니다.  




