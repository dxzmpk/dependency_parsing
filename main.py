from preprocessing import ReadData
from data_struct import ParseStack

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

    stack = ParseStack() #每次分析开始都新建一个句法分析栈
    # 当栈不是只有ROOT或者buffer长度大于0时，执行此操作
    while stack.get_len() > 1 or len(buffer) > 0:
        if stack.can_left_arc(sentence, buffer):
            head, sub = stack.left_arc()
            print('left arc：'+head+"-->"+sub)
        elif stack.can_right_arc(sentence, buffer):
            head, sub = stack.right_arc()
            print('right arc：'+head + "-->" + sub)
        elif len(buffer) > 0:
            word = buffer.pop(0)
            stack.shift(word)
            print('shift: ' + word)
        else:
            print("ERROR. PARSE ERROR")
            fail += 1
            print(index)
            break

fail = 0
sen_list = ReadData().readfile('train')
print('训练语料读取完毕')

for index, sentence in enumerate(sen_list):
    parse_sentence(index, sentence)
print('错误数目'+str(fail))

# test_index = 19998
# parse_sentence(test_index, sen_list[test_index])
# sentence = sen_list[test_index]
# for word in sentence:
#     print(sentence[word]['id'],word, sentence[word]['head'])


