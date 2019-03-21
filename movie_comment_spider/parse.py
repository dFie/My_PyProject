
from redis import Redis
import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class ParseComment:
    def __init__(self, stopwordfile='chineseStopWords.txt'):
        self.redis = Redis()
        self.stopwords = set()
        self.stopwordfile = stopwordfile

    # 获取停用词
    def get_stopwords(self):
        with open(self.stopwordfile, encoding='gbk') as f:
            for line in f:
                self.stopwords.add(line.rstrip('\r\n'))

        items = self.redis.lrange('dbcommit:items', 0, -1)
        return items

    # 统计词频
    def count_word(self):
        items = self.get_stopwords()
        words = {}
        for item in items:
            val = json.loads(item)['comment']
            for word in jieba.cut(val):
                if word not in self.stopwords:
                    words[word] = words.get(word, 0) + 1

        total = len(words)
        freq = {k: v/total for k, v in words.items()}
        return freq

    # 运行
    def run_display(self):
        freq = self.count_word()
        wordcloud = WordCloud(font_path='simhei.ttf', background_color='white', max_font_size=80)

        plt.figure(2)
        wordcloud.fit_words(freq)
        plt.imshow(wordcloud)
        plt.axis('off') # 去掉坐标
        plt.show()

if __name__ == '__main__':
    ParseComment().run_display()
