if __name__ == '__main__':
    f = open('../../data/knowledge_triple.txt', 'r', encoding='utf-8')
    #f = open('../../data/test.txt', 'r', encoding='utf-8')
    f_result = open('../../data/space_process.txt', 'a', encoding='utf-8')
    f_result.seek(0)
    f_result.truncate()
    get = f.read()
    f.close()
    txtline = get.split('\n')
    for i in range(len(txtline)):
        txt = []
        txt = txtline[i].split(';')
        process = False
        if len(txt[0])<2 or len(txt[1])<2 or len(txt[2])<2:
            continue
        if txt[4] == 'null':
            if '基地' in txt[2] or '地区' in txt[2]:
                txt[4] = txt[2]
                process = True
            if process == False:
                f_nation = open('../../data/nation.txt', 'r', encoding='utf-8')
                nat = f_nation.read()
                f_nation.close()
                nation = nat.split('\n')
                for j in range(len(nation)):
                    if nation[j] in txt[2]:
                        txt[4] = nation[j]
                        break
                    elif nation[j] in txt[5]:
                        txt[4] = nation[j]
                        break
        if txt[4] == '':
            txt[4] = 'null'
        for i in range(0, 5):
            f_result.write(str(txt[i]))
            f_result.write(";")
        f_result.write(str(txt[5]))
        f_result.write('\n')
    f_result.close()



