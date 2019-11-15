import os


class ReadData:

    def readfile(self, type='train'):
        #读入数据，默认为训练数据
        path = os.path.join('.', 'data', type+'.conll')
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
                    word = self.line2word(line)
                    sentence.append(word)
                else:
                    sentence_list.append(sentence)
                    sentence = []
            print("训练语料读取完毕")
            return sentence_list

    def line2word(self, line):
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

# 测试本模块功能
# sen_list = ReadData().readfile('dev')
# print(len(sen_list))
# print(sen_list.pop())
# print(sen_list.pop())
