import pandas as pd

# 분석을 통해 파악할 날씨별 연관성이 높은 세부 장르
weather_data_format = {'비' : ['TV 연예/오락&기타', 'TV드라마&기타', '영화&액션/어드벤쳐'],
                '맑음' : ['키즈&기타', '영화&액션/어드벤쳐', 'TV 시사/교양&기타'],
                '구름' : ['TV드라마&기타', '키즈&기타', '키즈&애니메이션']}

origin_data = pd.read_csv(r'./weather_recommend/data/weatherTop10.csv', encoding='cp949')
#print(origin_data)

#weather = '맑음'

# 날씨를 입력 받아서 그에 대한 추천을 진행
def weather_recommend(weather):
    # 입력받은 날씨에 해당하는 데이터만 추출하고 정렬
    weather_data = origin_data[origin_data['weather'] == weather][['asset_nm_new', 'rank']]
    weather_data = weather_data.sort_values('rank', ascending=True)

    # 정렬을 기준으로 1위부터 추천
    weather_recommend_list = []
    for _, item in weather_data.iterrows():
        asset = item['asset_nm_new']
        weather_recommend_list.append(asset)

    # 추천 결과를 리턴
    return weather_recommend_list
