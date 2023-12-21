from konlpy.tag import Twitter
import math
import scipy as sp
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import pandas as pd

# 데이터 원본을 가져와서 필요한 데이터만 사용
"""
origin_data = pd.read_csv(r'C:\\Users\\USER\\Desktop\\project\\test\\data\\final_vod.csv', encoding = 'cp949')
smry_data = origin_data[['subsr', 'SMRY']]
smry_data.to_csv("./data/smry_data.csv")
"""

# 줄거리를 포함한 데이터 가져오기
smry_data = pd.read_csv(r"./smry_recommend/data/smry_data.csv")

'''
# 세부 장르 데이터 가져오기
open_file = open(r'./smry_recommend/data/detail_genre.txt', 'r', encoding = 'utf8')
text = open_file.read()
open_file.close()

# 세부 장르 리스트 생성
data_list = text.split('\n')

# data_list 의 마지막에 공백이 추가되므로 공백 제거
data_list = data_list[:-2]
'''

# data_list 를 컨텐츠가 10개 이상인 장르만으로 수정
data_list = ['TV 시사&교양-기타', 'TV 연예&오락-기타', 'TV드라마-기타', 
             'TV드라마-외화 시리즈', 'TV애니메이션-기타', 'TV애니메이션-명랑&코믹', 
             '영화-SF&환타지', '영화-공포&스릴러', '영화-드라마', '영화-멜로', '영화-무협', 
             '영화-애니메이션', '영화-액션&어드벤쳐', '영화-코미디', '키즈-기타', '키즈-애니메이션', ]

