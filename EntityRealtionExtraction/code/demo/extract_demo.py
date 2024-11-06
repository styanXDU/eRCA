import json
import os
import re
import sys
import time
from tqdm import tqdm
from tqdm._tqdm import trange
import string
sys.path.append("..")  # 先跳出当前目录
from core.nlp import NLP
from core.extract_my import Extractor_MY
# from core.extract_sixyuanzu import Extractor_MY
# from core.run_demo import run_control

if __name__ == '__main__':
    in_path = '../../data/input_text.txt'  # 输入的文本文件
    output_path = '../../data/knowledge_triple.json'  # 输出的处理结果Json文件
    txt_path = '../../data/knowledge_triple.txt'
    if os.path.isfile(output_path):
        os.remove(output_path)
    # os.mkdir(output_path)


    # 实例化NLP(分词，词性标注，命名实体识别，依存句法分析)
    nlp = NLP()
    num = 1  # 知识三元组

    # json_triples = []


    with open(in_path, 'r', encoding='utf-8') as f_in:
        # 分句，获得句子列表
        global msg_num
        msg_num = 1
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
                    #print(origin_sentence)
                    # file_out.write(origin_sentence)

                    # 分词处理
                    lemmas = nlp.segment(origin_sentence.strip())
                    # 词性标注
                    words_postag = nlp.postag(lemmas)
                    # 命名实体识别
                    words_netag = nlp.netag(words_postag)

                    # 依存句法分析
                    sentence = nlp.parse(words_netag)
                    print(sentence.to_string())
                    extractor  = Extractor_MY()
                    # extractor.extract_1(para,origin_sentence, sentence, output_path,txt_path,msg_num)
                    # biaozhu_triples=extractor.extract_txt(para, origin_sentence, sentence, output_path, txt_path, msg_num)
                    extractor.extract_txt(para, origin_sentence, sentence, output_path, txt_path, msg_num)
                    msg_num += 1
                    #run_demo = run_control()
                    #run_demo.run_process()
                    # json_triples.append(biaozhu_triples)


    # #利用抽取结果进行标注
    # json_file = '../../data/knowledge_triple_biaozhu.json'
    # with open(json_file, 'a') as write_f:
    #     write_f.write(json.dumps(json_triples, indent=4, ensure_ascii=False))

