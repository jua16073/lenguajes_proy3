# Nuevo comienzo

def decomp(file):
    actual = 0
    read_lines = {}
    temp = ""
    name = ""
    while actual < len(file):
        temp += file[actual]
        #print("start",temp, "end")
        if temp == "COMPILER":
            print("leyendo Compiler")
            temp = ""
            actual += 1
            while actual < len(file):
                if file[actual] == "" or file[actual]== " ":
                    pass
                elif (file[actual] == " " or file[actual] == "\n") and name != "":
                    break
                else:
                    name += file[actual]
                actual += 1
            print("name = " , name)
            print(actual)
        if temp == "CHARACTERS":
            print("leyendo Characters")
            analyze_single("characters", )
            pass
        if temp == "KEYWORDS":
            print("leyendo Keywords")
            pass
        if temp == "TOKENS":
            print("leyendo Tokens")
            pass
        if temp == "PRODUCTIONS":
            print("leyendo Productions")
            pass
        if temp == "END":
            print("leyendo End")
            pass
        if temp == " " or temp == "\n":
            temp = ""
        if temp == "(.":
            while file[actual] != ")" or file[actual-1] != ".":
                actual += 1
            temp = ""
        actual += 1
    print(temp)

def analyze_single(name, file, actual, read_lines):
    actual += 1
    temp = ""
    while actual < len(file):
        print(file[actual])

