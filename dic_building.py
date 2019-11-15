from preprocessing import ReadData
import json
import numpy as np
import os


def parse_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        line = f.readline()
        words_dict = (json.loads(line))
    return words_dict


def save_json_data(dics, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dics, ensure_ascii=False) + '\n')
        f.flush()

def line2word(line):
    # 将输入的一行解释为一个单词，作为dict输出
    word = {}
    tags = line.split('\t')
    word['id'] = int(tags[0].strip())
    word['lemma'] = tags[1].strip()
    word['cpostag'] = tags[3].strip()
    word['postag'] = tags[4].strip()
    word['head'] = int(tags[6].strip())
    word['deprel'] = tags[7].strip()
    return word

def get_tags_dict(type = 'train'):

    pos_dic = {}
    # 读入数据，默认为训练数据
    index = 0
    path = os.path.join('.', 'data', type + '.conll')
    with open(path, 'r', encoding='utf-8') as f:
        # 存储句子列表
        sentence_list = []
        lines = f.readlines()
        sentence = []
        for line in lines:
            # 对于每一个句子，都生成一个子列表
            # 子列表中包含所有的词
            # 如果句子为空行，则将此句子合并到句子列表中
            if line != '\n':
                word = line2word(line)
                if word['postag'] not in pos_dic:
                    pos_dic[word['postag']] = index
                    index += 1
    save_json_data(pos_dic, './data/pos_dict.json')





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
    # 多留两个位置，为null和ROOT
    a = np.zeros(len(word_dict)+2)
    if word == 'null':
        a[len(word_dict)] = 1
    elif word == 'ROOT':
        a[len(word_dict)+1] = 1
    else:
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

# get_word_dict('train')