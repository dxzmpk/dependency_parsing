from preprocessing import ReadData
from data_struct import ParseStack
import dic_building as db
import os
import pickle
import numpy as np



def parse_sentence(index, sentence):
    """
    关键函数，根据句法分析树构建分析过程
    :param sentence: 待分析的分析树
    :return: fail:分析错误数
    """
    global fail

    buffer = []
    for word in sentence:
        buffer.append(word)
    parse_steps = []
    operation = 0
    stack = ParseStack() #每次分析开始都新建一个句法分析栈
    # 当栈不是只有ROOT或者buffer长度大于0时，执行此操作
    while stack.get_len() > 1 or len(buffer) > 0:
        if stack.can_left_arc(sentence, buffer):
            head, sub = stack.left_arc()
            operation = 1
            # print('left arc：'+head+"-->"+sub)
        elif stack.can_right_arc(sentence, buffer):
            head, sub = stack.right_arc()
            operation = 2
            # print('right arc：'+head + "-->" + sub)
        elif len(buffer) > 0:
            operation = 3
            word = buffer.pop(0)
            stack.shift(word)
            # print('shift: ' + word['lemma'])
        else:
            operation = 3
            # print("ERROR. PARSE ERROR")
            fail += 1
            # print(index)
            break
        # stack.show_data()
        if len(buffer)>0 :
            buffer_word = buffer[0]['lemma']
            buffer_pos = buffer[0]['postag']

        else:
            buffer_word = 'null'
            buffer_pos = 'null'

        step = [stack.data[-1]['lemma'], stack.data[-1]['postag'], buffer_word, buffer_pos, operation]

        parse_steps.append(step)
    return parse_steps

fail = 0

features_raw_path = os.path.join('.','data','features_raw.txt')
features_code_path = os.path.join('.','data','features_code.txt')

def build_features():
    # --------1/读取训练语料-----------
    sen_list = ReadData().readfile('train')

    # --------2/对所有的句子进行解析-----
    step_list = []
    for index, sentence in enumerate(sen_list):
        step_list.extend(parse_sentence(index, sentence))
    print('错误数目'+str(fail))
    print(len(step_list))
    with open(features_raw_path, "wb") as fp:
        pickle.dump(step_list, fp)

def get_pos_code(tag_dic, postag):
    vec_size = len(tag_dic)
    vec = np.zeros(vec_size)
    vec[tag_dic[postag]] = 1
    return vec

def get_operation_code(operation):
    vec = np.zeros(3)
    vec[operation-1] = 1
    return vec

def encode_features():
    """
    对特征进行编码
    :return:
    """
    # 读入词典
    word_dic_path = os.path.join('.', 'data', 'word_dict.json')
    pos_dic_path = os.path.join('.', 'data', 'pos_dict.json')
    word_dic = db.parse_json_data(word_dic_path)
    pos_dic = db.parse_json_data(pos_dic_path)
    code_list = []
    # 加载特征列表
    with open(features_raw_path, "rb") as fp:
        step_list = pickle.load(fp)
    print('特征数目:' + str(len(step_list)))
    for step in step_list:
        stack_word_code = db.get_one_hot(word_dic, step[0])
        stack_pos_code = get_pos_code(pos_dic, step[1])
        buffer_word_code = db.get_one_hot(word_dic, step[2])
        buffer_pos_code = get_pos_code(pos_dic, step[3])
        label_code = get_operation_code(step[4])
        list_format = list(stack_word_code)+list(stack_pos_code)+list(buffer_word_code)+list(buffer_pos_code)
        # code = np.concatenate((stack_word_code,stack_pos_code,buffer_word_code,buffer_pos_code))
        code_list.append(list_format)
        if(len(code_list)%30000 == 0):
            print(len(code_list))
    return code_list

def save_features():
    code_list = encode_features()
    with open(features_code_path, 'wb') as fp:
        pickle.dump(code_list, fp)

save_features()
# 加载特征矩阵，准备进行训练
with open(features_code_path, 'rb') as fp:
    code_list = pickle.load(fp)
    print(len(code_list))



def test(test_index):
    """
    进行测试，将test_index位置的句子进行解析
    :param test_index:
    :return:
    """
    # --------1/读取训练语料-----------
    sen_list = ReadData().readfile('train')
    parse_sentence(test_index, sen_list[test_index])
    sentence = sen_list[test_index]
    for word_dict in sentence:
        print(word_dict)


