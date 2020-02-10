import soynlp
from soynlp.hangle import compose, decompose


class Lemmatizer:
    def __init__(self, stems, predefined=None):
        self._stems = stems
        self._predefined = {}
        if predefined:
            self._predefined.update(predefined)

    def is_stem(self, w):
        return w in self._stems

    def lemmatize(self, word):
        raise NotImplemented

    def candidates(self, word):
        candidates = set()
        for i in range(1, len(word) + 1):
            l = word[:i]
            r = word[i:]
            candidates.update(self._candidates(l, r))
        return candidates

    def _candidates(self, l, r):
        candidates = set()
        if self.is_stem(l):
            candidates.add((l, r))

        l_last = decompose(l[-1])
        l_last_ = compose(l_last[0], l_last[1], ' ')
        r_first = decompose(r[0]) if r else ('', '', '')
        r_first_ = compose(r_first[0], r_first[1], ' ') if r else ' '

        # ㄷ 불규칙 활용: 깨닫 + 아 -> 깨달아
        if l_last[2] == 'ㄹ' and r_first[0] == 'ㅇ':
            l_stem = l[:-1] + compose(l_last[0], l_last[1], 'ㄷ')
            if self.is_stem(l_stem):
                candidates.add((l_stem, r))

        # 르 불규칙 활용: 굴 + 러 -> 구르다
        if (l_last[2] == 'ㄹ') and (r_first_ == '러' or (r_first_ == '라')):
            l_stem = l[:-1] + compose(l_last[0], l_last[1], ' ') + '르'
            r_canon = compose('ㅇ', r_first[1], r_first[2]) + r[1:]
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # ㅂ 불규칙 활용: 더러 + 워서 -> 더럽다
        if (l_last[2] == ' ') and (r_first_ == '워' or r_first_ == '와'):
            l_stem = l[:-1] + compose(l_last[0], l_last[1], 'ㅂ')
            r_canon = compose('ㅇ', 'ㅏ' if r_first_ == '와' else 'ㅓ', r_first[2]) + r[1:]
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        #         # 어미의 첫글자가 종성일 경우 (-ㄴ, -ㄹ, -ㅂ, -ㅅ)
        #         # 입 + 니다 -> 입니다
        if l_last[2] == 'ㄴ' or l_last[2] == 'ㄹ' or l_last[2] == 'ㅂ' or l_last[2] == 'ㅆ':
            l_stem = l[:-1] + compose(l_last[0], l_last[1], ' ')
            r_canon = l_last[2] + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        #         # ㅅ 불규칙 활용: 부 + 었다 -> 붓다
        #         # exception : 벗 + 어 -> 벗어
        if (l_last[2] == ' ' and l[-1] != '벗') and (r_first[0] == 'ㅇ'):
            l_stem = l[:-1] + compose(l_last[0], l_last[1], 'ㅅ')
            if self.is_stem(l_stem):
                candidates.add((l_stem, r))

        # 우 불규칙 활용: 똥퍼 + '' -> 똥푸다
        if l_last_ == '퍼':
            l_stem = l[:-1] + '푸'
            r_canon = compose('ㅇ', l_last[1], l_last[2]) + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # 우 불규칙 활용: 줬 + 어 -> 주다
        if l_last[1] == 'ㅝ':
            l_stem = l[:-1] + compose(l_last[0], 'ㅜ', ' ')
            r_canon = compose('ㅇ', 'ㅓ', l_last[2]) + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # 오 불규칙 활용: 왔 + 어 -> 오다
        if l_last[1] == 'ㅘ':
            l_stem = l[:-1] + compose(l_last[0], 'ㅗ', ' ')
            r_canon = compose('ㅇ', 'ㅏ', l_last[2]) + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # ㅡ 탈락 불규칙 활용: 꺼 + '' -> 끄다 / 텄 + 어 -> 트다
        if (l_last[1] == 'ㅓ' or l_last[1] == 'ㅏ'):
            l_stem = l[:-1] + compose(l_last[0], 'ㅡ', ' ')
            r_canon = compose('ㅇ', l_last[1], l_last[2]) + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # 거라, 너라 불규칙 활용
        # '-거라/-너라'를 어미로 취급하면 규칙 활용
        # if (l[-1] == '가') and (r and (r[0] == '라' or r[:2] == '거라')):
        #    # TODO

        # 러 불규칙 활용: 이르 + 러 -> 이르다
        # if (r_first[0] == 'ㄹ' and r_first[1] == 'ㅓ'):
        #     if self.is_stem(l):
        #         # TODO

        # 여 불규칙 활용
        # 하 + 였다 -> 하 + 았다 -> 하다: '였다'를 어미로 취급하면 규칙 활용

        # 여 불규칙 활용 (2)
        # 했 + 다 -> 하 + 았다 / 해 + 라니깐 -> 하 + 아라니깐 / 했 + 었다 -> 하 + 았었다
        if l_last[0] == 'ㅎ' and l_last[1] == 'ㅐ':
            l_stem = l[:-1] + '하'
            r_canon = compose('ㅇ', 'ㅏ', l_last[2]) + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # ㅎ (탈락) 불규칙 활용
        # 파라 + 면 -> 파랗다
        if (l_last[2] == ' ' or l_last[2] == 'ㄴ' or l_last[2] == 'ㄹ' or l_last[2] == 'ㅂ' or l_last[2] == 'ㅆ'):
            l_stem = l[:-1] + compose(l_last[0], l_last[1], 'ㅎ')
            r_canon = r if l_last[2] == ' ' else l_last[2] + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        # ㅎ (축약) 불규칙 할용
        # 시퍼렜 + 다 -> 시퍼렇다, 파랬 + 다 -> 파랗다, 파래 + '' -> 파랗다
        if (l_last[1] == 'ㅐ') or (l_last[1] == 'ㅔ'):
            # exception : 그렇 + 아 -> 그래
            if len(l) >= 2 and l[-2] == '그' and l_last[0] == 'ㄹ':
                l_stem = l[:-1] + '렇'
            else:
                l_stem = l[:-1] + compose(l_last[0], 'ㅓ' if l_last[1] == 'ㅔ' else 'ㅏ', 'ㅎ')
            r_canon = compose('ㅇ', 'ㅓ' if l_last[1] == 'ㅔ' else 'ㅏ', l_last[2]) + r
            if self.is_stem(l_stem):
                candidates.add((l_stem, r_canon))

        ## Pre-defined set
        if (l, r) in self._predefined:
            for stem in self._predefined[(l, r)]:
                candidates.add(stem)

        return candidates

stems = {
    '가소롭', '겁',
    '괴롭', '그립',
    '기운없',  '놀랍', '감미롭',
}

testset = [
    '가소로운','가소로울','가소로웠다','가소로워서','가소롭다',
    '괴롭다','괴로운','괴로울',
    '그리워','그립다','그리운','그리웠다','그리울','그리움',
]

lemmatizer = Lemmatizer(stems = stems)

for word in testset:
    candidates = lemmatizer.candidates(word)
    # print('{} : {}'.format(word, candidates))
