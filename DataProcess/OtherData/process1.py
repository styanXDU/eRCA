import csv
import re

inputfile = open("input1.txt", "r", encoding="utf-8")
csvfile = open("case1.csv", "w", newline="")
writer = csv.writer(csvfile)
#先写入columns_name
writer.writerow(["案例描述","故障现象","故障判定","原因分析","解决方法"])

input_lines = inputfile.readlines()
output_line = [""]*5
for line in input_lines:
    if line:
        if re.match("^[0-9]+\\.", line):
            print(line)
            writer.writerow(output_line)
            output_line = [""] * 5
            output_line[0] = line.split(".")[1].strip("\n")
        if line.startswith("故障"):
            if line.startswith("故障判定："):
                output_line[2] = line.split("故障判定：")[1].strip("。\n")
            if line.startswith("故障判断："):
                output_line[2] = line.split("故障判断：")[1].strip("。\n")
        if line.startswith("原"):
            if line.startswith("原因分析："):
                output_line[3] = line.split("原因分析：")[1].strip("\n")
            elif line.startswith("原 因分析："):
                output_line[3] = line.split("原 因分析：")[1].strip("\n")
            elif line.startswith("原因分析与解决："):
                output_line[3] = line.split("原因分析与解决：")[1].strip("\n")
        if line.startswith("解决："):
            output_line[4] = line.split("解决：")[1].strip("\n")
writer.writerow(output_line)  #写上最后一行
inputfile.close()
csvfile.close()





