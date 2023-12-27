fhandle = open("in.bib", "r")
all_lines = fhandle.readlines()
dictionary_list = []
for line in all_lines:
    line = line.strip()
    if line.startswith("@article"):
        dictionary = {}
        index1 = line.index("{")
        index2 = line.index(",")
        uniquekey = line[index1 +1: index2] 
    elif '"'  in line or "{" in line:
        if '{' in line:
                index1 = line.index("=")
                index2 = line.index("{")
                index3 = line.index("}")
        elif '"' in line:
                index1 = line.index("=")
                index2 = line.index('"')
                index3 = line.rindex('"')
        if line.startswith("author"):
            names_list = []
            name_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            splitted_names = context.split(" and ")
            for i in splitted_names:
                i = i.strip()
                last_splitted = i.split(",")
                last_splitted[0] = last_splitted[0].strip()
                last_splitted[1] = last_splitted[1].strip()
                name = last_splitted[1]
                surname = last_splitted[0]
                temp_name_list = []
                temp_name_list.append(name)
                temp_name_list.append(surname)
                names_list.append(temp_name_list)
            dictionary[name_field] = names_list    
        elif line.startswith("title"):
            title_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            dictionary[title_field] = context
        elif line.startswith("year"):
            year_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            dictionary[year_field] = context
        elif line.startswith("volume"):
            volume_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            dictionary[volume_field] = context
        elif line.startswith("number"):
            number_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            dictionary[number_field] = context
        elif line.startswith("doi"):
            doi_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            dictionary[doi_field] = context
        elif line.startswith("journal"):
            journal_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            dictionary[journal_field] = context
        elif line.startswith("pages"):
            pages_field = line[:index1].strip()
            context = line[index2 + 1: index3]
            start,end = context.split("--")
            pages_str = ""
            pages_str += "pp. "
            pages_str += start
            pages_str += "-"
            pages_str += end
            dictionary[pages_field] = pages_str

    elif line == "}":
        dictionary_list.append(dictionary)
fhandle.close()


#YAZDIRMA BÖLÜMÜ
my_tup = tuple()
tup_list = []
for i in dictionary_list:
    my_tup = tuple()
    my_tup = (-1 * int(i["year"]), i["title"], dictionary_list.index(i))
    tup_list.append(my_tup)
   
tup_list.sort()


                
index_list = []
for i in tup_list:
    a = i[2]
    index_list.append(a)

    

name_part =[]
for i in index_list:
    temp_str = ""
    j = dictionary_list[i]
    for k in range(len(j["author"])):
        if k == len(j["author"]) - 2:
            temp_str += j["author"][k][0]
            temp_str += " "
            temp_str += j["author"][k][1]
            temp_str += " and "
        else:
            temp_str += j["author"][k][0]
            temp_str += " "
            temp_str += j["author"][k][1] 
            temp_str += ", "  
    name_part.append(temp_str)        



fhandle2 = open("out.html", "w")
fhandle2.write("<html>\n")
a = len(index_list)
b = 0
temp_list = []

for i in index_list:
    current_dict = dictionary_list[i]
    if current_dict["year"] not in temp_list:
        fhandle2.write(f'<br> <center> <b> {current_dict["year"]} </b> </center>\n')   
        temp_list.append(current_dict["year"])
    fhandle2.write("<br>\n")   
    fhandle2.write(f'[J{a}] {name_part[b]}<b>{current_dict["title"]}</b>, <i>{current_dict["journal"]}</i>, ')     
    if "number" in current_dict.keys():
        fhandle2.write(f'{current_dict["volume"]}:{current_dict["number"]}, ')
    else:
        fhandle2.write(f'{current_dict["volume"]}, ')
    if "pages" in current_dict.keys():
        fhandle2.write(f'{current_dict["pages"]}, ')
    fhandle2.write(f'{current_dict["year"]}. ')
    if "doi" in current_dict.keys():
        fhandle2.write(f'<a href="https://doi.org/{current_dict["doi"]}">link</a> ')
    fhandle2.write("<br>\n")  
    b += +1
    a += -1

fhandle2.write("</html>")   
fhandle2.close()

#ERROR HANDLING BOLUMU
article_unique_namelist = []
fhandle = open("in.bib", "r")
all_lines = fhandle.readlines()

for line in all_lines:
    line = line.strip()
    if line.startswith("@article"):
        line = line[:-1]
        line_split = line.split("{")
        unique_name = line_split[1]
        article_unique_namelist.append(unique_name)
for i in range(len(article_unique_namelist)):
    for j in range(i+1, len(article_unique_namelist)):
        if article_unique_namelist[i] == article_unique_namelist[j]:
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()

for i in article_unique_namelist:
    for j in i:
        x = j.isalnum()
        if x == True:
            continue
        elif x == False:
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()

for dic in dictionary_list:
    for j in dic.keys():
        x = j.islower()
        if x == True:
            continue
        elif x == False:
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()

for dic in dictionary_list:
    for j in dic.values():
        if j == "":
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()

for dic in dictionary_list:
    for j in dic:
        x = int(dic["year"])
        if x < 1000:
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()
        elif x > 2022:
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()   

for dic in dictionary_list:
    for j in dic:
        x = int(dic["volume"])
        if x <= 0:
            fhandle2 = open("out.html", "w")
            fhandle2.write("Input file in.bib is not a valid .bib file!")
            fhandle2.close()

for dic in dictionary_list:
    if "number" not in dic.keys():
        continue
    else:
        for j in dic["number"]:
            if int(j) <= 0:
                fhandle2 = open("out.html", "w")
                fhandle2.write("Input file in.bib is not a valid .bib file!")
                fhandle2.close()

for dic in dictionary_list:
    if "pages" not in dic.keys():
        continue
    else:
        for j in dic["pages"]:
            x = dic["pages"][4:]
            splitted_pages = x.split("-")
            number1 = int(splitted_pages[0])
            number2 = int(splitted_pages[1])
            if number1 <= 0 :
                fhandle2 = open("out.html", "w")
                fhandle2.write("Input file in.bib is not a valid .bib file!")
                fhandle2.close()
            if number2 <= 0 or number2 <= number1:
                fhandle2 = open("out.html", "w")
                fhandle2.write("Input file in.bib is not a valid .bib file!")
                fhandle2.close()

