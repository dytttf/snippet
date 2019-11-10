# coding:utf8
import re
import json
import datetime
from collections import Counter


import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 设置显示中文
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]


def main():
    # 加载数据
    with open("cnblogs_blog.json", encoding="utf8") as f:
        data = json.load(f)
    data_list = list(data.values())

    df = pd.DataFrame(data_list)
    # 转换时间格式
    df["ctime"] = pd.to_datetime(df["ctime"])
    # 去掉30天之外的
    df = df[df["ctime"] > df["ctime"].max() - datetime.timedelta(days=30)]
    # 统计发布时间 按小时
    if 0:
        df["hour"] = df["ctime"].apply(lambda x: x.hour)
        hour_counter = df["hour"].value_counts().sort_index()
        hour_counter.plot.bar()
        plt.show()
    # 统计发布时间 按天
    if 0:
        df["day"] = df["ctime"].apply(lambda x: x.day)
        day_counter = df["day"].value_counts().sort_index()
        day_counter.plot.bar()
        plt.show()
    # 统计作者发文数
    if 0:
        author_counter = df["author"].value_counts()[:100]
        author_counter.plot.bar()
        # 输出前五
        print(author_counter[:5])
        plt.show()
    # 标题摘要top30词云
    if 0:
        for cat in ["title", "summary"]:
            text = re.sub("[^\w]", " ", " ".join(list(df[cat])))
            # 清理空格和单字
            word_counter = Counter([x for x in jieba.cut(text) if len(x.strip()) > 1])
            top_30 = word_counter.most_common(30)
            # 词云
            title_word_cloud = WordCloud(
                background_color="white", font_path="simsun.ttf"
            ).generate_from_frequencies(dict(top_30))
            plt.imshow(title_word_cloud)
            plt.axis("off")
            plt.show()
    #

    return


if __name__ == "__main__":
    main()
    pass
