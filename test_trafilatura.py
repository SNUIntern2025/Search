import trafilatura as test_trafilatura

# 크롤링할 URL 설정
response = [{'url': 'https://plankim.com/아이폰14-15-16-비교-분석/',
    'content': '3 모델 중 아이폰15를 선택하는 기준은 크게 3가지입니다. 애플 인텔리전스 기능은 아직 한국 지원도 안 하지만 그렇게 큰 쓸모가 없다고 생각하시는 분! 아이폰16 후면 카메라 디자인이 맘에 안 드는 경우, 그리고 마지막으로 접사 사진 기능이 필요 없는 분입니다.'},
  {'url': 'https://support.apple.com/ko-kr/108044',
    'content': '세부 사항: iPhone 15 Pro Max에는 Dynamic Island 기술이 적용된 17.01cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 14 Pro Max에는 Dynamic Island 기술이 적용된 17.01cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 14에는 15.49cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 13 Pro Max에는 ProMotion 기술이 적용된 17.01cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 13에는 15.49cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 12 Pro Max에는 17.01cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 12에는 15.49cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다. 세부 사항: iPhone 11 Pro Max에는 16.51cm1 전체 화면 Super Retina XDR 디스플레이가 장착되어 있습니다.'},
  {'url': 'https://m.blog.naver.com/onyu_family/223337783277',
    'content': '애플 아이폰 6s ... 아이폰16 라인 은 기본모델, 플러스, 프로, 프로 맥스 총 4개의 종류로 출시하였습니다. 이전 아이폰 X 시리즈 디자인과 흡사한 세로 카메라를 다시 적용하며, 아이폰 16 및 16 플러스 모델은 이전 세대와 동일한 6.1인치 및 6.7인치 Super Retina XDR OLED'},
  {'url': 'https://www.tech42.co.kr/애플-오늘-공개한-아이폰-16-pro-및-아이폰-16-pro-max-특징-그리고/',
    'content': "애플(Apple)이 9일(현지시간) 아이폰(iPhone) 16 Pro와 아이폰 16 Pro Max를 공개했다. 두 모델 모두 더 커진 디스플레이, 첨단 카메라 시스템에 빠르게 접근할 수 있는 새로운 '카메라 컨트롤,' 새로운 창의성의 장을 열어주는 혁신적인 프로 카메라 기능, 게임에 몰입감을 더해주는 그래픽 성능 등 다양한"},
  {'url': 'https://ko.wikipedia.org/wiki/아이폰',
    'content': '(최신, 독점 업데이트 ... us$499의 4 gb 모델과 us$599의 8 gb 모델, 이렇게 2개의 초기 모델(모두 2년 계약 필수)이 2007년 6월 29일 미국에서 현지 시각 오후 6:00에 판매에 들어갔고 수백 명의 고객들이 국내 스토어 밖에서 줄을 섰다. ... (한국어) 애플 코리아 아이폰 공식'}]
  
for item in response:
    url = item['url']

    # 웹 페이지 다운로드
    downloaded = test_trafilatura.fetch_url(url)

    # 본문 및 메타데이터 추출
    result = test_trafilatura.extract(downloaded, output_format="json", include_comments=False, include_links=False, with_metadata=True)

    # JSON 문자열을 파이썬 딕셔너리로 변환
    import json
    parsed_result = json.loads(result)

    # 제목 출력
    print("제목:", parsed_result['title'])

    # 본문 출력
    print("\n본문:")
    print(parsed_result['text'])
    print("\n\n\n")
    break