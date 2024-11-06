import os
import re
import sys
import codecs
import json
import gc
import time
from tqdm import tqdm
from tqdm._tqdm import trange
import string
sys.path.append("..")  # 先跳出当前目录
from core.nlp import NLP
from core.pos_my import Extractor_MY

class ExtractionDemo:
    def __init__(self,in_text_path, in_entity_path,output_file):
        """
        初始化
        :param in_path:输入的已经过滤的文本的路径
        :param in_path:输入的已经抽取的实体的路径
        """
        self.__in_text_path = in_text_path
        self.__output_path = 'result/'+ output_file.split(".txt")[0]+ ".json"  # 输出的处理结果
        self.__in_entity_path = in_entity_path
        # if os.path.isfile(self.__output_path):
        #     os.remove(self.__output_path)

    def start(self):
        # 实例化NLP(分词，词性标注，命名实体识别，依存句法分析)
        nlp = NLP(self.__in_entity_path)

        with open(self.__in_text_path, 'r', encoding='utf-8') as f_in:
            # 分句，获得句子列表
            # global msg_num
            data = []
            origin_para = re.split('\n', f_in.read())
            for para in origin_para:
                origin_sentences = re.split('[。？！；]', para)
                for origin_sentence in origin_sentences:
                    if origin_sentence:
                        if (len(origin_sentence) < 6):
                            continue
                        counts = re.split('[，、]',origin_sentence);
                        if(len(counts)>10):
                            continue

                        # 分词处理
                        lemmas = nlp.segment(origin_sentence.strip())
                        # 词性标注
                        words_postag = nlp.postag(lemmas)
                        # # 命名实体识别
                        words_netag = nlp.netag(words_postag)  #抽取三元组需要
                        # # 依存句法分析
                        sentence = nlp.parse(words_netag)   #抽取三元组需要
                        # print(sentence.to_string())
                        extractor  = Extractor_MY()
                        triple_last = extractor.extract_json(para, origin_sentence, sentence, self.__output_path)
                        if triple_last != []:
                            data.append(
                                {
                                    'text': origin_sentence,
                                    'spo_list': [(i[0], i[1], i[2]) for i in triple_last]
                                }
                            )
        with codecs.open(self.__output_path, 'a', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        del nlp, lemmas, words_postag, words_netag, sentence
        gc.collect()

