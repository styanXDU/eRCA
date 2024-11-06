input_file_name = "Bert_keywords/processed_text_contain_keywords.txt"
train_file_name = "Bert_keywords/train.txt"
test_file_name = "Bert_keywords/test.txt"
train_file = open(train_file_name, "w", encoding="utf-8")
test_file = open(test_file_name, "w", encoding="utf-8")

rate = 0.75
all_count = {
    "内容安全类": 1584,
    "新IT类": 1282,
    "边界安全类": 708,
    "访问安全类": 659,
    "云计算类": 307,
    "其他": 582,
}
count = {
    "内容安全类": 0,
    "新IT类": 0,
    "边界安全类": 0,
    "访问安全类": 0,
    "云计算类": 0,
    "其他": 0,
}

with open(input_file_name, encoding="utf-8") as input_file:
    lines = input_file.readlines()
    for row in lines:
        cls,text = row.split(" ")[0]," ".join(row.split(" ")[1:])
        count[cls]+=1
        if cls=="内容安全类":
            new_cls = 0
        elif cls=="新IT类":
            new_cls = 1
        elif cls=="边界安全类":
            new_cls = 2
        elif cls=="访问安全类":
            new_cls = 3
        elif cls=="云计算类":
            new_cls = 4
        elif cls=="其他":
            new_cls = 5
        if count[cls]>all_count[cls]*rate:
            test_file.write(text.rstrip("\n")+"\t"+str(new_cls)+"\n")
        else:
            train_file.write(text.rstrip("\n")+"\t"+str(new_cls)+"\n")



train_file.close()
test_file.close()
