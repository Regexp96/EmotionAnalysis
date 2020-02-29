import lemmatizer
import csv
from soynlp.hangle import compose, decompose


# todo 사전 csv파일 읽어서 원형 복원기 사전으로 넣기
# todo test셋도 csv파일 기반으로 만들고 테스트 돌려보기


def word_check(word, output):
    import timeit
    start = timeit.default_timer()
    # stems == 용언의 원형 사전
    stems = []
    word_dic = open('graphData/emotionword_dic.csv', 'r')
    for i in word_dic.readlines():
        stems.append(i.rstrip("\n"))
    # testset == 원형을 찾고싶은 단어들을 모아놓은 배열
    testset = ''

    import re
    hangul = re.compile('[^ 가-힣]+')
    a = hangul.sub("", word)
    if len(a) == 0:
        pass
    else:
        testset = a

    lemmatiz = lemmatizer.Lemmatizer(stems=stems)

    candidates = lemmatiz.candidates(testset)
    if len(candidates) == 0:
        # print(word)
        if non_predicate(testset, stems):
            # print(word[0])
            output.write(testset[0] + '\n')
            print('후보가 없음')
    else:
        # print('{} : {}'.format(word, candidates))
        cand_list = list(candidates)
        output.write(list(cand_list[0])[0] + '\n')


def non_predicate(target_word, dic_word):
    # 자소 분리해서 비교하는 알고리즘
    i = 0
    flag = False
    try:
        target_list = make_decomposed_list(target_word)
        dic_list = make_decomposed_list(dic_word[0])
    except TypeError:
        return flag

    # 사전에 있는 단어 길이 기준으로 나눔
    # 비교하다가 다른 단어 있으면 false 플래그 세움
    for length in dic_word:
        while i < len(dic_list):
            # todo 종성이 없는 단어를 decompose하면 종성자리를 남김 ex) 가소ㄹ -> ['ㄱ', 'ㅏ', ' ', 'ㅅ', 'ㅗ', ' ', 'ㄹ', ' ', ' ']
            # todo 타겟이랑 사전이랑 배열 길이 다른거 해결해야함
            # todo 숫자로 시작하는건 아에 decompose되지않음 (아마 초성체도 그대로일듯)
            dic_idx, target_idx = i, i
            if target_idx != len(target_list) or dic_idx != len(dic_list):
                return False
            if target_list[i] == dic_list[i]:
                # print('target: ' + target_list[i] + " dic: " + dic_list[i])
                flag = True
            elif target_list[i] != dic_list[i]:
                flag = False
            print(flag)
            i = i + 1
            dic_list = make_decomposed_list(dic_word[i])
        a = 0
    print(flag)
    return flag


def make_decomposed_list(target):
    i = 0
    target_list = list()
    while len(target) > i:
        decomposed_target = decompose(target[i])
        i = i + 1
        for a in decomposed_target:
            target_list.append(a)
    a = 0
    # print('make_decomposed_list: '+target)
    return target_list

# import csv
# file = open('../coinedWordData.csv')
# write = open('../test.txt','w')
# read_csv = csv.reader(file)
# for lines in read_csv:
#     print(lines[0], file=write)
#
# write.close()


# word_check('../test.txt','1.txt')