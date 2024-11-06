import jieba.posseg as pseg
# from openEntityRealtionExtraction.code.core import nlp

line = "安装时出现堆栈memcpy+；安装宕机,安装失败"

'''
结巴分词

安装 v
时 n
出现 v
堆栈 n
memcpy eng
+ x
； x
安装 v
宕机 nrt
, x
安装 v
失败 v
'''
print("====jieba分词(精确模式)====")
sentence =pseg.cut(line)
for w in sentence:
    print (w.word,w.flag)
print("==========================")

'''
hanlp

[['安装', 'v'], ['时', 'Ng'], ['出现', 'v'], ['堆栈', 'n'], ['memcpy', 'nx'], ['+', 'w'],
 ['安装', 'v'], ['宕机', 'v'], [',', 'w'], ['安装', 'v'], ['失败', 'v']]
'''
# print("====hanlp分词(精确模式)====")
# print(HanLP.segment(line))
# print("==========================")


'''
ltp

1	安装	v	2	ATT
2	时	n	3	ADV
3	出现	v	0	HED
4	堆栈	v	3	VOB
5	memcpy	ws	4	VOB
6	+	wp	5	WP

1	安装	v	0	HED
2	宕机	n	1	VOB
3	,	wp	1	WP
4	安装	v	1	COO
5	失败	v	4	VOB
'''
# print("====ltp分词(精确模式)====")
# # 分词处理
# lemmas = nlp.segment(line.strip())
# # 词性标注
# words_postag = nlp.postag(lemmas)
# print("==========================")