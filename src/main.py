from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import russel_floating
from konlpy.tag import Hannanum
import csv
from pykospacing import spacing

def morpheme_analysis(input_filename, output_filename):
    t = Hannanum()
    # 감정표현가능 형태소 분류한 거 기록할 파일 오픈
    write_file = open(output_filename, 'w')
    read_file = open(input_filename, 'rt')

    # 총 단어 개수
    word_count = 0
    mor_word_count = 0
    #
    if input_filename.endswith('.csv'):
        read_csv = csv.reader(read_file)
        for lines in read_csv:
            un_spaced_line = lines[1]
            # 띄어쓰기 검사
            # 198자가 넘어가면 에러가 뜨는데 설마 198자나 띄어쓰기 안하고 쓰는사람이 있을리가...?
            if len(un_spaced_line) >= 198:
                line = un_spaced_line
            else:
                line = spacing(un_spaced_line)
            tagKo = t.pos(line, ntags=22)
            # print(line)
            word_count += len(tagKo)
            for e in tagKo:
                if (e[1] == 'NC') or (e[1] == 'NQ') or (e[1] == 'NB') or (e[1] == 'NN') or (e[1] == 'NP') or (
                        e[1] == 'PV') or (e[1] == 'PA') or (e[1] == 'II'):
                    print(e[0], file=write_file)
                    print(e[0])
                    mor_word_count += 1
    else:
        while True:
            # 띄어쓰기 검사
            un_spaced_line = read_file.readline()
            if len(un_spaced_line) >= 198:
                line = un_spaced_line
            else:
                line = spacing(un_spaced_line)

            if not line:
                print('파일 다 읽음')
                break
            else:
                # if (len(line) >= 1000): 잠시만 주석
                #     print('너무 많은 데이터의 게시글이라 pass')
                #     continue
                tagKo = t.pos(line,ntags=22)
                # print(line)
                word_count += len(tagKo)
                for e in tagKo:
                    if (e[1] == 'NC') or (e[1] == 'NQ') or (e[1] == 'NB') or (e[1] == 'NN') or (e[1] == 'NP') or (e[1] == 'PV') or (e[1] == 'PA') or (e[1] == 'II'):
                        print(e[0], file=write_file)
                        print(e[0])
                        mor_word_count += 1

    read_file.close()
    write_file.close()

    print('단어개수 ', word_count)
    print('감정표현가능 형태소만 분류한 개수 ', mor_word_count)


def create_dictionary():
    import sys
    import csv

    # csv 읽는 부분
    max_int = sys.maxsize
    decrement = True

    while decrement:
        decrement = False
        try:
            csv.field_size_limit(max_int)
        except OverflowError:
            max_int = int(max_int / 10)
            decrement = True

    f = open('감정단어사전 647개 스테밍.csv', 'r')
    rdr = csv.reader(f)

    steamed_file_list = []

    for line in rdr:
        steamed_file_list.append(line)
        print(line)

    f.close()
    return steamed_file_list


# 폐기예정
def dictionary_matching(matching_complete,complete_analyze):
    # 감정단어사전 생성
    dictionaryList = create_dictionary()

    # 감정단어와 매칭된 형태소분석 완료 단어를 기록하기 위한 파일 오픈
    w = open(matching_complete, 'w')

    # 감정단어사전과 매칭시키기 위한 형태소분석 완료 단어 데이터 파일 오픈
    readFile = open(complete_analyze, 'rt')

    while True:
        # 한 줄을 읽을 때 개행문자도 같이 읽혀서 제거해줌
        line = readFile.readline().rstrip('\n')
        n = 0

        if not line:
            print('감정단어사전 매칭 완료')
            print('감성단어는 총 '+str(n)+'개입니다.')
            readFile.close()
            break

        for i in dictionaryList:
            # ['1', '2'] 이렇게 2개이상일 때만 즉, 기본형 플러스 변형어도 갖고 있을 때
            if len(i) > 1:
                # 형태소분석한 단어가 감정표현단어의 기본형과 같거나 변형어와 같다면
                if line == i[0] or line in i[1].split('_'):
                    w.write(i[0] + '\n')
                    n = n+1
                    print(i[0])
            # ['1'] 이런식으로 기본형만 있을 때 같은지 비교
            elif line == i[0]:
                w.write(i[0] + '\n')  # 왜 감격하다면 감,격,하,다 이렇게 저장되지?
                n = n + 1
                print(i[0])


def create_wordcloud(matching_complete):
    font_path = '../Font/HMKMRHD.ttf'
    d = path.dirname(__file__)

    # 워드클라우드 뿌릴 데이터 파일 오픈
    text = open(path.join(d, matching_complete)).read()
    if len(text) < 1:
        return

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
        input_file = 'dataset/everytime.csv'
        output_file = 'output.txt'
        matching_complete = 'matching_complete.txt'
        complete_analyze = 'complete_analyze.txt'
        # file_name = file_path
        #

        # 새로운 단어 체크 알고리즘
        # 그래프 플로팅용 다시 만들어야함
        # import word_count
        # word_count.word_check(output_file, matching_complete)

        print(input_file, '분석중....')

        # 형태소분석
        print('형태소 분석 시작.')
        # morpheme_analysis(input_file,output_file)

        # 감정단어사전 매칭
        print('감성사전 매칭')
        dictionary_matching(matching_complete,output_file)

        # 워드클라우드 생성
        print('워드클라우드 생성')
        create_wordcloud(matching_complete)
        # 러셀모델에 플로팅
        print('모델에 플로팅')
        russel_floating.run(matching_complete)

run()