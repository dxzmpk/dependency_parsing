from preprocessing import ReadData
import json
import numpy as np


def parse_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        line = f.readline()
        words_dict = (json.loads(line))
    return words_dict


def save_json_data(dics, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dics, ensure_ascii=False) + '\n')
        f.flush()


def get_word_dict(type = 'train'):
    # 建立词典
    # 词典格式为 {word1:{pos,id}, word2:{pos, id}}
    sen_list = ReadData().readfile(type)

    words_dict = {}
    index = 0

    for sentence in sen_list:
        for word in sentence:
            if word not in words_dict:
                words_dict[word] = {'id': index, 'cpostag': sentence[word]['cpostag'], 'postag': sentence[word]['postag']}
                index += 1
            else:
                continue

    save_json_data(words_dict, './data/word_dict.json')


# 供外部使用
def get_one_hot(word_dict, word):
    """
    :param word_dict: 词典
    :param word: 根据词典得到其one-hot编码
    :return:表示word的one-hot向量
    """
    a = np.zeros(len(word_dict))
    a[word_dict[word]['id']] = 1
    return a

# word_dict = parse_json_data('./data/word_dict.json')
# print(word_dict['世界'])
# print(word_dict['好莱坞']['id'])
#
# print(len(word_dict))
#
# a = np.zeros(len(word_dict))
# a[word_dict['好莱坞']['id']] = 1
# print(a[14676:])
# print(get_one_hot(word_dict, '好莱坞'))

get_word_dict('train')