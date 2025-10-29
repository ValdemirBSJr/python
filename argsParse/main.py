import argparse

def mostrarKwargs(**kwargs):
    print(f'Meu nome é {kwargs["nome"]}. tenho {kwargs["idade"]} e estou vendo esta mensagem com os valores passados como: {kwargs["metodo"]}.')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='teste com argParse')
    parser.add_argument('--nome', default='Usuário(a)', type=str)
    parser.add_argument('--idade', required=True, type=int)
    parser.add_argument('--metodo', required=True, type=str)

    argumentos = vars(parser.parse_args())

    mostrarKwargs(**argumentos)


