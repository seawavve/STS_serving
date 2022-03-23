# **STS Model Serving**

FastAPI 프레임워크를 사용하여 sentence-klue-roberta-base 모델을 서빙했습니다. 본 모델은 두 문장의 유사도를 반환하는 STS(Sentence Textual Similarity) Task 모델입니다. 두 문장이 들어오면 이를 RestAPI로 inference 결과를 반환합니다. 위 코드는 모듈화 되어 있습니다. Model을 서빙하기위해 Python 기반 백앤드 프레임워크를 고민했습니다. 우수한 공식 문서와 큰 생태계를 갖고 있는 장고 프레임워크와 직관적이고 가벼운 플라스크 프레임워크를 고려했습니다. 고민 끝에 비교적 속도가 빠른 FastAPI 프레임워크를 선택했습니다.

## **How to Run(Conda)**

1. Repository clone
    본 Repository를 clone하여 로컬에 생성합니다. 폴더에 들어가 모델 파일 압축을 해제하여 사용할 모델을 세팅합니다.
    ```
    git clone https://github.com/seawavve/STS_serving
    cd STS_serving
    unzip training_sts-Huffon-sentence-klue-roberta-base-2022-03-16_16-35-50.zip
    ```
    

2. 환경 생성
    conda로 가상환경을 설정합니다. requirements.txt 파일을 읽어 sts-serving conda 환경을 설정합니다. 

    ```
    conda create -n sts-serving python=3.8
    conda activate sts-serving
    conda install --file requirements.txt
    conda install -c powerai sentencepiece
    ```
    위 방식이 실행되지 않는다면 아래 코드를 실행해주세요.

   
    ```
    pip install -r requirements.text
    ```

    or

    ```
    pip3 install -r requirements.text
    ```

3. Server Code
   FastAPI Code를 실행합니다.
    ```
    uvicorn main:app --reload
    ```
    



