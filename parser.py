# File for productions only

OPS  = ["[", "{", "|", "("]
ENDING = ["]", "}", "|", ")"]
OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']

def parser(productions, parse_line, tokens, keywords):
    print("analizando producciones")
    file = open("./outputs/parser.py", 'w+'
    )
    string = "class Parser:\n"

    string += "\tdef __init__(self, tokens):\n"
    string += "\t\tself.tokens = tokens\n"
    string += "\t\tself.id_token = 0\n"
    string += "\t\tself.actual_token = self.tokens[self.id_token]\n"
    string += "\t\tself.last_token = ''\n"
    string += "\t\t#self.advance()\n\n"

    string += "\tdef advance( self ):\n"
    string += "\t\tself.id_token += 1\n"
    string += "\t\tif self.id_token < len(self.tokens):\n"
    string += "\t\t\tself.actual_token = self.tokens[self.id_token]\n"
    string += "\t\t\tself.last_token = self.tokens[self.id_token - 1]\n\n"

    string += "\tdef expect(self, item, arg = None):\n"
    string += "\t\tog = self.id_token\n"
    string += "\t\tpossible = False\n"
    string += "\t\tif item != None:\n"
    string += "\t\t\ttry:\n"
    string += "\t\t\t\tif arg == None:\n"
    string += "\t\t\t\t\tans = item()\n"
    string += "\t\t\t\telse:\n"
    string += "\t\t\t\t\tans = item(arg)\n"
    string += "\t\t\t\tif type(ans) == bool:\n"
    string += "\t\t\t\t\tpossible = ans\n"
    string += "\t\t\t\telse:\n"
    string += "\t\t\t\t\tpossible = True\n"
    string += "\t\t\texcept:\n"
    string += "\t\t\t\tpossible = False\n"
    string += "\t\tself.id_token = og\n"
    string += "\t\tself.actual_token = self.tokens[self.id_token]\n"
    string += "\t\tself.last_token = self.tokens[self.id_token - 1]\n"
    string += "\t\treturn possible\n\n"

    string += "\tdef read(self, item, type = False):\n"
    string += "\t\tif type:\n"
    string += "\t\t\tif self.actual_token.type == item:\n"
    string += "\t\t\t\tself.advance()\n"
    string += "\t\t\t\treturn True\n"
    string += "\t\t\telse:\n"
    string += "\t\t\t\treturn False\n"
    string += "\t\t\t\t#print('expected ', item, ' got ', self.actual_token.type)\n"
    string += "\t\telse:\n"
    string += "\t\t\tif self.actual_token.value == item:\n"
    string += "\t\t\t\tself.advance()\n"
    string += "\t\t\t\treturn True\n"
    string += "\t\t\telse:\n"
    string += "\t\t\t\treturn False\n"
    string += "\t\t\t\t#print('expected ', item, ' got ', self.actual_token.value)\n"

    string += "\tvalue, result, value1, value2 = 0,0,0,0\n"
    
    new_tokens = []
    for p in productions:
        string = first(p, string)
        string, news = second(productions[p], string, parse_line, tokens, keywords)
        string += "\n"
        for token in news:
            if token not in new_tokens:
                new_tokens.append(token)

    #print(string)
    file.write(string)
    file.close()
    #print(parse_line)
    new_parse = parse_line[:-1]
    for token in new_tokens:
        if token in OPERATORS:
            #print(ord(token))
            new_parse += "|" + str(ord(token))
        else:
            new_parse += "|" + token
    new_parse = new_parse + ")"
    #print(new_parse)
    fixed_parser = fix_expect(string)
    print(new_parse)
    return fixed_parser, new_parse

def fix_expect(parser):
    parser = parser.split("\n")
    new_parser = ""
    for line in parser:
        if "self.expect(" in line and "while" not in line:
            original = line
            new_line = line.split("(",1)
            new_parser += new_line[0] + "("
            args = new_line[1].split("(", 1)
            second = args[1].replace(")", "")
            second = second.replace(":", "")
            new_parser += args[0] + "," + second + "):\n"
        elif "self.expect(" in line and "while" in line:
            or_parted = line.split("or")
            for part in or_parted:
                new_line = part.split("(",1)
                new_parser += new_line[0] + "("
                args = new_line[1].split("(", 1)
                second = args[1].replace(")", "")
                new_parser += args[0] + "," + second[:-1] + ") or"
            new_parser = new_parser[:-2] +  ":\n"
            #new_parser += line + "\n"
        else:
            new_parser += line + "\n"
    #print(new_parser)
    return new_parser



def first(name, string):
    name = name.replace("\n", "")
    name = name.replace("\t", "")
    name = name.replace(" ", "")
    funciton_name = name.split("<")[0]
    string += "\tdef " + funciton_name + "(self"
    if "<" in name:
        function_params = name.split("<")[1]
        #print("params ", function_params[:-1])
        string +="," + function_params[:-1]
    string += "):\n"
    return string

