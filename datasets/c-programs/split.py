
f = open("data.txt", "r")

content = f.read()

content_splitted = content.split("#include")

include = ""
count = 0
for i in content_splitted:
    tmp = i.split('\n')
    if (len(tmp) == 2):
        include += "#include " + tmp[0] + '\n'
        continue
    else:
        print(include + '\n' + "#include " + tmp[0])
        i = i.split('\n', maxsplit=1)[1] if len(i.split('\n', maxsplit=1)) == 2 else ""
        include = ""
    data = open(f"data{count}.c", "w")
    data.write(i)
    data.close()
    count += 1
