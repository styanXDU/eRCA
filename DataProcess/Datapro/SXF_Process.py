import csv
from lxml import etree
import re
import urllib
from HTML2Text import filterHtmlTag
import codecs


input_file_name = "深信服社区.csv"
added_header = ['故障标题', '关键字', '故障-问题描述', '故障-告警信息', '故障-处理过程','故障-有效排查步骤', '故障-根因', '故障-解决方案',\
                '故障-建议与总结', '文档编号', '作者', '更新时间', '适用版本']
csvfile = open("SXF_processed_cases.csv", "w", encoding="utf-8", newline="")
writer = csv.writer(csvfile)
# 先写入columns_name
writer.writerow(added_header)

with open(input_file_name,encoding="utf-8") as input_file:
    # line = input_file.readlines()
    csv_reader = csv.reader(input_file)  # 使用csv.reader读取input_file中的文件
    header = next(csv_reader)        # 读取第一行每一列的标题
    # header = line[0]
    # for row in line[1:]:
    for row in csv_reader:            # 将csv 文件中的数据保存到data中
        #row[1]里边存放的是关键字，需要将关键字和|进行保留
        row[1] = re.sub("[^a-zA-Z0-9\u4e00-\u9fa5]&^\\|", '', row[1]).replace(" ","")
        row[1] = row[1].replace("\n","")
        dom = etree.HTML(row[2])
        xpath_items = '//div[@class="t-content-box"]/div[@class="t-content"]'
        items = dom.xpath(xpath_items)
        case = [''] * 7
        for item in items:
            title = item.xpath('./h2/text()')[0].strip()
            contents = item.xpath('./div')[0]
            words = etree.tostring(contents, encoding='utf-8', pretty_print=True, method='html').decode('utf-8')
            word = filterHtmlTag(words)
            if title=="问题描述":
                case[0] =word
            elif title=="告警信息":
                case[1] = word
            elif title=="处理过程":
                case[2] = word
            elif title=="有效排查步骤":
                case[3] = word
            elif title=="根因":
                case[4] =word
            elif title=="解决方案":
                case[5] =word
            elif title=="建议与总结":
                case[6] =word
        new_row = row[:2]+case+row[3:]
        writer.writerow(new_row)

csvfile.close()