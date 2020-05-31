# Main file for project
import file_read
import decomp
import analysis

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
    archivo = open("./inputs/Aritmetica.ATG")
    data = archivo.read()
    archivo.close()
    name, characters, keywords, tokens, productions = decomp.main(data)
    analysis.analyze(name, characters,keywords,tokens,productions)


if __name__ == "__main__":
    main()