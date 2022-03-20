# STS Model Serving
-----
FastAPI 프레임워크를 사용하여 sentence-klue-roberta-base 모델을 서빙했습니다. 본 모델은 두 문장의 유사도를 반환하는 STS(Sentence Textual Similarity) Task 모델입니다. 두 문장이 들어오면 이를 RestAPI POST로 받아와 inference 결과를 반환합니다. 위 코드는 모듈화 되어 있습니다.

## Code Description
`main.py`는 총 세 가지 기능을 제공합니다.
- predict_sentences
  하나의 문장쌍을 입력받아 Inference 값을 반환하는 기능
- predict_json_multiprocessing
  json 파일로 여러 개의 문장쌍 데이터를 입력받아 Inference 값을 반환하는 기능
- predict_json
  json 파일로 여러 개의 문장쌍 데이터를 입력받아 MultiProcessing으로 Inference 값을 반환하는 기능

가장 기본적인 STS Model Serving 기능은 predict_json입니다. 
대용량 데이터 처리를 위한 기능은 predict_json_multiprocessing과 predict_sentences입니다. 대용량 데이터를 inference 하는데에 효율적으로 처리하기 위해서 여러 프로세스를 병렬적으로 사용하는 멀티프로세싱 기능을 지원합니다. 일정 데이터 개수 이하의 데이터를 처리한다면 오버헤드 문제로 싱글프로세싱을 사용하는게 더 시간이 적게 드는 Case도 고려하여 predict_json을 개발했습니다. 데이터 양에 따라 나누어서 사용하시면 됩니다.  

`content.py`는 메인 코드를 돌리기 위한 모듈입니다.
- 


## How to Run
