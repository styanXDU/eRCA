import csv

'''
right：正确的关键词结果
comp：抽取的结果
k：top-k
'''
def account_metrics(allwords, right, comp, k):
    '''
    TP: 真阳性，是关键词且模型正确预测出来
    FP：假阳性，不是关键词但是模型错误的预测了出来
    TN：真阴性，不是关键词且模型预测不是关键词
    FN：假阴性，是关键词但是模型没有预测出来
    '''
    TP,FP,FN,TN = 0,0,0,0
    allwords_len = len(allwords)
    P_flag = False
    TN_flag = False
    for i in range(k):
        if comp[i] in right:
            TP+=1
            P_flag = True
        else:
            for kw in right:
                if kw in comp[i]:
                    TP+=1
                    P_flag = True
                    break
        if P_flag==False:
            FP+=1
    for w in allwords:
        if w not in comp:
            for kw in right:
                if w in kw or kw in w:
                    FN+=1
                    TN_flag = True
                    break
            if TN_flag==False:
                TN+=1
    P = TP/(TP+FP)
    R = TP/(TP+FN)
    if P+R!=0:
        F1 = 2*P*R/(P+R)
    else:
        F1 = 0
    return P, R, F1







csvFile_name = "result/keys_TFIDF_test.csv"
biaozhuFile_name = "right_keywords.txt"
biaozhu_file = open(biaozhuFile_name, 'r', encoding="utf-8")
biaozhu_lines = biaozhu_file.readlines()

data = []
with open(csvFile_name,'r', encoding="utf-8") as input_file:
    csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
    header = next(csv_reader)
    i = 0
    P,R,F1 = 0,0,0
    for row in csv_reader:
        bz_kw = biaozhu_lines[i].split("\t")
        all_words = row[2].split("\t")
        com_kw = row[3].split("\t")
        metrics = account_metrics(all_words, bz_kw,com_kw,3)
        P+=metrics[0]
        R+=metrics[1]
        F1+=metrics[2]
        i+=1
    print("precision：",P)
    print("recall：",R)
    print("f1：",F1)


