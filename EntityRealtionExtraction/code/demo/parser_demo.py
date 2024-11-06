import os
import re

import sys
sys.path.append("..")  # 先跳出当前目录
from core.nlp import NLP
from core.extractor import Extractor

if __name__ == '__main__':
    in_path = '../../data/input_text.txt'  # 输入的文本文件
    output_dic = '../../data'  # 输出的处理结果Json文件

    # os.mkdir(output_path)

    print('Start extracting...')

    # 实例化NLP(分词，词性标注，命名实体识别，依存句法分析)
    nlp = NLP()
    num = 1  # 知识三元组
    sent_id = 0
    para_id= 0


    with open(in_path, 'r', encoding='utf-8') as f_in:
        # 分句，获得句子列表
        origin_para = re.split('\n', f_in.read())
        print(origin_para)
        # origin_sentences = f_in.readlines()
        # 遍历每一篇文档中的句子
        for para in origin_para:
            para_id += 1
            origin_sentences = re.split('[。？！；]', para)
            for origin_sentence in origin_sentences:
                if origin_sentence:
                    if (len(origin_sentence) < 6):
                        continue
                    sent_id += 1
                    sent_path = str(sent_id) + '.txt'
                    output_path = os.path.join(output_dic, sent_path)
                    if os.path.isfile(output_path):
                        os.remove(output_path)
                    print(output_path)
                    # file_out.write(origin_sentence)

                    # 分词处理
                    lemmas = nlp.segment(origin_sentence)
                    # 词性标注
                    words_postag = nlp.postag(lemmas)
                    # 命名实体识别
                    words_netag = nlp.netag(words_postag)
                    #     i=0
                    #     for i in range(len(words_netag)):
                    #         # print(words_netag[i].to_string())
                    #         if '基地' in words_netag[i].to_string():
                    #             if words_netag[i-1].postag == 'ns' or len(words_netag[i-1].lemma)==1 and words_netag[i-1].postag =='v':
                    #                print(words_netag[i-1].lemma + words_netag[i].lemma)
                    #                # file_out.write(words_netag[i-1].lemma + words_netag[i].lemma+'\r\n')
                    #             elif words_netag[i-1].postag == 'nh':
                    #                  if words_netag[i-2].postag =='nh':
                    #                     print(words_netag[i-2].lemma+words_netag[i-1].lemma + words_netag[i].lemma)
                    #                     # file_out(words_netag[i-2].lemma+words_netag[i-1].lemma + words_netag[i].lemma+'\r\n')
                    #                  else:
                    #                      print(words_netag[i-1].lemma + words_netag[i].lemma)
                    #                      # file_out(words_netag[i-1].lemma + words_netag[i].lemma+'\r\n')
                    #             else:
                    #                 print(words_netag[i].lemma)
                    #                 # file_out.write(words_netag[i].lemma+'\r\n')
                    #
                    # file_out.close()
                    #
                    # 依存句法分析
                    sentence = nlp.parse(words_netag)
                    # print(sentence.to_string())
                    with open(output_path, "w", encoding='utf-8') as f:
                        f.write(para)
                        f.write('\n')
                        f.write(sentence.to_string())







