# Main file for project
import file_read
import decomp
import analysis
import to_file

from libs import trees
from libs import directo
from libs import graph
from libs import evaluate


def main():
    # string = "((abc)|(dξc))*|ani"
    # string = trees.pre(string)
    # tree  = trees.evaluate(string)
    # trees.print2D(tree)
    # dfa = directo.directo(tree, string)
    # #graph.graph(dfa, "prueba")
    # #graph.to_txt(dfa, "prueba")
    # print(evaluate.is_in_language(dfa, "ab"))
    # print("Ingrese archivo ")
    # archivo = input()
    # archivo = open("./inputs/"+archivo)
    archivo = open("./inputs/DoubleAritmetica.ATG")
    data = archivo.read()
    archivo.close()
    name, characters, keywords, tokens, productions = decomp.main(data)
    dfa, dfas, parser = analysis.analyze(name, characters,keywords,tokens,productions)
    to_file.create(dfa, dfas, parser, name)
    


if __name__ == "__main__":
    main()