# 장르별 top10
genre_10 = {'TV 시사&교양-기타': ['꼬리에꼬리를무는그날이야기', '그것이알고싶다', '인간극장', '과학수사대스모킹건', '오은영리포트결혼지옥', '실화탐사대', '동물극장단짝', 'NFS국과수', '영상앨범산', '2023역사저널그날'], 'TV 연예&오락-기타': ['런닝맨', '심야괴담회', 'TV동물농장', '불타는장미단', '미운우리새끼', '나혼자산다', '미스터로또', '장미꽃필무렵', '개는훌륭하다', '구해줘!홈즈'], 'TV드라마-기타': ['최강배달꾼', '연인파트1', '소방서옆경찰서그리고국과수', '하늘의인연', '금이야옥이야', '천원짜리변호사', 'TV소설은희', '낭만닥터김사부3', '진짜가나타났다!', '야인시대'], 'TV드라마-외화 시리즈': ['천고결진', '연희공략:건륭황제의여인', '경이로운소문', '구소한야난-너의온도', '유리미인살', '사랑의불시착', '용주전기무간도', '응답하라1988', '경이로운소문2:카운터펀치', '호심'], 'TV애니메이션-기타': ['슈뻘맨TV', '빨간토마토극장시즌1', '흔한남매', '런민기TV시즌4카러플', '백앤아Part2', '로빈TV미니게임PART4', '말량n홍챠TV시즌2', '백앤아남매튜브2', '파뿌리TVPart2', '런민기TV시즌2'], 'TV애니메이션-명랑&코믹': ['짱구는못말려10기', '짱구는못말려22기', '짱구는못말려11기', '짱구는못말려15기', '원픽은,흔한남매', '신도라에몽21기', '짱구는못말려23기', '신도라에몽스페셜2기', '로빈TV변신몬스터', '신도라에몽14기'], '영화-SF&환타지': ['아바타:물의길', '더문', '애쉬래드2:황금성을찾아서', '2067', '인어공주', '신과함께-인과연', '가디언즈오브갤럭시VOL3', '루퍼', '신천녀유혼2:원령대전', '신천녀유혼:인과연'], '영화-공포&스릴러': ['백설공주살인사건', '비닐하우스', '사일런싱', '퇴마-무녀굴', '공작조:현애지상', '더웹툰-예고살인', '뒤틀린집', '베니싱트윈', '블랙워터:어비스', '써스피션'], '영화-드라마': ['러브포세일', '멍뭉이', '리볼버', '극장판시그널', '상류사회', '창', '보안관', '임파서블러브', '장군의아들', '터널'], '영화-멜로': ['해피엔드', '후궁-제왕의첩', '초대:스와핑데이', '은교', '러브이세벨', '웨이트:감각에눈뜰때', '무뢰한', '세기말', '극적인하룻밤', '10일간의애인'], '영화-무협': ['어요지:물속의괴물', '야연2', '첩혈강호', '황실수사대', '검신의제국2', '산해거수', '영웅연대', '왕자후예', '적인걸:백호의저주', '천기검'], '영화-애니메이션': ['슈퍼마리오브라더스', '엘리멘탈', '라이온킹', '이웃집토토로', '스파이더맨:어크로스더유니버스', '짱구는 못말려: 수수께끼! 꽃피는 천하떡잎학교', '짱구는못말려:동물소환닌자', '극장판명탐정코난:할로윈의신부', '도라에몽-진구의비밀도구박물관', '모모와다락방의수상한요괴들'], '영화-액션&어드벤쳐': ['범죄도시3', '존윅4', '밀수', '존윅3:파라벨룸', '표적', '마크맨', '탈명검:풍운재기', '절색특공:데드스콜피온', '보이스', '해운대'], '영화-코미디': ['육사오', '이장과군수', '오늘부터우리는!!', '귀신이산다', '롤러코스터', '미스터주:사라진VIP', '인턴', '지옥의화원', '강룡신장소걸아', '동갑내기과외하기2'], '키즈-기타': ['뽀로로인기동요', '타요의씽씽극장동요2', '엘리가간다시즌4', '잠자는숲속의공주', '우당탕탕에디의실험실', '기운센말', '엘리가간다시즌7', '우리집에는사자가있어', '지니강이플러스시즌2', '캐리와친구들의장난감놀이시즌4'], '키즈-애니메이션': ['뽀로로와노래해요NEW1', '마카앤로니2', '엉뚱발랄콩순이와친구들5기', '마법버스타요', '크니쁘니히어로즈', '타요의씽씽극장시즌2', '뽀롱뽀롱뽀로로NEW1', '프렌즈2022', '감자아저씨의크리스마스공연외', '강건너기외'], }

# 불용어 처리
with open(r'./smry_recommend/data/stopword.txt', 'r', encoding = 'utf-8') as f:
    stopwords = f.read()
stopwords_list = stopwords.split('\n')

word_dict_data = {}

# 각 세부 장르 별로 단어 리스트 생성하고 저장
for detail_genre in data_list:
    # 각 세부 장르에 대해 단어 데이터 가져오기
    open_file = open(r'./smry_recommend/data/' + detail_genre + '_words.txt', 'r', encoding = 'utf8')
    text = open_file.read()
    
    # 파일 닫기
    open_file.close()
    
    # 각 단어 분리하기
    text_list = text.split('\n')
    text_list = text_list[:-2] # 마지막의 공백 제외
    
    # 각 장르별 주요 단어 찾기
    spliter = Twitter()
    nouns_for_dictionary = spliter.nouns(text)
    ko = nltk.Text(nouns_for_dictionary, name = detail_genre)
       
    # 불용어 제거
    ko1 = [each_word for each_word in ko if each_word not in stopwords_list]
    ko = nltk.Text(ko1, name = detail_genre)
    word_dict = dict(ko.vocab())
    
    # 단어 리스트를 dict 형태로 저장
    word_dict_data[detail_genre] = word_dict


# 장르별 벡터 저장
word_vector_dict = {}
vectorizer = CountVectorizer(min_df = 0.05)
    
