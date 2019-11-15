
# 依存语法推理栈
class ParseStack:

    def __init__(self) -> None:
        self.data = ['ROOT']

    def show_data(self):
        print(self.data)

    def get_len(self):
        return len(self.data)


    def get_head(self, sentence, word):
        """
        内部调用函数，得到当前词在句中的头,以单词的形式返回
        :param sentence:
        :param word:
        :return:
        """
        head_id = sentence[word]['head']
        if head_id == 0:
            return 'ROOT'
        for index, value in sentence.items():
            if value['id'] == head_id:
                return index

    def index2word(self, index, sentence):
        """
        在sentence中找到id为index的词，并返回其单词形式
        :param index:
        :param sentence:
        :return:
        """
        for word, value in sentence.items():
            if value['id'] == index:
                return word

    def can_left_arc(self, sentence, buffer):
        """
        :param sentence: 句子，传入句子的原因是其保存了依赖信息，而我们需要据此判断
               是否满足left-arc执行的条件
        :return: Yes代表当前栈顶可进行left-arc操作， No代表条件不满足
                 即-2的头不是-1
        """

        if len(self.data) < 3:
            return False

        # 开始先判断倒数第二个词是不是别的词的头，如果是的话返回False
        # 避免之后的词无法进行关系的建立
        # 也就是说，只有当缓冲区没有依赖当前要被栈删除的词时，才可以进行left-arc
        for word in buffer:
            temp_head_id = sentence[word]['head']
            if self.index2word(temp_head_id, sentence) == self.data[-2]:
                return False

        # 找到倒数第二个单词的头，看是不是和倒数第一个相同
        head = self.get_head(sentence, self.data[-2])
        return head == self.data[-1]

    def can_right_arc(self, sentence, buffer):
        """
        :param sentence:
        :param buffer: 只有当buffer为空时，才可进行最终的ROOT-->word操作
        :return: Yes代表当前栈顶可进行right-arc操作， No代表条件不满足
                 即-1的头不是-2
        """

        if len(self.data) < 2:
            return False

        # 开始先判断倒数第一个词是不是别的词的头，如果是的话返回False
        # 避免之后的词无法进行关系的建立
        # 也就是说，只有当缓冲区没有依赖当前要被栈删除的词时，才可以进行right-arc
        for word in buffer:
            temp_head_id = sentence[word]['head']
            if self.index2word(temp_head_id, sentence) == self.data[-1]:
                return False

        # 找到倒数第一个单词的头，看是不是和倒数第二个相同
        head = self.get_head(sentence, self.data[-1])

        # 当head为ROOT时，进行拦截，判断缓冲区长度是否为0
        # 只有当缓冲区长度为0时，才可进行ROOT -> word 操作
        if head == 'ROOT' and len(buffer) != 0:
            return False
        return head == self.data[-2]

    def left_arc(self):
        """
        将ROOT后的词弹出
        :return: 返回两个,以列表形式 [head_word, sub_word]
        """
        data_len = len(self.data)
        if len(self.data) < 3:
            print('非法操作！栈中只有 ' +str(len(self.data) ) +'个元素，无法执行left_arc')
            return
        head_word = self.data[-1]
        sub_word = self.data.pop(-2)
        return head_word, sub_word

    def right_arc(self):
        """
        如果data中元素个数为2，弹出[1],返回[0],[1]
                    否则  ，弹出[2],返回[1],[2]
        :return: 返回两个,以列表形式 [head_word, sub_word]
        """
        data_len = len(self.data)
        if data_len == 2:
            head_word = self.data[0]
            sub_word = self.data.pop(1)
        elif data_len >= 3:
            head_word = self.data[-2]
            sub_word = self.data.pop(-1)
        else:
            print('非法操作！栈中只有 ' +str(data_len ) +'个元素，无法执行right_arc')
            return
        return head_word, sub_word

    def shift(self, value):
        """
        :param value: 待移进的词
        :return: 返回移进后数据的数目
        """
        self.data.append(value)
        return len(self.data)

# 测试
# stack = ParseStack()
# stack.shift(1)
# stack.shift(2)
# stack.shift(3)
# stack.show_data()
# stack.shift(4)
# print(stack.left_arc())
# stack.show_data()
# stack.right_arc()
# stack.show_data()
# stack.right_arc()
# stack.show_data()
# print(stack.right_arc())