from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import russel_floating
from konlpy.tag import Hannanum
import csv
from pykospacing import spacing
import sys
import word_count


def morpheme_analysis(input_filename, output_filename):
    t = Hannanum()
    # 감정표현가능 형태소 분류한 거 기록할 파일 오픈
    write_file = open(output_filename, 'w')
    read_file = open(input_filename, 'rt')

    file = open(input_filename, 'rt')
    row_count = len(file.readlines())
    file.close()
    # 총 단어 개수
    word_counts = 0
    mor_word_count = 0
    #
    if input_filename.endswith('.csv'):
        read_csv = csv.reader(read_file)
        rows = 0
        print(row_count)
        for lines in read_csv:
            un_spaced_line = lines[1]
            rows += 1
            # 띄어쓰기 검사
            # 198자가 넘어가면 에러가 뜨는데 설마 198자나 띄어쓰기 안하고 쓰는사람이 있을리가...?
            if len(un_spaced_line) >= 198:
                line = un_spaced_line
            else:
                line = spacing(un_spaced_line)
            tagKo = t.pos(line, ntags=22)
            # print(line)
            word_counts += len(tagKo)
            for e in tagKo:
                if (e[1] == 'NC') or (e[1] == 'NQ') or (e[1] == 'NB') or (e[1] == 'NN') or (e[1] == 'NP') or (
                        e[1] == 'PV') or (e[1] == 'PA') or (e[1] == 'II'):
                    # print(e[0], file=write_file)
                    word_count.word_check(e[0], write_file)
                    # print(e[0])
                    mor_word_count += 1
            print(str(int((rows/row_count)*100))+"%")
    else:
        row_count = read_file.read().count("\n")+1
        rows = 0
        print(row_count)
        while True:
            # 띄어쓰기 검사
            un_spaced_line = read_file.readline()
            rows += 1
            if len(un_spaced_line) >= 198:
                line = un_spaced_line
            else:
                line = spacing(un_spaced_line)

            if not line:
                print('파일 다 읽음')
                break
            else:
                tagKo = t.pos(line,ntags=22)
                # print(line)
                word_counts += len(tagKo)
                for e in tagKo:
                    if (e[1] == 'NC') or (e[1] == 'NQ') or (e[1] == 'NB') or (e[1] == 'NN') or (e[1] == 'NP') \
                            or (e[1] == 'PV') or (e[1] == 'PA') or (e[1] == 'II'):
                        # print(e[0], file=write_file)
                        # 여기서 바로 단어 매칭으로 넘기기
                        import word_counts
                        word_counts.word_check(e[0], output_filename)
                        # print(e[0])
                        mor_word_count += 1
                print(str(int((rows / row_count) * 100)) + "%")

    read_file.close()
    write_file.close()

    print('단어개수 ', word_counts)
    print('감정표현가능 형태소만 분류한 개수 ', mor_word_count)


def create_wordcloud(matching_complete):
    font_path = '../Font/HMKMRHD.ttf'
    d = path.dirname(__file__)

    # 워드클라우드 뿌릴 데이터 파일 오픈
    text = open(path.join(d, matching_complete)).read()
    if len(text) < 1:
        return

    # relative_scaling = 0 ~ 1 이고 0일 수록 빽빽히 차게 된다.
    wordcloud = WordCloud(max_font_size=80, font_path=font_path, background_color='white',
                          relative_scaling=0.48, collocations=False).generate(text)
    # plt.figure(figsize=(18, 18))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('output/wordcloud.png', bbox_inches='tight')
    # plt.show()


def run():
    if __name__ == '__main__':
        # 분석할 텍스트파일 경로
        # input_file = file_path
        input_file = 'dataset/twitter1.csv'
        output_file = 'output/output.txt'
        matching_complete = 'output/matching_complete.txt'

        print(input_file, '분석중....')
        # 형태소분석
        print('형태소 분석/매칭 시작')
        morpheme_analysis(input_file, output_file)

        # 감정단어사전 매칭
        print('감성사전 매칭')
        word_count.word_check(output_file, matching_complete)

        # 워드클라우드 생성
        print('워드클라우드 생성')
        create_wordcloud(matching_complete)

        # 러셀모델에 플로팅
        print('모델에 플로팅')
        russel_floating.run(matching_complete)

run()

# print(sys.argv)
