

COMMENTS = ["/*", "*/", "//"]

def read_word(file, actual):
    temp_word = ""
    while actual < len(file):
        if (file[actual] == " " or file[actual] == "\n") and (len(temp_word) > 0):
            break
        elif file[actual] == " " or file[actual] == "\n":
            actual += 1
        else:
            temp_word += file[actual]
            actual += 1
    return temp_word, actual

def main(file):
    actual = 0
    characters = []
    keywords = []
    tokens = []
    productions = []
    temp_word = ""
    while actual < len(file):
        temp_word, actual = read_word(file, actual)
        print(temp_word)
        if temp_word == "COMPILER":
            name, actual = COMPILER(file, actual)
        if temp_word == "CHARACTERS":
            characters, actual = CHARACTERS(file, actual)
        if temp_word == "KEYWORDS":
            keywords, actual = KEYWORDS(file, actual)
        if temp_word == "TOKENS":
            tokens, actual = TOKENS(file, actual)
        if temp_word == "PRODUCTIONS":
            productions, actual = PRODUCTIONS(file, actual)
        if temp_word == "END":
            final = END(file, actual, name)
            if final:
                break
            else:
                print("No coincide el nombre")
                break
        
    
    return name, characters, keywords, tokens, productions

def COMPILER(file, actual):
    actual += 1 
    name, actual = read_word(file, actual)
    return name, actual

def CHARACTERS(file, actual):
    print("leyendo CHARACTERS")
    actual += 1
    temp = ""
    characters = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "KEYWORDS":
            actual -= 8
            break
        line += temp
        if line[-1] == "." and line[-2] != ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                #print("id: ",temp_id, " values: ", temp_values)
                characters[temp_id] = temp_values
                line =  ""
            else:
                print("no se encuentra el '='")
    return characters, actual

def KEYWORDS(file, actual):
    print("leyendo KEYWORDS")
    actual += 1
    temp = ""
    keywords = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "TOKENS":
            actual -= 6
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                keywords[temp_id] = temp_values
                line =  ""
            else:
                print("no se encuentra el '='")
    return keywords, actual

def TOKENS(file, actual):
    print("leyendo TOKENS")
    actual += 1
    temp = ""
    tokens = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "PRODUCTIONS":
            actual -= 11
            break
        if temp == "END":
            actual -= 3
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                tokens[temp_id] = temp_values
                line =  ""
            else:
                print("no se encuentra el '='")
    return tokens, actual

def PRODUCTIONS(file, actual):
    print("leyendo PRODUCTIONS")
    print(actual)
    actual += 1
    temp = ""
    productions = {}
    temp_id = ""
    temp_values = ""
    line = ""
    flag = False
    while actual < len(file):
        print(temp)
        if flag:
            pass
        if not flag:
            temp += file[actual]
        if not flag and temp[-1] == "." and (file[actual + 1] == " " or file[actual+1] == "\n"):
            print(temp)
            temp_id = temp.split("=", 1)[0]
            temp_values = temp.split("=", 1)[1]
            productions[temp_id] = temp_values
            temp = ""
        if file[actual] == "(" and file[actual + 1] == "." and not flag:
            flag = True
            actual += 1
            temp = temp[:-1]
        if flag and file[actual] == "." and file[actual  + 1] == ")":
            actual += 1
            flag = False
        if temp == "END":
            actual -= 3
            print("salir")
            temp = ""
            break
        actual += 1
    print("producciones")
    print(productions)
    for p in productions:
        print(p, ": ", productions[p])
    return productions, actual

def END(file, actual, name):
    actual += 1
    end_name, actual = read_word(file, actual)
    if end_name == name:
        return True
    return False


if __name__ == "__main__":
    file = open("inputs/file.txt")
    content = file.read()
    main(content)
    file.close()