4. URL 접속 `http://127.0.0.1:8000/docs#/` URL 로 Swagger UI에 접속해 세 가지 모듈 중에 원하는 기능을 실행합니다. 기본 기능은 predict_sentences입니다.
    
    ![https://user-images.githubusercontent.com/66352658/159536641-63cd6e61-4b0c-4766-a8b3-cfbba6ec654a.png](https://user-images.githubusercontent.com/66352658/159536641-63cd6e61-4b0c-4766-a8b3-cfbba6ec654a.png)
    
5. Usage
- predict_sentences (/pred/sentences/)Try it Out -> "sentence_1": "string"의 "string"에 한국어 문장1 삽입 & "sentence_2": "string"의 "string"에 한국어 문장2 삽입 -> Execute결과는 Response Body에서 확인할 수 있습니다.
    
    ![https://user-images.githubusercontent.com/66352658/159537841-89fbbb9d-be7e-405d-afa6-a80baf649ab7.png](https://user-images.githubusercontent.com/66352658/159537841-89fbbb9d-be7e-405d-afa6-a80baf649ab7.png)
    
- predict_json_multiprocessing (/pred/file/)  
  Try it Out -> sample_data.json 삽입 -> Execute  
  결과는 Response Body에서 확인할 수 있습니다.  
    
    ![https://user-images.githubusercontent.com/66352658/159538459-5116948b-8c2e-4f51-97bf-26c5a39bb193.png](https://user-images.githubusercontent.com/66352658/159538459-5116948b-8c2e-4f51-97bf-26c5a39bb193.png)
    
- predict_json (/pred/multi/)  
  Try it Out -> sample_data.json 삽입 -> Execute  
  결과는 Response Body에서 확인할 수 있습니다.  
    
    ![https://user-images.githubusercontent.com/66352658/159538640-534d0597-f2a3-449b-8c54-63485e2a7bc4.png](https://user-images.githubusercontent.com/66352658/159538640-534d0597-f2a3-449b-8c54-63485e2a7bc4.png)
    

## **Execution Result**

main.py로 두 문장을 넣어 predict_sentences를 실행한 결과입니다. 변수로 주어진 문장(sentence),두 문장의 코사인 유사도 실수값(score), binary 유사도 값(pred), 코드 런타임(runtime)입니다.

![https://github.com/seawavve/STS_serving/raw/master/execution_result.png](https://github.com/seawavve/STS_serving/raw/master/execution_result.png)

## **Code Description**

`main.py`는 총 세 가지 비동기 기능을 제공합니다. 가장 기본적인 STS Model Serving 기능은 predict_json입니다. 평귱 1.3초 소요됩니다. 대용량 데이터 처리를 위한 기능은 predict_json_multiprocessing과 predict_sentences입니다. 대용량 데이터를 inference 하는데에 효율적으로 처리하기 위해서 여러 프로세스를 병렬적으로 사용하는 멀티프로세싱 기능을 지원합니다. 일정 데이터 개수 이하의 데이터를 처리한다면 오버헤드 문제로 싱글프로세싱을 사용하는게 더 시간이 적게 드는 Case도 고려하여 predict_json을 개발했습니다. 데이터 양에 따라 나누어서 사용하시면 됩니다. json_data 형식은 sample_data.json 파일을 참고하세요.

- predict_sentences하나의 문장쌍을 입력받아 Inference 값을 반환하는 기능
- predict_json_multiprocessingjson 파일로 여러 개의 문장쌍 데이터를 입력받아 Inference 값을 반환하는 기능
- predict_jsonjson 파일로 여러 개의 문장쌍 데이터를 입력받아 MultiProcessing으로 Inference 값을 반환하는 기능

`content.py`는 메인 코드를 돌리기 위한 모듈입니다. main에서 두 문장을 받아와 predict_model 함수에서 모델 Inference 값을 반환합니다. 모델을 불러와 두 문장이 학습된 모델에 맞추어 벡터로 변환하여 코사인 유사도 계산을 통해 문장 유사도 값을 도출합니다.

- cosine_similarity두 문장의 임베딩 벡터로 코사인 유사도를 구하는 함수
- predict_model모델 Inference 함수


##################


# STS Model Serving
FastAPI 프레임워크를 사용하여 sentence-klue-roberta-base 모델을 서빙했습니다. 본 모델은 두 문장의 유사도를 반환하는 STS(Sentence Textual Similarity) Task 모델입니다. 두 문장이 들어오면 이를 RestAPI로 inference 결과를 반환합니다. 위 코드는 모듈화 되어 있습니다.
Model을 서빙하기위해 Python 기반 백앤드 프레임워크를 고민했습니다. 우수한 공식 문서와 큰 생태계를 갖고 있는 장고 프레임워크와 직관적이고 가벼운 플라스크 프레임워크를 고려했습니다. 고민 끝에 비교적 속도가 빠른 FastAPI 프레임워크를 선택했습니다.
  


## How to Run(Conda)

1. Repository clone
``` 
git clone https://github.com/seawavve/STS_serving
cd STS_serving
unzip training_sts-Huffon-sentence-klue-roberta-base-2022-03-16_16-35-50.zip
```
본 Repository를 clone하여 로컬에 생성합니다. 폴더에 들어가 모델 파일 압축을 해제하여 사용할 모델을 세팅합니다.

2. 환경 생성

```
conda create -n sts-serving python=3.8
conda activate sts-serving
conda install --file requirements.txt
conda install -c powerai sentencepiece
```
conda로 가상환경을 설정합니다. requirements.txt 파일을 읽어 sts-serving conda 환경을 설정합니다.   
위 방식이 실행되지 않는다면 아래 코드를 실행해주세요.

```
pip install -r requirements.text
```
or
```
pip3 install -r requirements.text
```

3. Server Code 

```
uvicorn main:app --reload
```
FastAPI Code를 실행합니다.    

4. URL 접속
`http://127.0.0.1:8000/docs#/` URL 로 Swagger UI에 접속해 세 가지 모듈 중에 원하는 기능을 실행합니다. 기본 기능은 predict_sentences입니다.
<img width="592" alt="image" src="https://user-images.githubusercontent.com/66352658/159536641-63cd6e61-4b0c-4766-a8b3-cfbba6ec654a.png">

5. Usage  
  * predict_sentences (/pred/sentences/)  
  Try it Out -> "sentence_1": "string"의 "string"에 한국어 문장1 삽입 & "sentence_2": "string"의 "string"에 한국어 문장2 삽입 -> Execute  
  결과는 Response Body에서 확인할 수 있습니다.  
  <img width="413" alt="image" src="https://user-images.githubusercontent.com/66352658/159537841-89fbbb9d-be7e-405d-afa6-a80baf649ab7.png">

  * predict_json_multiprocessing (/pred/file/)    
  Try it Out -> sample_data.json 삽입 -> Execute  
  결과는 Response Body에서 확인할 수 있습니다.  
  <img width="409" alt="image" src="https://user-images.githubusercontent.com/66352658/159538459-5116948b-8c2e-4f51-97bf-26c5a39bb193.png">
  
  * predict_json (/pred/multi/)  
  Try it Out -> sample_data.json 삽입 -> Execute  
  결과는 Response Body에서 확인할 수 있습니다.  
  <img width="463" alt="image" src="https://user-images.githubusercontent.com/66352658/159538640-534d0597-f2a3-449b-8c54-63485e2a7bc4.png">


## Execution Result
main.py로 두 문장을 넣어 predict_sentences를 실행한 결과입니다. 변수로 주어진 문장(sentence),두 문장의 코사인 유사도 실수값(score), binary 유사도 값(pred), 코드 런타임(runtime)입니다.
![execution_result](https://github.com/seawavve/STS_serving/blob/master/execution_result.png)



## Code Description
`main.py`는 총 세 가지 비동기 기능을 제공합니다. 가장 기본적인 STS Model Serving 기능은 predict_json입니다. 평귱 1.3초 소요됩니다. 대용량 데이터 처리를 위한 기능은 predict_json_multiprocessing과 predict_sentences입니다. 대용량 데이터를 inference 하는데에 효율적으로 처리하기 위해서 여러 프로세스를 병렬적으로 사용하는 멀티프로세싱 기능을 지원합니다. 일정 데이터 개수 이하의 데이터를 처리한다면 오버헤드 문제로 싱글프로세싱을 사용하는게 더 시간이 적게 드는 Case도 고려하여 predict_json을 개발했습니다. 데이터 양에 따라 나누어서 사용하시면 됩니다. json_data 형식은 sample_data.json 파일을 참고하세요.  
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


