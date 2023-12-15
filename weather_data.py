# 날씨 데이터용 Python3 코드

import requests
import json

# 초단기 예보 조회(3일까지 조회 가능) - getUltraSrtFcst
service_key = 'WR5g74pN0Qlika3v5ycMeyP3aQyqLtsFGPbt3nU4zT4a2sJMxZ1i8Z2e1NpZ%2BZWxZ4B6VCR8u2WR0ky52jg%2Bhw%3D%3D'
base_date = '20231214'
# base_time은 3시간 단위로 사용해야 함 - 0200, 0500, 0800 ...
base_time = '0500'
nx = '60'
ny = '127'
data_format = 'JSON'
# base_date, base_time을 기준으로 1개의 데이터만 가져오도록 설정
url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={service_key}&numOfRows=12&pageNo=1&dataType={data_format}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}'

# 데이터 조회
response = requests.get(url, verify = False)

# 데이터 확인
result = json.loads(response.text)
#print(response.content)
print(response)
#print(result)
#print(type(result))

# 필요한 날씨 데이터가 위치하는 카테고리 확인
informations = dict()
for items in result['response']['body']['items']['item'] :
    cate = items['category']
    fcstTime = items['fcstTime']
    fcstValue = items['fcstValue']
    temp = dict()
    temp[cate] = fcstValue
    
    if fcstTime not in informations.keys() :
        informations[fcstTime] = dict()
#     print(items['category'], items['fcstTime'], items['fcstValue'])
#     print(informations[fcstTime])
    informations[fcstTime][cate] = fcstValue

print(informations)