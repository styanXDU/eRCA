import sys
import re
import json
import traceback

from tool.append_to_json import AppendToJson

sys.path.append("..")  # 先跳出当前目录
from bean.word_unit import WordUnit
from bean.sentence_unit import SentenceUnit
from bean.entity_pair import EntityPair
from core.extract_by_dsnf import ExtractByDSNF


class Extractor_MY:
    #抽取三元组
    vob_name = ''
    def complete_vob(self,sentence,word_id,name):
        num = max(word_id - 6, 0)
        i = word_id -1  #因为从0开始遍历
        for id in range(0,word_id-1):
            i -= 1
            if (sentence.words[i].postag =='a' or sentence.words[i].dependency == 'ATT' or sentence.words[i].dependency == 'FOB' or  sentence.words[i].postag =='m' or  sentence.words[i].postag =='b'or  sentence.words[i].postag =='wp'):
                name = sentence.words[i].lemma + name
            else :
                break
        return  name
    def complete_pob(self,sentence,word_id,name):
        num = max(word_id - 6 , 0)
        i = word_id - 1  #因为从0开始遍历
        for id in range(0, word_id-1):
            i -= 1
            if sentence.words[i].dependency == 'ATT' or sentence.words[i].dependency == 'FOB' or sentence.words[i].postag =='b' or sentence.words[i].postag =='a' or  sentence.words[i].postag =='m' or sentence.words[i].postag =='wp':
                name = sentence.words[i].lemma + name
            else:
                break
        return name
    def complete_sub(self,sentence,word_id,name):
        num = max(word_id - 6,0)
        i = word_id-1  #因为从0开始遍历
        for id in range(0, word_id-1):
            i -= 1
            # if sentence.words[i].dependency == 'ATT' and ('n' in sentence.words[i].postag or 'a' in sentence.words[i].postag or 'b' in sentence.words[i].postag):
            if (sentence.words[i].dependency == 'ATT' or 'a' in sentence.words[i].postag or 'b' in sentence.words[i].postag) and 'r' not in sentence.words[i].postag:
                name = sentence.words[i].lemma + name
            else:
                break
        return name
    def get_time(self,para,sentence):
        time = ''
        p = re.compile("[0-9年]*[0-9]+月[0-9]+日")
        result = p.search(sentence)
        if result == None:
            result = p.search(para)
        if (result):
            time= result.group()
        # time = sentence.split(' ')[0]
        return time

    def get_pob(self,para,sentence,origin_sentence,time):
        # 将当前的并列主语加入
        subject = []
        triple = []
        num = 0
        verb_full = ''
        vob_pos = ''
        vob_num = 0
        vob_lemma = ''
        self.origin_sentence = origin_sentence
        for q in sentence.words:
            if q.dependency == 'SBV' and ('n' in q.postag or 'b' in q.postag or 'ws' in q.postag):
                subject = []
                num = q.ID
                #subject.append(q.lemma)
                sub = self.complete_sub(sentence,num,q.lemma)
                subject.append(sub)
                for w in sentence.words:
                    if w.dependency == 'COO' and ('n' in w.postag or 'b' in w.postag or 'ws' in w.postag) and w.head == q.ID:
                        #subject.append(w.lemma)
                        sub = self.complete_sub(sentence, w.ID, w.lemma)
                        subject.append(sub)
                #定位POB   15	空军基地	n	12	POB
                for n in range(num+1,len(sentence.words)):
                #for word in sentence.words:
                    word = sentence.words[n]
                    if word.dependency == 'SBV' and ('n' in word.postag or 'k' in word.postag or 'b' in word.postag or 'ws' in word.postag):
                        break
                    if word.dependency == 'POB' and ('q' in word.postag or 'n' in word.postag  or 'j' in word.postag or 'm' in word.postag):  #15	空军基地	n	12	POB   or 'v' in word.postag
                        #根据宾语定位介词   12	从	p	16	ADV
                        head_id = word.head
                        #根据介词定位动词   16	起飞	v	0	HED
                        verb = word.head_word.head_word
                        if verb == None:
                            continue
                        if ('v' in verb.postag):
                            verb_full= verb.lemma
                            verb_id = verb.ID
                            #扩展pob
                            pob_full = self.complete_pob(sentence, word.ID, word.lemma)
                            #扩展verb  #实施 预警指挥
                            for wo in sentence.words:
                                if wo.dependency == 'VOB'and wo.head == verb_id:
                                    vob_pos = wo.postag
                                    vob_num = wo.ID
                                    vob_lemma = wo.lemma
                                    vob_full = self.complete_vob(sentence,wo.ID,wo.lemma)
                                    verb_full = verb.lemma + vob_full
                            for sub in subject:
                                # time = self.get_time(self.para,self.origin_sentence)
                                # if len(time)<3:
                                #     time = 'null'
                                space = 'null'
                                if vob_pos == 'ns':
                                    space = vob_lemma
                                else:
                                    for i in range(0,vob_num):
                                    # for m in sentence.words:
                                        if sentence.words[i].postag == 'ns':
                                            space = sentence.words[i].lemma
                                            break
                                # triple.append(sub+','+verb_full+','+pob_full+','+time+','+space+','+self.origin_sentence)
                                # triple.append('['+'\"'+sub+'\"'+','+'\"'+verb_full+'\"'+','+'\"'+pob_full+'\"'+']')
                                if (verb_full in pob_full):
                                    pob_full = pob_full.replace(verb_full, "")
                                if (len(sub) >= 2 and len(pob_full) >= 2):
                                    triple.append([sub, verb_full, pob_full])   
                                    # triple.append([sub,verb_full,pob_full,time, space, para])
                            #补充并列的pob
                            for i in sentence.words:
                                if i.dependency == 'COO'and (('n' in i.postag  or 'j' in i.postag) or (len(i.lemma)>2 and 'v' in i.postag)) and i.head == word.ID :
                                    vob_pos = i.postag
                                    vob_num = i.ID
                                    vob_lemma = self.complete_pob(sentence, i.ID, i.lemma)
                                    for sub in subject:
                                        # time = self.get_time(self.para,self.origin_sentence)
                                        # if (len(time) < 3):
                                        #     time = 'null'
                                        space = 'null'
                                        if vob_pos == 'ns':
                                            space = vob_lemma
                                        else:
                                            for i in range(0, vob_num):
                                                # for m in sentence.words:
                                                if sentence.words[i].postag == 'ns':
                                                    space = sentence.words[i].lemma
                                                    break
                                        # triple.append(sub+','+verb_full+','+i.lemma+',' + time +','+ space +','+ self.origin_sentence )
                                        # triple.append('[\"'+sub + '\",\"' + verb_full + '\",\"' + i.lemma + '\"]')
                                        # triple.append([sub,verb_full,vob_lemma,time,space,para])
                                        if (verb_full in vob_lemma):
                                            vob_lemma = vob_lemma.replace(verb_full, "")
                                        if (len(sub) >= 2 and len(vob_lemma) >= 2) :
                                            triple.append([sub, verb_full, vob_lemma])
        return triple

    def get_vob2(self, para, sentence, origin_sentence, time):
        triple = []
        for q in sentence.words:
            if q.dependency  == 'VOB' and ('m' in q.postag or 'i' in q.postag or'q' in q.postag or 'n' in q.postag or 'v' in q.postag or 'j' in q.postag):
                count = 0
                locationV = 0
                subject = ''
                object = ''
                predicate = ''
                temp = q
                # 向前寻找20次
                while ('HED' not in temp.dependency and count < 20):
                    index = temp.head
                    name = temp.lemma
                    # 拿到宾语
                    if count == 0:
                        object = self.complete_vob(sentence, temp.ID, name)
                        if 'v' in temp.postag and len(object) <= 2:
                            object = ''
                    # ？？
                    if count == 1:
                        predicate = temp.lemma
                        locationV = temp.ID  # 当前谓语所在的位置
                    count += 1
                    temp = sentence.words[index - 1]  # 因为是从0开始遍历
                # 判断HED和谓词之间是否存在其他主语
                flag = True
                for i in range(temp.ID, locationV):
                    if sentence.words[i].dependency == 'SBV':
                        flag = False
                # 如果存在其他主语，或，核心词语的下一个为标点符号，则不保存
                if (temp.dependency == 'HED' and temp.ID < len(sentence.words) and('wp' not in sentence.words[temp.ID].postag or flag)):
                    # 注意，如果第二个词就是hed，上面无法保存谓语，因为已经跳出循环。
                    if count == 1:
                        predicate = temp.lemma
                    for i in range(0, len(sentence.words)):
                        if(sentence.words[i].ID>temp.ID):
                            break
                        if temp.ID == sentence.words[i].head and sentence.words[i].dependency == 'SBV' and 'v' not in sentence.words[i].postag and 'r' not in sentence.words[i].postag:
                            subject = self.complete_sub(sentence, sentence.words[i].ID, sentence.words[i].lemma)
                            break
                if predicate in object:
                    object = object.replace(predicate, "")
                if subject != '' and object != '' and predicate !='' and (len(subject) >= 2 and len(object) >= 2):
                    triple.append([subject, predicate, object])
        return triple
    def get_vob(self,para,sentence,origin_sentence,time):
        #将当前的并列主语加入
        subject = []
        triple = []
        head = 0
        num = 0
        vob_num = 0
        vob_pos = ''
        self.origin_sentence = origin_sentence
        self.para=para
        for q in sentence.words:
            if q.dependency == 'SBV' and ('n' in q.postag or 'k' in q.postag or 'b' in q.postag or 'ws' in q.postag):
                subject = []
                num = q.ID
                #subject.append(q.lemma)
                sub = self.complete_sub(sentence, num, q.lemma)
                subject.append(sub)
                for w in sentence.words:
                    if w.dependency == 'COO' and ('n' in w.postag  or 'k' in w.postag or 'b' in w.postag or 'ws' in w.postag) and w.head == q.ID:
                        #subject.append(w.lemma)
                        sub = self.complete_sub(sentence, w.ID, w.lemma)
                        subject.append(sub)
                # 定位VOB
                # for word in sentence.words:
                for n in range(num + 1, len(sentence.words)):
                    word = sentence.words[n]
                    if word.dependency == 'SBV' and ('n' in word.postag or 'k' in word.postag or 'b' in word.postag or 'ws' in word.postag):
                        break
                    if word.dependency == 'VOB' and ('ws' in word.postag or 'm' in word.postag or 'i' in word.postag or 'q' in word.postag or 'n' in word.postag or 'v' in word.postag or 'j' in word.postag):   #12	巴士海峡	ns	11	VOB
                        vob_pos = word.postag
                        vob_num = word.ID
                        vob_lemma = word.lemma
                        head = word.head   #11	飞越	v	9	COO
                        vob_full=self.complete_vob(sentence,word.ID,word.lemma)
                        if ('v' in sentence.words[head-1].postag and (vob_pos == 'n' or (len(vob_full) > 2))):#######
                            #print(head)
                            #print(sentence.words[head].to_string())
                            for sub in subject:
                                # time = self.get_time(self.para,self.origin_sentence)
                                # if (len(time) < 3):
                                #     time = 'null'
                                space = 'null'
                                # if vob_pos == 'ns':
                                #     space = vob_lemma
                                # else:
                                #     for i in range(0, vob_num):
                                #         # for m in sentence.words:
                                #         if sentence.words[i].postag == 'ns':
                                #             space = sentence.words[i].lemma
                                #             break
                                # triple.append(sub+','+sentence.words[head-1].lemma+','+vob_full+',' + time +','+ space +','+ self.origin_sentence )
                                # triple.append('[\"'+sub + '\",\"' + sentence.words[head - 1].lemma + '\",\"' + vob_full + '\"]' )
                                # triple.append([sub,sentence.words[head-1].lemma,vob_full,time,space,para])
                                if sentence.words[head - 1].lemma in vob_full:
                                    vob_full = vob_full.replace(sentence.words[head - 1].lemma, "")
                                if (len(sub) >= 2 and  len(vob_full) >= 2) :
                                    triple.append([sub, sentence.words[head - 1].lemma, vob_full])
                            for w in sentence.words:
                                if w.dependency == 'COO'and (('n' in w.postag  or 'j' in w.postag) or (len(w.lemma)>2 and 'v' in w.postag)) and w.head == word.ID:
                                    vob_pos = w.postag
                                    vob_num = w.ID
                                    vob_lemma = w.lemma
                                    vob_full = self.complete_vob(sentence, w.ID,w.lemma)
                                    for sub in subject:
                                        # time = self.get_time(self.para,self.origin_sentence)
                                        # # if (len(time) < 3):
                                        # #     time = 'null'
                                        # space = 'null'
                                        # if vob_pos == 'ns':
                                        #     space = vob_lemma
                                        # else:
                                        #     for i in range(0, vob_num):
                                        #         # for m in sentence.words:
                                        #         if sentence.words[i].postag == 'ns':
                                        #             space = sentence.words[i].lemma
                                        #             break
                                        # triple.append(sub+','+sentence.words[head-1].lemma+','+vob_full+',' + time+',' + space+',' + self.origin_sentence )
                                        # triple.append('[\"'+sub + '\",\"' + sentence.words[head - 1].lemma + '\",\"' + vob_full + '\"]' )
                                        # triple.append([sub,sentence.words[head-1].lemma,vob_full,time,space,para])
                                        if sentence.words[head - 1].lemma in vob_full:
                                            vob_full = vob_full.replace(sentence.words[head - 1].lemma, "")

                                        if(len(sub)>= 2 and len(vob_full)>=2):
                                           triple.append([sub, sentence.words[head - 1].lemma, vob_full])
        return triple

    # def get_vob(self, para, sentence, origin_sentence, time):
    #     subject = []
    #     triple = []
    #     head = 0
    #     num = 0
    #     vob_num = 0
    #     vob_pos = ''
    #     self.origin_sentence = origin_sentence
    #     self.para = para
    #     for q in sentence.words:
    #         if q.dependency == 'SBV' and ('n' in q.postag or 'k' in q.postag or 'b' in q.postag or 'ws' in q.postag):
    #             subject = []
    #             num = q.ID
    #             sub = self.complete_sub(sentence, num, q.lemma)
    #             subject.append(sub)
    #             for w in sentence.words:
    #                 if w.dependency == 'COO' and (
    #                         'n' in w.postag or 'k' in w.postag or 'b' in w.postag or 'ws' in w.postag) and w.head == q.ID:
    #                     sub = self.complete_sub(sentence, w.ID, w.lemma)
    #                     subject.append(sub)
    #             for n in range(num + 1, len(sentence.words)):
    #                 word = sentence.words[n]
    #                 if word.dependency == 'SBV' and (
    #                         'n' in word.postag or 'k' in word.postag or 'b' in word.postag or 'ws' in word.postag):
    #                     break
    #                 if word.dependency == 'VOB' and (
    #                         'ws' in word.postag or 'm' in word.postag or 'i' in word.postag or 'q' in word.postag or 'n' in word.postag or 'v' in word.postag or 'j' in word.postag):  # 12	巴士海峡	ns	11	VOB
    #                     vob_pos = word.postag
    #                     vob_num = word.ID
    #                     vob_lemma = word.lemma
    #                     head = word.head
    #                     vob_full = self.complete_vob(sentence, word.ID, word.lemma)
    #                     if ('v' in sentence.words[head - 1].postag and (vob_pos == 'n' or (len(vob_full) > 2))):
    #                         for sub in subject:
    #                             space = 'null'
    #                             if sentence.words[head - 1].lemma in vob_full:
    #                                 vob_full = vob_full.replace(sentence.words[head - 1].lemma, "")
    #                             if (len(sub) >= 2 and len(vob_full) >= 2) and sentence.words[head - 1].lemma != '是':
    #                                 triple.append([sub, sentence.words[head - 1].lemma, vob_full])
    #                         # 扩展vob
    #                         for w in sentence.words:
    #                             if w.dependency == 'COO' and (('n' in w.postag or 'j' in w.postag) or (
    #                                     len(w.lemma) > 2 and 'v' in w.postag)) and w.head == word.ID:
    #                                 vob_pos = w.postag
    #                                 vob_num = w.ID
    #                                 vob_lemma = w.lemma
    #                                 vob_full = self.complete_vob(sentence, w.ID, w.lemma)
    #                                 for sub in subject:
    #                                     if sentence.words[head - 1].lemma in vob_full:
    #                                         vob_full = vob_full.replace(sentence.words[head - 1].lemma, "")
    #                                     if (len(sub) >= 2 and len(vob_full) >= 2):
    #                                         triple.append([sub, sentence.words[head - 1].lemma, vob_full])
    #     return triple


    '''0去除冗余1,去除：飞机，进入，南海'''
    def delete_triple1(self,triples):
        flag = True
        triple_last = []
        i = -1
        for tri in triples:
            i += 1
            flag = True
            tri_obj = tri[2]
            tri_sub=tri[0]
            for t in triples:
                t_sub = t[0]
                t_verb = t[1]
                if t_sub == tri_sub and tri_obj in t_verb:
                    flag = False
            if flag == True:
                    triple_last.append(triples[i])
        return triple_last
    '''去除冗余2，去除：飞机，进入南海，基地'''
    def delete_triple2(self,triples):
        flag = True
        triple_last = []
        i = -1
        for tri in triples:
            i += 1
            flag = True
            tri_verb = tri[1]
            tri_sub=tri[0]
            for t in triples:
                t_sub = t[0]
                t_obj = t[2]
                if t_sub == tri_sub and t_obj in tri_verb:
                    flag = False
            if flag == True:
                    triple_last.append(triples[i])
        return triple_last

    def extract(self, para,origin_sentence, sentence, file_path,txt_path,msg_num):
        """
        Args:
            origin_sentence: string，原始句子
            sentence: SentenceUnit，句子单元
        Returns:
            num： 知识三元组的数量编号
        """
        self.file_path = file_path
        self.para = para
        self.origin_sentence = origin_sentence
        triples = []
        triple_pob = self.get_pob(para,sentence,origin_sentence)
        for i in triple_pob:
            triples.append(i)
        triple_vob = self.get_vob(para,sentence,origin_sentence)
        for i in triple_vob:
            triples.append(i)
        print('tripples:',triples)
        triple_last = self.delete_triple1(triples)
        print('triple_last:',triple_last)
        msg_time = self.get_time(self.para,self.origin_sentence)  #para：段落
        result = dict()
        result['spos'] = triple_last
        result['msg'] = msg_num
        result['source'] = '海情'
        result['timestr'] = msg_time
        result['txt'] = self.origin_sentence
        AppendToJson().append(self.file_path, result)
        # f = open(txt_path,'a',encoding="utf-8")
        #         # f.write(t)
        #         # f.write('\n')
        #         # f.close()
    def extract_1(self, para,origin_sentence, sentence, file_path,txt_path,msg_num):
        self.file_path = file_path
        self.para = para
        self.origin_sentence = origin_sentence
        triples = []
        result = []
        msg_time = self.get_time(self.para, self.origin_sentence)  # para：段落
        triple_pob = self.get_pob(para, sentence, origin_sentence, msg_time)
        for i in triple_pob:
            triples.append(i)
        triple_vob = self.get_vob(para, sentence, origin_sentence, msg_time)
        for i in triple_vob:
            triples.append(i)
        # triple_vob2 = self.get_vob2(para, sentence, origin_sentence, msg_time)
        # for i in triple_vob2:
        #     triples.append(i)
        print('tripples:', triples)
        triple_last = self.delete_triple1(triples)
        print('triple_last:', triple_last)
        for p in triple_last:
            #AppendToJson().append(self.file_path, p)
            with open(self.file_path, 'a', encoding='utf-8') as f:
                # dumps 将数据转换成字符串
                json_str = json.dumps(p, indent=4, sort_keys=True, ensure_ascii=False)
                f.write(json_str)
                f.write(',')

    def extract_txt(self, para,origin_sentence, sentence, file_path,txt_path,msg_num):
        self.file_path = txt_path
        self.para = para
        self.origin_sentence = origin_sentence
        triples = []
        result = []
        #msg_time = self.get_time(self.para, self.origin_sentence)  # para：段落
        msg_time = 'null'
        triple_pob = self.get_pob(para, sentence, origin_sentence, msg_time)
        for i in triple_pob:
            if i not in triples:
                triples.append(i)
        triple_vob = self.get_vob(para, sentence, origin_sentence, msg_time)
        for i in triple_vob:
            if i not in triples:
                triples.append(i)
        # triple_vob2 = self.get_vob2(para, sentence, origin_sentence, msg_time)
        # for i in triple_vob2:
        #     if i not in triples:
        #         triples.append(i)
        print(origin_sentence)
        # print('tripples:', triples)
        triple_last = self.delete_triple1(triples)
        print('triple_last:', triple_last)
        for p in triple_last:
            #AppendToJson().append(self.file_path, p)
            with open(self.file_path, 'a', encoding='utf-8') as f:
                    f.write(str(p))
                    f.write('\n')

        #将抽取结果写入json文件
        load_dict = {"text":"","spo_list":[]}
        load_dict["text"]=origin_sentence
        load_dict["spo_list"]=triple_last
        json_file = '../../data/knowledge_triple_biaozhu_zhedie.json'
        with open(json_file, 'a',encoding="utf-8") as write_f:
            write_f.write(str(load_dict))
            write_f.write("\n")
        # return load_dict






