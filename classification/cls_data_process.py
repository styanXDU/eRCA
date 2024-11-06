input_file_name = "Bert_keywords/origin_text.txt"
output_file_name = "Bert_keywords/processed_text_contain_keywords.txt"
output_file = open(output_file_name, "w", encoding="utf-8")

clses = []
count = {}

with open(input_file_name, encoding="utf-8") as input_file:
    lines = input_file.readlines()
    for row in lines:
        cls,text = row.split(" ")[0]," ".join(row.split(" ")[1:])
        new_cls = ""
        if cls=="AC":
            new_cls = "内容安全类"
        elif cls=="AF" or "SIG" in cls:
            new_cls = "边界安全类"
        elif "SSL" in cls or "VPN" in cls:
            new_cls = "访问安全类"
        elif "HCI" in cls or "aDR-H" in cls or "EDS" in cls or "SCP" in cls :
            new_cls = "云计算类"
        elif "SDW-R" in cls or "aBos" in cls or "WOC" in cls or "AD" in cls or "IPSEC" in cls or "aDesk" in cls :
            new_cls = "新IT类"
        else:
            new_cls = "其他"

        if new_cls not in clses:
            clses.append(new_cls)
            count[new_cls] = 1
        else:
            count[new_cls]+=1

        output_file.write(new_cls + " " + text)

output_file.close()
sorted_count=sorted(count.items(),key=lambda x:x[1],reverse=True)
print(sorted_count)