def second(body, string, parse_line, tokens, key_words):
    new_tokens = []
    actual = 0
    temp = ""
    extras = "\t\t"
    conditional = False
    inside_if = False
    while actual < len(body):
        if body[actual] == "{":
            extra = actual + 1
            counter = 0
            while body[extra] not in OPS and counter != 2:
                if body[extra] == " ":
                    pass
                elif body[extra] == '"':
                    counter += 1
                    temp += body[extra]
                else:
                    temp += body[extra]
                extra += 1
            if "<" in temp:
                    if conditional:
                        temp = "self.expect('" + temp + "'):"
                        conditional = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    temp = "self."+ name + "(" + arg + ")"
            elif '"' in temp:
                temp = "self.read(" + temp +")"
            else:
                temp = "self."+ temp + "()"
            string += extras + "while self.expect(" + temp +"):\n"
            temp = ""
            extras += "\t"
        elif body[actual] == "}":
            extras = extras.replace("\t", "", 1)
            if inside_if:
                extras = extras.replace("\t", "", 1)


        elif body[actual] == "(" and body[actual+1] == ".":
            actual += 2
            while body[actual] != "." or body[actual + 1] != ")":
                # if body[actual] == " ":
                #     pass
                # else:
                temp += body[actual]
                actual += 1
            actual += 1
            string += extras + temp + "\n"
            temp = ""


        elif body[actual] == '"':
            actual += 1
            while body[actual] != '"':
                temp += body[actual]
                actual += 1
            if conditional:
                string += "self.expect(self.read('" + temp + "')):\n"
                conditional = False
            string += extras + 'self.read("' + temp + '")\n'
            new_tokens.append(temp)
            #print(new_tokens)
            temp = ""


        elif body[actual] == "(":
            pass

        elif body[actual] == ")":
            if inside_if:
                extras = extras.replace("\t", "", 1)


        elif body[actual] == "[":
            string += extras + "if "
            conditional = True
            extras += "\t"
        elif body[actual] == "]":
            extras = extras.replace("\t", "", 1)
            if inside_if:
                extras = extras.replace("\t", "", 1)


        elif body[actual] == "|":
            extra = actual -1
            # search for previous symbol
            while extra > 0:
                if body[extra] == " " or body[extra] == "\n":
                    pass
                elif body[extra] =="." and body[extra - 1] == "(":
                    extra -= 1 
                elif body[extra] in OPS:
                    break
                extra -= 1
            # what to do with each previous case
            if body[extra] == "{":
                part = string.rfind("while")
                while string[part] != ":":
                    part += 1
                counter = 0
                cond = ""
                i = actual + 1
                while body[i] not in OPS and counter != 2:
                    if body[i] == " ":
                        pass
                    elif body[i] == '"':
                        counter += 1
                        temp += body[i]
                    else:
                        temp += body[i]
                    i += 1
                if "<" in temp:
                        if conditional:
                            string += "self.expect('" + temp + "'):"
                            conditional = False
                        name = temp.split("<", 1)[0]
                        arg = temp.split("<", 1)[1][:-1]
                        temp = "self."+ name + "(" + arg + ")"
                elif '"' in temp:
                    temp = "self.read(" + temp +")"
                else:
                    temp = "self."+ temp + "()"
                first_if = string[part+2:].split("\n")[0]
                string_parted = string[part+1:]
                string = string[:part] + " or self.expect("+ temp + ")" + ":\n"
                first_if = first_if.replace("\t", "")
                string += extras + "if self.expect(" + first_if + "):"
                lines = string_parted.split("\n")
                for line in lines:
                    string += "\t" + line + "\n"
            elif body[extra] == "(":
                i = extra + 1
                counter = 0
                while body[i] not in OPS and counter != 2:
                    if body[i] == " ":
                        pass
                    elif body[i] == '"':
                        counter += 1
                        temp += body[i]
                    else:
                        temp += body[i]
                    i += 1
                if "<" in temp:
                        if conditional:
                            string += "self.expect('" + temp + "'):"
                            conditional = False
                        name = temp.split("<", 1)[0]
                        arg = temp.split("<", 1)[1][:-1]
                        temp = arg + "=self."+ name + "(" + arg + ")"
                elif '"' in temp:
                    temp = "self.read(" + temp +")"
                else:
                    temp = "self."+ temp + "()"
                previous = string.rfind(temp)
                string_parted = string[previous:]
                print(string_parted)
                print(string[:previous])
                print(temp)
                if "=" in temp:
                    expect_arg = temp.split("=")[1]
                else:
                    expect_arg = temp
                string = string[:previous] + "if self.expect(" + expect_arg +"):\n"
                print(string)
                lines = string_parted.split("\n")
                for line in lines:
                    string += extras + "\t"+ line + "\n"
                temp == ""
                print(string)
            elif body[extra] == "|":
                pass
            # Siguiente parte del or
            temp = ""
            inside_if = True
            i = actual + 1
            counter = 0 
            in_comillas = False
            while (body[i] not in OPS or not in_comillas) and counter != 2:
                if body[i] == ")" and not in_comillas:
                    break
                if body[i] == " ":
                    pass
                elif body[i] == '"':
                    counter += 1
                    temp += body[i]
                else:
                    temp += body[i]
                i += 1
            if "<" in temp:
                    if conditional:
                        string += "self.expect('" + temp + "'):"
                        conditional = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    temp = "self."+ name + "(" + arg + ")"
            elif '"' in temp:
                temp = "self.read(" + temp +")"
            else:
                temp = "self."+ temp + "()"
            string += extras + "elif self.expect(" + temp + "):\n"
            extras += "\t"
            temp = ""


        elif body[actual] == " " or body[actual] == "\n" or body[actual] == "\t":
            if temp != "":
                if temp in tokens or temp in key_words:
                    string += extras + "self.read('" + temp + "', True)\n"
                elif "<" in temp:
                    if conditional:
                        string += "self.expect('" + temp + "'):\n"
                        conditional = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    string += extras + arg.replace(" ", "") + "=self."+ name + "(" + arg + ")\n"
                else:
                    if conditional:
                        string += "self.expect('" + temp + "'):\n"
                        conditional = False
                    string += extras + "self."+ temp + "()\n"
                temp = ""
            else:
                pass


        else:
            temp += body[actual]
        actual += 1
    return string, new_tokens