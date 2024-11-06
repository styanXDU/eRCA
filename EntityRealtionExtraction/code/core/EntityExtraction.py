'''
对输入文本抽取实体，建立实体字典
'''
from pyhanlp import *
import os
import re
import shutil
import functools
import  gc
sys.path.append("..")  # 先跳出当前目录
from demo.pos_demo import ExtractionDemo

class EntityExtraction:
    def __init__(self, input_file_path, split=False, split_size=10000):
        """
        初始化函数
        :param input_file_path: 输入 txt格式文件的绝对路径（字符串）
        :param output_path: 输出结果文件的文件夹绝对路径（字符串）----固定
        :param split: 是否对输入文件进行拆分处理，默认为 False
        :param split_size: 若对文件进行拆分处理，则输入拆分的大小，即文件的行数，默认为 10000
        """
        self.__input_file_path = input_file_path
        # self.__output_path = output_path
        self.__output_path = "data/entity_dict_text/"
        self.__split = split
        self.__split_size = split_size
        self.__result_content_filenames = []
        self.__result_entity_filenames = []
        self.__check()
        self.__get_filename()
        self.__triple_txt = "data/pos_data.json"
        #对三元组结果文件进行清空
        # if os.path.isfile(self.__triple_txt):
        print("初始化：清空之前的实体和文本")
        shutil.rmtree("data/entity_dict_text")
        os.mkdir("data/entity_dict_text")
            # print("初始化：清空之前的三元组抽取结果")
            # os.remove(self.__triple_txt)

    def start(self):
        """
        实体抽取
        :return:
        """
        print('实体抽取开始')
        file_name_number = 0
        entity = set()
        content = []
        line_num = 0
        with open(self.__input_file_path, 'r', encoding='utf-8') as r:
            for line in r:
                if line == '' or line is None:
                    continue
                line = self.__get_content_1(line)
                entity_temp = self.__get_entity_by_re(line)
                for e in entity_temp:
                    entity.add(e)
                entity_temp = self.__get_entity_by_hanlp(line)
                for e in entity_temp:
                    entity.add(e)
                content.append(self.__get_content_2(line))
                line_num += 1
                if line_num == self.__split_size:
                    with open(self.__output_path + self.__result_content_filenames[file_name_number], 'w',
                              encoding='utf-8') as w:
                        for s in content:
                            w.write(s)
                            w.write('\n')
                    content.clear()
                    print(self.__result_content_filenames[file_name_number] + ' 写入完成')
                    with open(self.__output_path + self.__result_entity_filenames[file_name_number], 'w',
                              encoding='utf-8') as w:
                        for s in sorted(list(entity), key=functools.cmp_to_key(EntityExtraction.__my_sort)):
                            w.write(s)
                            w.write('\n')
                    print(self.__result_entity_filenames[file_name_number] + ' 写入完成')
                    entity.clear()
                    line_num = 0
                    file_name_number += 1
        if len(entity) > 0:
            with open(self.__output_path + self.__result_content_filenames[file_name_number], 'w',
                      encoding='utf-8') as w:
                for s in content:
                    w.write(s)
                    w.write('\n')
            content.clear()
            print(self.__result_content_filenames[file_name_number] + ' 写入完成')
            with open(self.__output_path + self.__result_entity_filenames[file_name_number], 'w',
                      encoding='utf-8') as w:
                for s in sorted(list(entity), key=functools.cmp_to_key(EntityExtraction.__my_sort)):
                    w.write(s)
                    w.write('\n')
            entity.clear()
            print(self.__result_entity_filenames[file_name_number] + ' 写入完成')
        print('实体抽取完成')

    def extract_start(self, output_file):
        """
        对已经切分好的文件读取并进行抽取
        :return: 抽取完成的三元组文件
        """
        print("三元组抽取开始")
        filted_text_dir = "data/entity_dict_text"
        filecount = len([lists for lists in os.listdir(filted_text_dir) if os.path.isfile(os.path.join(filted_text_dir, lists))])
        textnum = filecount//2
        filename = os.path.basename(self.__input_file_path)
        for i in range(1,textnum + 1):
            f_text_path = "正文-" + str(i) + "-"+ filename
            filted_entity_path = "data/entity_dict_text/实体-"+ str(i) + "-"+ filename
            filted_text_path = "data/entity_dict_text/正文-" + str(i) + "-"+ filename
            TripleExtraction = ExtractionDemo(filted_text_path, filted_entity_path, output_file)
            TripleExtraction.start()
            print( f_text_path + ' 抽取完成')
        print("三元组抽取完成")

    def __get_entity_by_re(self, line):
        """
        通过正则表达式对一行文本进行实体抽取
        :param line: 一行文本（字符串）
        :return: 一个set集合，元素为实体字符串
        """
        # 匹配形如 F / A - 18“尖端神经中心” 、 “白杨”-M、“三叉戟”Ⅱ 、D5LE、“民兵”Ⅲ
        r1 = '[-0-9a-zA-Z/ ⅡⅢⅠⅣⅤⅥⅦⅧⅨⅩⅪⅫ]*[“"][^，"“”。了的我这、不没否在：:为但而]{0,30}?[”"][-0-9a-zA-Z/ ⅡⅢⅠⅣⅤⅥⅦⅧⅨⅩⅪⅫ]*'
        # 匹配形如 VVER - 1000 / V - 320、F / A - 18、2 - 2、B - 21、F / A - 18 、E / F
        r2 = '[-0-9a-zA-Z/ ]+[/-][-0-9a-zA-Z/ ]+'
        # 匹配形如 《中导条约》
        r3 = '(?<=《).*?(?=》)'
        # 匹配形如 GPS Ⅲ
        r4 = '[-0-9a-zA-Z/ ]+[ⅡⅢⅠⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+'
        # 匹配形如MK54 、MOD 2
        r5 = '[0-9A-Z][0-9a-zA-Z]{0,10}[0-9a-zA-Z \\s]{0,20}'
        # 匹配形如199.2
        r6 = '[0-9]+[.][0-9]+'

        regex = r1 + '|' + r2 + '|' + r3 + '|' + r4 + '|' + r5 + '|' + r6
        pattern = re.compile(regex)
        entity_temp = pattern.findall(line)
        # 去除实体中的特殊字符及书名号、引号
        regex = '[^\u4E00-\uFA29\uE7C7-\uE7F3 a-zA-Z0-9_\\-`~!\\\\@#$%^&*+=|:;,・·./?~！@#￥%……&*——+|；：。，、？ⅡⅢⅠⅣⅤⅥⅦⅧⅨⅩⅪⅫ]{0,}|的'
        pattern = re.compile(regex)
        entity = set()
        for e in entity_temp:
            ee = self.__filter_entity(pattern.sub('', e))
            if ee is not None:
                entity.add(ee)
        return entity

    def __get_entity_by_hanlp(self, line):
        """
        使用hanlp进行命名实体识别
        :param line: 一行文本（字符串）
        :return: 一个set集合，元素为实体字符串
        """
        # 将文本分句处理
        lines = line.split('。')
        entity = set()
        NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
        for line in lines:
            # print(line)
            terms = NLPTokenizer.segment(line)
            entity_temp = self.__get_n(terms, line)
            for e in entity_temp:
                if e is not None:
                    entity.add(e)
            terms = HanLP.newSegment().enableTranslatedNameRecognize(True).seg(line)
            entity_temp = self.__get_n(terms, line)
            for e in entity_temp:
                if e is not None:
                    entity.add(e)
            terms = HanLP.newSegment().enableOrganizationRecognize(True).seg(line)
            entity_temp = self.__get_n(terms, line)
            for e in entity_temp:
                if e is not None:
                    entity.add(e)
        return list(entity)

    def __get_n(self, terms, line):
        """
        对由hanlp识别出的命名实体进行筛选
        :param terms: 使用hanlp在line中是别出的词的列表
        :param line: 一行文本中的一句
        :return: 一个set集合，元素为实体字符串
        """
        entity = set()
        index = 0
        while index < len(terms):
            term = terms[index]
            word = str(term.word)
            nature = str(term.nature)
            temp_word = ''

            word = word.strip()
            # 去掉过长和由五个以上单词组成的实体，去掉仅由数字空格和小写英文字母组成的实体，去掉由小写字母开头的实体
            if len(word.split(' ')) > 5 or len(word) > 50 or len(re.sub('[0-9a-z \\s]', '', word)) == 0 or (
                    len(word) > 0 and re.match('[a-z]', word[0])):
                index += 1
                continue
            # 去掉实体中包含以下内容的实体
            if re.search('[:;：；，。,.]', word) or re.match('[0-9一二三四五六七八九十]+[年].*', word):
                index += 1
                continue
            # 若实体开头包含以下内容，则对实体进行裁剪
            if re.match('有关.*|都有.*', word):
                word = word[2:]
            if re.match('有.*', word) and re.match('v', str(HanLP.segment(word)[0].nature)):
                word = word[1:]

            if re.match('.*nr.*', nature):
                # 处理音译人名
                if index + 1 < len(terms) and index + 2 < len(terms) and re.match('[・·].*', str(
                        terms[index + 1].word)) and re.match('.*nr.*', str(terms[index + 2].nature)):
                    temp_word = word + str(terms[index + 1].word) + str(terms[index + 2].word)
                    index += 2
                elif index + 1 < len(terms) and re.match('.*[・·]', word) and re.match('.*nr.*', str(terms[index + 1].nature)):
                    temp_word = word + str(terms[index + 1].word)
                    index += 1
                elif index + 1 < len(terms) and re.match('[・·].*', str(terms[index + 1].word)) and re.match('.*nr.*', str(terms[index + 1].nature)):
                    temp_word = word + str(terms[index + 1].word)
                    index += 1
                else:
                    temp_word = word
            elif re.match('.*ns.*|.*nx.*|.*nz.*', nature):
                temp_word = word
            elif re.match('.*ni.*|.*nt.*', nature):
                if re.match('年.*|年代.*|项.*|架.*', word) and re.match('.*[0-9一二三四五六七八九十]+([年项架]+|年代).*', line):
                    if re.match('年代.*', word):
                        word = word[2:]
                    else:
                        word = word[1:]
                terms_temp = HanLP.newSegment().enableTranslatedNameRecognize(True).seg(word)
                e = None
                if len(terms_temp) > 1:
                    for t in terms_temp:
                        if re.match('p.*|d.*', str(t.nature)) and e is not None:
                            self.__split_entity_from_hanlp(e, entity)
                            e = None
                        elif re.match('p.*|d.*', str(t.nature)) and e is None:
                            pass
                        else:
                            if e is None:
                                e = ''
                            e += str(t.word)
                else:
                    self.__split_entity_from_hanlp(word, entity)
                if e is not None:
                    self.__split_entity_from_hanlp(e, entity)
            if temp_word != '':
                ee = self.__filter_entity(self.__deal_entity_from_hanlp(temp_word))
                if ee is not None:
                    entity.add(ee)
            index += 1
        return list(entity)

    def __split_entity_from_hanlp(self, e, entity):
        """
        对由hanlp识别出的实体进行分割处理
        :param e: 一个实体字符串
        :param entity: 实体集合
        :return: 返回修改后的实体集合
        """
        # 若实体中包含以下汉字，则对其进行分割
        s_list = ['已经', '已向', '已同', '已']
        if re.match('.*' + '为' + '.*', e):
            for ee in e.split('为'):
                entity.add(self.__filter_entity(self.__deal_entity_from_hanlp(ee)))
        if re.match('.*' + '以及' + '.*', e):
            for ee in e.split('以及'):
                entity.add(self.__filter_entity(self.__deal_entity_from_hanlp(ee)))
        flag = True
        for s in s_list:
            if re.match('.*' + s + '.*', e):
                for ee in e.split(s):
                    entity.add(self.__filter_entity(self.__deal_entity_from_hanlp(ee)))
                flag = False
                break
        if flag:
            entity.add(self.__filter_entity(self.__deal_entity_from_hanlp(e)))

    def __get_filename(self):
        """
        生成输出文件名
        :return:
        """
        filename = os.path.basename(self.__input_file_path)
        count = -1
        # 获取文件行数
        for count, line in enumerate(open(self.__input_file_path, 'r', encoding='utf-8')):
            pass
        count += 1
        file_num = 1
        # 根据参数进行输出文件名的生成
        if self.__split is not True or count <= self.__split_size:
            self.__split_size = count
            self.__result_content_filenames.append('正文-' +"1"+"-"+ filename)
            self.__result_entity_filenames.append('实体-' +"1"+"-"+ filename)
        else:
            file_num = count // self.__split_size
            r = count % self.__split_size
            if r > 0:
                file_num += 1
            for i in range(1, file_num + 1):
                self.__result_content_filenames.append('正文-' + str(i) + '-' + filename)
                self.__result_entity_filenames.append('实体-' + str(i) + '-' + filename)
        print('文件：' + self.__input_file_path + ' 共 ' + str(count) + '行，将被分为 ' + str(file_num) + ' 个文件')

    def __check(self):
        """
        判断输入参数是否正确
        :return:
        """
        if os.path.exists(self.__input_file_path) is not True:
            print('请输入正确的文件的绝对路径')
            exit(-1)
        if os.path.isfile(self.__input_file_path) is not True:
            print('请输入文件的绝对路径，而不是文件夹路径')
            exit(-1)
        if self.__input_file_path.split('.')[-1] != 'txt':
            print('请输入txt格式文件')
            exit(-1)
        if os.path.exists(self.__output_path) is not True:
            os.makedirs(self.__output_path)

    @staticmethod
    def __get_content_1(line):
        """
        对一行文本进行预处理，删除括号内容以及网页链接
        :param line: 一行文本
        :return:
        """
        regex = '[\\(（].*?[\\)）]|[\\[【].*?[\\]】]'
        pattern = re.compile(regex)
        line = pattern.sub('', line)
        return line.strip()

    @staticmethod
    def __get_content_2(line):
        """
        对一行文本进行2次处理，删除特殊字符以及其他句子结构
        :param line: 一行文本
        :return:
        """
        lines = line.split('。')
        line = ''
        for l in lines:
            if re.match('.*是[^,.，。]*?的.*', l) is not True:
                line = line + l + '。'

        regex = '[^\u4E00-\uFA29\uE7C7-\uE7F3 a-zA-Z0-9_\\-`~!\\\\@#$%^&*+=|:;,・·./?~！@#￥%……&*——+|；：。，、？ⅡⅢⅠⅣⅤⅥⅦⅧⅨⅩⅪⅫ]{0,}' \
                '|在[^,.，。]*?情况下[,，。.]*|在[^,.，。]*?之际[,，。.]*|在[^,.，。]*?之初[,，。.]*|自[^,.，。]*?以来[,，。.]*' \
                '|从[^,.，。]*?以来[,，。.]*|在[^,.，。]*?中[,，。.]*|的'
        pattern = re.compile(regex)
        line = pattern.sub('', line)
        return line.strip()

    @staticmethod
    def __deal_entity_from_hanlp(entity):
        """
        处理由hanlp识别出的实体
        :param entity: 实体字符串
        :return: 实体字符串或None
        """
        if entity is None:
            return None
        regex = '[^\u4E00-\uFA29\uE7C7-\uE7F3 a-zA-Z0-9_\\-`~!\\\\@#$%^&*+=|:;,・·./?~！@#￥%……&*——+|；：。，、？ⅡⅢⅠⅣⅤⅥⅦⅧⅨⅩⅪⅫ]{0,}|的'
        pattern = re.compile(regex)
        entity = pattern.sub('', entity)
        entity = entity.strip()
        if re.match('[,.，。；;:：]', entity):
            entity = re.sub('[,.，。；;:：]+', '', entity, flags=1)
        if re.match('生产|开发|安装', entity):
            entity = re.sub('生产|开发|安装', '', entity, flags=1)
        if re.match('[但而由如则及其将该来于]', entity):
            entity = re.sub('[但而由如则及其将该来于]', '', entity, flags=1)
        if re.match('.*有史以来.*|绝大多数.*', entity):
            entity = re.sub('有史以来|绝大多数', '', entity)
        if re.match('比如|及其|将会|将要|许多|若干|继续|每个|很多|大量|多种|多家|一些|一个|一种|一套|一名', entity):
            entity = re.sub('比如|及其|将会|将要|许多|若干|继续|每个|很多|大量|多种|多家|一些|一个|一种|一套|一名', '', entity)
        if len(entity) > 0 and entity[-1] == '有':
            entity = entity[:-1]
        entity.strip()
        if len(entity) <= 2:
            entity = None
        return entity

    @staticmethod
    def __filter_entity(e):
        """
        对实体进行筛选
        :param e: 实体字符串
        :return: 实体字符串或None
        """
        if e is None:
            return None
        e = e.strip()
        if len(e) < 2:
            return None
        if re.search('[，,。.?？！!]', e):
            return None
        if len(e) == 3 and re.match('[0-9][\u4E00-\uFA29\uE7C7-\uE7F3]{2}|[0-9]{2}[\u4E00-\uFA29\uE7C7-\uE7F3]', e):
            return None
        if len(e) > 100:
            return None
        if re.match('.*只有.*|.*之间.*|.*可能.*|.*至少.*|.*还有.*|.*此次.*|.*那么.*|.*如何.*|.*需要.*', e):
            return None
        if len(re.sub('[0-9 a-zA-Z\\-]', '', e)) == 0:
            # print(entity)
            ss = e.split(' ')
            # print(ss)
            if re.match('[^A-Z 0-9]+', ss[0]):
                return None
            if re.match('[^A-Z 0-9]+', ss[-1]):
                return None
            if len(ss[-1]) < 4 and len(re.sub('[A-Z0-9a-z\\-]', '', ss[-1])) == 0:
                return None
        if len(re.sub('[0-9 *?？]', '', e)) == 0 or re.match('[-・=/一$#@!*&^%]', e[0]) or re.match('[-・=/一$#@!*&^%]', e[-1]):
            return None
        if len(e) >= 2 and len(re.sub('[a-zA-Z]', '', e)) > 0:
            return e

    @staticmethod
    def __my_sort(s1, s2):
        """
        自定义字符串比较函数
        :param s1:
        :param s2:
        :return:
        """
        if len(s1) > len(s2):
            return -1
        if len(s2) > len(s1):
            return 1
        return 0


if __name__ == '__main__':
    input_dir = 'E:\军事知识抽取\深度学习--军事知识抽取\合并版--200种关系'
    files = os.listdir(input_dir)  # 得到文件夹下的所有文件名称
    files.sort()  # 排序
    # pred_str = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            # pred_str.append(file.split(".txt")[0])
            print('------------------------------------------')
            print(file)
            print('------------------------------------------')
            input_text = input_dir + '\\'+ file
            print(input_text)
            # 首先建立实体字典，，对文本也进行过滤
            entityExtraction = EntityExtraction(input_text,True,10000)
            entityExtraction.start()
            #接下来是对切分的文件分别抽取三元组
            entityExtraction.extract_start(file)
            # del postag_flag,ner_flag,parse_flag
            gc.collect()