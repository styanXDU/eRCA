#故障标题,关键字,故障-问题描述,故障-告警信息,故障-处理过程,故障-有效排查步骤,故障-根因,故障-解决方案,
# 故障-建议与总结,文档编号,作者,更新时间,适用版本
import csv

class Account:
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


    '''
    案例总数： 5180
    统计关键字的总数：总共有704个关键字
    '''
    def accountKeyWords(self):
        input_file_name = "SXF_cases_splitImage.csv"
        all_keywords = set()
        kw_count = 0
        case_counts = 0
        with open(input_file_name, encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:
                keywords = row[1].strip("。")
                text = row[0] + row[2]
                if keywords!="":
                    case_counts+=1
                for word in row[1].split("|"):
                    word = word.strip("。")
                    kw = self.getNumofCommonSubstr(word,text)
                    if kw:
                        kw_count+=1
                        all_keywords.add(kw)
        print("案例总数：",case_counts)
        print("关键字的总个数：",kw_count)
        print("分别是：")
        print(all_keywords)


    def accountClasses(self):
        input_file_name = "SXF_cases.csv"
        all_classes = dict()
        cases_notclass_count = 0
        with open(input_file_name, encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:
                if "【" not in row[0]:
                    cases_notclass_count+=1
                    print(row[0])
                    continue
                else:
                    case_class = row[0].split("】")[0][1:].strip().upper()
                    if case_class not in all_classes:
                        all_classes[case_class] = 1
                    else:
                        all_classes[case_class]+=1
        print("没有类别的案例总数：",cases_notclass_count)
        print("案例类别的总个数：",len(all_classes))
        print("分别是：")
        print(all_classes)

        #分大类
        Category = {
            "安全类": ['SASE', 'LAS', 'DAS', 'BBC', 'XSEC','XSEC&CSSP', 'SIP','STA', 'EDR', 'aTRUST', 'SSL VPN','SSL','VPN', \
                    'SSLVPN','EMM', 'AF','OSM','GAP', 'AC','AC准入','AC&AF','A','BA','SC','SG','CSSP'],
            "云计算类": ['ADR-H', 'EDS', 'SCP', 'HCI','BVT','HCI-VT','HCI-ARM','HCI-VN','ACLOUD','ACLOU','SCLOUD',\
                     'HCI-监控中心','ACMP','APM','ACOUD','ALCOUD','ASW','标准化排查','标准化场景'],
            "新IT类": ['SDW-R', 'ABOS', 'WOC', 'AD', 'IPSEC', 'ADESK','ADDESK','ADSEK','ADEKS','MIG'],
        }
        Category_count = {
            "安全类": 0,
            "云计算类": 0,
            "新IT类": 0,
        }
        for cls in all_classes:
            if cls in Category["安全类"]:
                Category_count["安全类"]+=all_classes[cls]
            elif cls in Category["云计算类"]:
                Category_count["云计算类"]+=all_classes[cls]
            elif cls in Category["新IT类"]:
                Category_count["新IT类"] += all_classes[cls]
            else:
                print(cls)
                Category_count["云计算类"] += all_classes[cls]

        print(Category_count)

        anquan_count = {'SASE': 0, 'LAS': 0, 'DAS': 0, 'BBC': 0, 'XSEC': 0, 'SIP': 0, 'EDR': 0, \
                             'SSL': 0, 'AF': 0, 'AC': 0}
        for cls in all_classes.keys():
            if cls in ["SASE"]:
                anquan_count["SASE"]+=all_classes[cls]
            elif cls in ["LAS"]:
                anquan_count["LAS"]+=all_classes[cls]
            elif cls in ["DAS"]:
                anquan_count["DAS"]+=all_classes[cls]
            elif cls in ["BBC"]:
                anquan_count["BBC"]+=all_classes[cls]
            elif cls in ["XSEC",'XSEC&CSSP','CSSP']:
                anquan_count["XSEC"]+=all_classes[cls]
            elif cls in ["SIP",'STA']:
                anquan_count["SIP"]+=all_classes[cls]
            elif cls in ["EDR",'EMM']:
                anquan_count["EDR"]+=all_classes[cls]
            elif cls in ["SSL",'VPN','SSL VPN','SSLVPN']:
                anquan_count["SSL"]+=all_classes[cls]
            elif cls in ["AF",'AC&AF','OSM','GAP']:
                anquan_count["AF"]+=all_classes[cls]
            elif cls in ["AC",'AC准入','A','SC',"SG",'BA']:
                anquan_count["AC"]+=all_classes[cls]
            elif cls in Category["安全类"]:
                print(cls,all_classes[cls])
        print("安全类案例数目分别是：")
        print(anquan_count)




solution = Account()
solution.accountKeyWords()