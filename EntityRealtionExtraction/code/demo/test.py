import json

json_file = '../../data/knowledge_triple_biaozhu.json'
output_file = '../../data/knowledge_triple_biaozhu_zhedie.json'
fo = open(output_file,'a',encoding='utf-8')
with open(json_file,'r',encoding='gbk') as f:
    lists=f.readlines()
    # lists=json.loads(data)
    for line in lists:
        fo.write(json.dumps(line, ensure_ascii=False) + '\n')



