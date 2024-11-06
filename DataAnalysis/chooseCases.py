import csv
import pandas as pd

class Choose:
    '''
    挑选一部分案例进行标注

    总共是十种类别（均是安全类）
    挑选的案例总数： 90
        分别是：
        SASE : 8
        LAS : 8
        DAS : 10
        BBC : 10
        XSEC : 4
        SIP : 10
        EDR : 10
        SSL : 10
        AF : 10
        AC : 10
    '''
    def aLittleCase(self):
        input_file_name = "SXF_cases.csv"
        with open(input_file_name, encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
            header = next(csv_reader)
            clses = ['SASE', 'LAS', 'DAS', 'BBC', 'XSEC', 'SIP', 'EDR', 'aTRUST', 'SSL', \
                     'AF', 'AC']
            count = {'SASE': 10, 'LAS': 10, 'DAS': 10, 'BBC': 10, 'XSEC': 10, 'SIP': 10, 'EDR': 10, \
                     'aTRUST': 10, 'SSL': 10, 'AF': 10, 'AC': 10}
            cases = []
            for row in csv_reader:
                case_class = row[0].split("】")[0][1:].strip().upper()
                if case_class in clses:
                    if count[case_class]>0:
                        count[case_class] -= 1
                        cases.append(row)
                #特殊处理
                elif row[0] in ["【Xsec&CSSP】集群地址登陆控制台无法登陆，提示限制登陆","XSEC组件登录之组件登录显示403登录错误","【CSSP】自定义应用之Linux系统网卡重启失败"]:
                    count['XSEC']-=1
                    row[0] = '【Xsec】'+row[0].split("】")[1] if "】"in row[0] else '【Xsec】'+row[0]
                    cases.append(row)

            cases.sort()
            print("挑选的案例总数：",len(cases))
            print("分别是：")
            for i in range(11):
                c = clses[i]
                print(c,":",10-count[c])

            added_header = ['故障标题', '关键字', '故障-问题描述', '故障-告警信息', '故障-处理过程', \
                            '故障-有效排查步骤', '故障-根因', '故障-解决方案', \
                            '故障-建议与总结', '文档编号', '作者', '更新时间', '适用版本']
            csvfile = open("a_little_cases.csv", "w", encoding="utf-8", newline="")
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(added_header)
            for case in cases:
                writer.writerow(case)


    '''
    去除图片和空格
    '''
    def splitImageAndBlank(self):
        input_file_name = "SXF_cases.csv"
        added_header = ['故障标题', '关键字', '故障-问题描述', '故障-告警信息', '故障-处理过程', \
                        '故障-有效排查步骤', '故障-根因', '故障-解决方案', \
                        '故障-建议与总结', '文档编号', '作者', '更新时间', '适用版本']
        csvfile = open("SXF_cases_splitImage.csv", "w", encoding="utf-8", newline="")
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(added_header)
        with open(input_file_name, encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
            header = next(csv_reader)
            for row in csv_reader:
                for id_p,part in enumerate(row):
                    part = part.strip("\n")
                    part = part.split("\n")
                    deled = []
                    for i,line in enumerate(part):
                        if line=="下载附件":
                            deled+=[i-1,i,i+1]
                    row[id_p] = ""
                    for i in range(len(part)):
                        if i not in deled:
                            row[id_p]+=part[i]
                            row[id_p]+='\n'
                    # row[id_p] = row[id_p].strip('\n')
                    row[id_p] = row[id_p].replace(u'\xa0', '')
                    row[id_p] = row[id_p].replace("\n", '。')
                writer.writerow(row)



    '''
    截图数据
    '''
    def Jietu(self):
        input_file_name = "SXF_cases_splitImage.csv"
        added_header = ["cid","author","update_time","version","c_keywords","c_title","c_description",\
                        "c_warning","c_processing","c_cause","c_solution"]
        csvfile = open("SXF_cases_jietu.csv", "w", encoding="utf-8", newline="")
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(added_header)
        with open(input_file_name, encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
            header = next(csv_reader)
            for row in csv_reader:
                new_row=[""]*11
                for id_p, part in enumerate(row):
                    part=part.strip("。")
                    if id_p==0: #故障标题
                        new_row[5]=part
                    elif id_p==1: #关键字
                        new_row[4] = part
                    elif id_p==2: #问题描述
                        new_row[6] = part
                    elif id_p==3: #告警信息
                        new_row[7] = part
                    elif id_p==4: #处理过程
                        new_row[8] = part
                    elif id_p==6: #根因
                        new_row[9] = part
                    elif id_p==7: #解决方案
                        new_row[10] = part
                    elif id_p==9: #文档编号
                        new_row[0] = part
                    elif id_p==10: #作者
                        new_row[1] = part
                    elif id_p==11: #更新时间
                        new_row[2] = part
                    elif id_p==12: #适用版本
                        new_row[3] = part

                writer.writerow(new_row)

    '''
    求最长公共子串
    '''
    def getNumofCommonSubstr(self, str1, str2):

        lstr1 = len(str1)
        lstr2 = len(str2)
        record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
        maxNum = 0  # 最长匹配长度
        p = 0  # 匹配的起始位

        for i in range(lstr1):
            for j in range(lstr2):
                if str1[i] == str2[j]:
                    # 相同则累加
                    record[i + 1][j + 1] = record[i][j] + 1
                    if record[i + 1][j + 1] > maxNum:
                        # 获取最大匹配长度
                        maxNum = record[i + 1][j + 1]
                        # 记录最大匹配长度的终止位置
                        p = i + 1
        return str1[p - maxNum:p]


    def chooseCase(self):
        classes = ['故障-问题标题','故障-问题描述','故障-告警信息','故障-处理过程','故障-有效排查步骤','故障-根因','故障-解决方案','故障-建议与总结']
        input_file_name = "SXF_cases_splitImage.csv"
        text_file_name = "../a_keyword_extraction_experiment/data/origin_text.csv"
        keyword_file_name = "../a_keyword_extraction_experiment/data/keyword_filted.txt"
        # text_file = open(text_file_name, "w", encoding="utf-8")
        text_file = open(text_file_name, 'w', encoding='utf-8',newline="")
        keyword_file = open(keyword_file_name, "w", encoding="utf-8")

        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(text_file)

        # 3. 构建列表头
        csv_writer.writerow(["id", "title", "description"])


        id = 0
        with open(input_file_name, encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
            header = next(csv_reader)
            '''提取类别信息'''
            # for row in csv_reader:
            #     row[0] = row[0].rstrip("。")+"。"
            #     if "】" in row[0]:
            #         cls = row[0].split("】")[0][1:]
            #         text = row[0].split("】")[1]+row[2]
            #         output_file.write(cls+" "+text+row[1])
            #         output_file.write("\n")
            '''提取关键词信息'''
            for row in csv_reader:
                keywords = row[1].strip("。").split("|")
                keywords_filted = []
                if keywords!=[""]:
                    title = row[0].strip("。")
                    description = row[2].strip("。")
                    csv_writer.writerow([id, title, description])
                    text = title + description
                    for kw in keywords:
                        common_kw = self.getNumofCommonSubstr(text, kw)
                        if common_kw:
                            keywords_filted.append(common_kw)
                    keyword_file.write("\t".join(keywords_filted)+"\n")
                    id+=1
        text_file.close()
        keyword_file.close()


solution = Choose()
# solution.aLittleCase()
# solution.splitImageAndBlank()
solution.chooseCase()
# solution.Jietu()