# dict 형태로 저장되어 있는 단어 데이터를 읽고
# 각 단어들을 모아서 하나의 문장으로 만든 다음 저장
for detail_genre in data_list:
    contents_tokens = word_dict_data[detail_genre]

    # 벡터화를 위해 단어들을 가지고 문장 생성
    contents_for_vect = []
    sentence = ''
    # 토큰 단위로 구분된 문장을 생성
    for content in contents_tokens:
        sentence += ' ' + content

    # 생성한 문장을 리스트에 추가
    contents_for_vect.append(sentence)
    
    word_vector_dict[detail_genre] = contents_for_vect


#거리 구해주는 함수 생성
def dist_raw(v1, v2):
    # 차이를 계산
    delta = v1 - v2
    
    return sp.linalg.norm(delta.toarray())

# 사용자 번호를 입력으로 사용
def smry_recommend(subsr_num):
    # 사용자 번호가 일치하는 데이터 중 줄거리만 가져오기
    user_data = smry_data[smry_data['subsr'] == subsr_num]['SMRY']
    
    smry_list = []
    # 데이터를 순회하면서 줄거리 저장
    for item in user_data:
        if item not in smry_list:
            smry_list.append(item)
        
    smry_sentence = ''
    for smry in smry_list:
        smry_sentence += (smry + ' ')
        
    # 샘플 문장 토큰화
    spliter = Twitter()
    sample_words = spliter.nouns(smry_sentence)

    # 가장 거리가 짧은 세부 장르 계산용
    min_distance = 65536
    min_detail_genre = 'None'

    
    # 각 세부 장르별 거리 계산을 수행
    for detail_genre in data_list:
        vectorizer = CountVectorizer(min_df = 1) # 1번만 등장해도 단어 사전에 포함시키도록

        # 장르 별로 줄거리 불러오기 - dict 의 value
        contents_tokens = word_vector_dict[detail_genre]

        sentence = contents_tokens[0]

        # 생성한 문장을 리스트에 추가
        contents_for_vect = []
        contents_for_vect.append(sentence)

        # 피처 벡터화 - 띄어쓰기를 기준으로 벡터화
        X = vectorizer.fit_transform(contents_for_vect)

        # 샘플 줄거리 문장을 피처 벡터화
        new_content_vect = vectorizer.transform([smry_sentence])

        # 거리 계산
        post_vec = X.getrow(0) # 단어 문장이 1개이므로 첫번째인 0번 인덱스
        distance = dist_raw(new_content_vect, post_vec)

        # 세부 장르별 단어의 갯수를 세고 일정 갯수 이하이면 제외
        length = post_vec.shape[1]
        limit_length = 100
        limit_cor = 0.3
        if length < limit_length:
            pass

        else:
            # 일치율 계산하기
            count = 0
            for item in sample_words:
                if item in contents_tokens[0]:
                    count += 1

            cor = count / len(sample_words)

            # 일치율이 기준을 넘는 경우에만 거리를 계산
            if cor < limit_cor:
                pass

            else:
                # 결과 확인 - 장르와의 거리는 줄거리 단어의 길이를 가중치로 반영하여 계산
                weighted_distance = distance / (math.log10(length)) / cor
                '''
                print(detail_genre, ' 장르와의 거리는 : \t', weighted_distance, sep='') 
                # 1000을 곱한 이유는 쉽게 보기 위함
                print(detail_genre, ' 장르와의 거리(원본)는 : \t', distance, sep='')
                print(detail_genre, ' 장르와의 일치율은 : \t', cor * 100 , '%', sep='')
                print(detail_genre, ' 장르의 단어 길이는 : \t', length, '\n',sep='')
                '''

                if weighted_distance < min_distance:
                    min_distance = weighted_distance
                    min_detail_genre = detail_genre

    # 최종 결과         
    #print('가장 유사한 장르는 ', min_detail_genre, sep = '')
    #print(genre_10[min_detail_genre])
    return(genre_10[min_detail_genre])