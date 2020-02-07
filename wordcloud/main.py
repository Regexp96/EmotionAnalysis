def morpheme_analysis(input_filename, output_filename):
    import csv
    from konlpy.tag import Okt

    t = Okt()
    # 감정표현가능 형태소 분류한 거 기록할 파일 오픈
    writeFile = open(output_filename, 'w')

    readFile = open(input_filename, 'rt')
    #
    # # 총 단어 개수
    wordCount = 0

    morWordCount = 0
    #
    while True:
        line = readFile.readline()
        # line = unicode(line, 'euc-kr').dencode('utf-8')

        if not line:
            print('파일 다 읽음')
            break
        else:
            # if (len(line) >= 1000): 잠시만 주석
            #     print('너무 많은 데이터의 게시글이라 pass')
            #     continue

            tagKo = t.pos(line)
            # print(line)

            wordCount += len(tagKo)

            for e in tagKo:
                if (e[1] == 'Noun') | (e[1] == 'Verb') | (e[1] == 'Adjective') | (e[1] == 'Exclamation'):
                    print(e[0], file=writeFile)
                    print(e[0])
                    morWordCount += 1

    readFile.close()
    writeFile.close()

    print('단어개수 ', wordCount)
    print('감정표현가능 형태소만 분류한 개수 ', morWordCount)


def create_dictionary():
    import sys
    import csv

    # csv 읽는 부분
    maxInt = sys.maxsize
    decrement = True

    while decrement:
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt / 10)
            decrement = True

    f = open('감정단어사전 647개 스테밍.csv', 'r')
    rdr = csv.reader(f)

    list = []

    for line in rdr:
        list.append(line)

    f.close()
    return list


def dictionary_matching(matching_complete,complete_analyze):
    # 감정단어사전 생성
    dictionaryList = create_dictionary()

    # 감정단어와 매칭된 형태소분석 완료 단어를 기록하기 위한 파일 오픈
    w = open(matching_complete, 'w')

    # 감정단어사전과 매칭시키기 위한 형태소분석 완료 단어 데이터 파일 오픈
    readFile = open(complete_analyze, 'rt')

    # 매칭된 단어 개수
    successCount = 0

    while True:
        # 한 줄을 읽을 때 개행문자도 같이 읽혀서 제거해줌
        line = readFile.readline().rstrip('\n')

        if not line:
            print('감정단어사전 매칭 완료')
            readFile.close()
            break

        for i in dictionaryList:
            # ['1', '2'] 이렇게 2개이상일 때만 즉, 기본형 플러스 변형어도 갖고 있을 때
            if len(i) > 1:
                # 형태소분석한 단어가 감정표현단어의 기본형과 같거나 변형어와 같다면
                if line == i[0] or line in i[1].split('_'):
                    w.write(i[0] + '\n')
            # ['1'] 이런식으로 기본형만 있을 때 같은지 비교
            elif line == i[0]:
                w.write(i[0] + '\n')  # 왜 감격하다면 감,격,하,다 이렇게 저장되지?


def create_wordcloud(matching_complete):
    from os import path
    from wordcloud import WordCloud

    font_path = '../HMKMRHD.ttf'
    d = path.dirname(__file__)

    # 워드클라우드 뿌릴 데이터 파일 오픈
    text = open(path.join(d, matching_complete)).read()

    import matplotlib.pyplot as plt

    # relative_scaling = 0 ~ 1 이고 0일 수록 빽빽히 차게 된다.
    wordcloud = WordCloud(max_font_size=40, font_path=font_path, background_color='white',
                          relative_scaling=0.48).generate(text)
    # plt.figure(figsize=(18, 18))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wordcloud.png', bbox_inches='tight')
    # plt.show()


def run(file_path=''):
    if __name__ == '__main__':
        # 분석할 텍스트파일 경로
        input_filename = 'dataset/everytime.csv'
        output_filename = 'output.txt'
        matching_complete = 'matching_complete.txt'
        complete_analyze = 'complete_analyze.txt'
        # file_name = file_path

        print(input_filename, '분석중....')

        # 형태소분석
        morpheme_analysis(input_filename,output_filename)

        # 감정단어사전 매칭
        dictionary_matching(matching_complete,output_filename)
        #
        # 워드클라우드 생성
        create_wordcloud(matching_complete)
        # 러셀모델에 플로팅

        import russel_floating
        russel_floating.run(matching_complete)

run()