from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import Document
import asyncio

# api key
from config import OPENAI_API_KEY
# 시간 측정을 위한 time 모듈
import time


# 야라 문서를 병렬적으로 요약하는 비동기 작업을 처리하는 함수입니다.
async def summarize_documents(docs, llm, prompt_template, max_concurrent_tasks=5):
    # gpt4o-mini 모델을 사용하여 문서를 요약하는 체인을 로드합니다.
    chain = load_summarize_chain(llm, chain_type="map_reduce", return_intermediate_steps=False)

    #비동기 작업의 수를 제한하는 세파모어를 설정하여 동시에 실행되는 작업의 수를 max_concurrent_tasks로 제한합니다.
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    #각 문서를 받아온 후 요약 작업을 수행하는 비동기 함수입니다
    async def summarize_task(doc):
        async with semaphore:
            # 각 문서를 langchain 내장 클래스인 Document 객체로 변환합니다. page_content parameter에 string으로 된 text를 저장합니다.
            document = Document(page_content=doc)
            # chain.ainvoke() 메서드를 사용하여 문서를 요약합니다
            return await chain.ainvoke({"input_documents": [document]})

    # 비동기적으로 수행할 작업들을 리스트로 만듭니다. 아래 return await asyncio.gather(*tasks)에서 *tasks 내의 작업들을 unpackiing하여 작업을 수행하게 됩니다.
    tasks = [summarize_task(doc) for doc in docs]

    # asyncio.gather: 여러 비동기 작업을 병렬로 실행하여 모든 문서의 요약 결과를 반환합니다.
    return await asyncio.gather(*tasks)

# Example Usage
async def main():

    # 요약할 문서 목록. 여기에 crawling함수의 output 결과를 불러오면 될 것 같습니다.
    docs = [
        "아이폰(영어: iPhone)은 미국의 기업 애플이 디자인하고 마케팅한 터치스크린 기반 휴대 전화 계열이다. 애플의 iOS 모바일 운영 체제를 사용한다. 1세대 아이폰은 애플의 공동 창립자 스티브 잡스가 2007년 1월 9일 발표하였고 2007년 6월 29일 처음으로 출시되었다. 그 뒤로 애플은 해마다 새로운 아이폰 모델과 iOS 업데이트를 출시해왔다. 2018년 11월 1일 기준으로 22억대 이상의 아이폰이 판매되었다. 아이폰의 사용자 인터페이스는 가상 키보드를 갖춘 멀티 터치 화면으로 구성된다. 아이폰은 셀룰러 망이나 와이파이에 연결되며, 통화, 웹 브라우징, 사진 촬영, 음악 재생, 이메일과 문자 메시지 송수신을 할 수 있다. 아이폰 런칭 이후 더 많은 기능들이 추가되었는데, 여기에는 더 큰 화면 크기, 동영상 촬영, 방수 기능, 앱 스토어를 경유한 서드파티 모바일 앱의 설치 기능, 접근성 지원이 포함된다. 2017년까지 아이폰은 전면 패널에 사용자를 홈 스크린으로 복귀시키는 하나의 버튼을 갖춘 레이아웃을 사용하였다. 2017년 이후 출시된 아이폰 X 이상 모델들은 제스처 인식에 의해 앱 전환 활성화가 가능한, 베젤리스에 가까운 전면 화면 디자인으로 전환하였다. 1세대 아이폰은 모바일 전화 산업 면에서 '혁명적인', '게임 체인저'라는 용어로 기술되었으며 차기 모델들 또한 찬사를 받았다. 아이폰은 휴대전화와 슬레이트 폼 팩터를 보급하는데 주된 기여를 하였으며 모바일 앱과 앱 경제를 위한 커다란 시장을 창출하였다. 2017년 1월 기준으로, 애플의 앱 스토어에는 아이폰을 대상으로 220만개 이상의 애플리케이션이 포함되었다.",
        "애플(Apple)이 9일(현지시간) 아이폰(iPhone) 16 Pro와 아이폰 16 Pro Max를 공개했다. 두 모델 모두 더 커진 디스플레이, 첨단 카메라 시스템에 빠르게 접근할 수 있는 새로운 '카메라 컨트롤, 새로운 창의성의 장을 열어주는 혁신적인 프로 카메라 기능, 게임에 몰입감을 더해주는 그래픽 성능 등 다양한 최신 기능을 갖추고 있고, 이 모든 기능을 구현해 주는 A18 Pro 칩을 탑재한다.",
        "더 빠른 쿼드 픽셀 센서를 탑재하고 초당 120 프레임의 4K Dolby Vision 동영상 촬영을 지원하는 새로운 48MP Fusion 카메라를 갖춘 새 Pro 모델들은 아이폰 사상 가장 높은 해상도와 프레임률의 조합을 자랑한다.",
        "더 나아가 두 Pro 모델 모두 접사 사진을 포함해 더 높은 해상도의 사진을 찍을 수 있는 새로운 48MP 울트라 와이드 카메라와 5배 망원 카메라, 여기에 한층 생생한 오디오 레코딩을 지원하는 스튜디오급 마이크까지 갖추었다.",
        "견고한 티타늄 디자인은 더 커진 디스플레이 사이즈에서도 가벼우면서도 강한 내구도를 가지고 있을 뿐 아니라, 애플 제품 중 가장 얇은 베젤 역시 눈에 띈다. 또한, 배터리 수명이 대폭 증가한 덕분에 아이폰 16 Pro Max의 경우 아이폰 사상 최고의 배터리 사용 시간을 제공한다.",
    ]

    # llm 로딩. max_tokens는 1000으로 설정했습니다.
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini-2024-07-18", max_tokens=1000)

    # 시간 측정 시작
    start_time = time.time()

    # 요약하는 prompt
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="다음 텍스트를 요약해줘:\n{text}\n"
    )

    # 문서들을 병렬적으로 요약하고 결과를 출력합니다
    summaries = await summarize_documents(docs, llm, prompt_template, max_concurrent_tasks=3)

    # 시간 측정 종료
    end_time = time.time()

    print(summaries)

    # 실행 시간
    elapsed_time = end_time - start_time

    print(f"Execution Time: {elapsed_time:.2f} seconds")


# maing 함수 비동기적으로 실행
asyncio.run(main())

