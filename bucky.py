#o tktinter vem por padrão na maioria das instalações python
#começamos importando todo o conteúdo da biblioteca

from tkinter import *

#conceitor básicos,
# - container armazena objetos
# - widgets são quaisquer componentes na tela
# - event handler são as rotinas de excução para verificar os eventos
# - event loop verifica constantemente se um evento foi acionado
# o modulo tkinter oferece 3 formas de gerenciamento de geometrias
# - pack, grid e place

#começamos declarando a classe principal da aplicação, que usaremos pra instaciar os widgets dentro da tela

class Aplicacao:
    def __init__(self, master=None):
        self.widget1 = Frame(master) #o frame 'master' é o maior objeto da hierarquia. Janela da aplicação(top-level)
        self.widget1["bg"] = ("purple")
        self.widget1.pack()
        self.message = Label(self.widget1, text="Olá mundo")
        self.message["font"] = ("Verdana", "10", "italic", "bold")
        self.message["bg"] = ("purple")
        self.message.pack()
        self.buttonOut = Button(self.widget1)
        self.buttonOut["command"] = self.changeText
        self.buttonOut["text"] = "sair"
        self.buttonOut["bg"] = ("gray")
        self.buttonOut["width"] = 100
        self.buttonOut.pack(side=RIGHT)

    def changeText(self):
        if self.message["text"] == "Olá mundo":
            self.message["text"] = "Clique"
        else:
            self.message["text"] = "Olá mundo"

root = Tk()
root["bg"] = ("purple")
Aplicacao(root) #aqui, passamos a variável root como parametro da classe construtora "Aplicaçao",
                #com isso, sabemos em que tela podemos imprimir as mensagens na tela
root.mainloop() #usamos o metodo mainloop para exibirmos na tela


#mais observações
# - devemos sempre saber qual o container pai
# - caso o widget não seja atribuido a nenhum gerenciador de geometria, ele não será exibido ao usuário


#algumas configurações de estilo
# - Width é a largura do widget
# - Height é a altura do widget
# - Text é o texto dentro do widget
# - Font é a familia da font do texto exibido
# - Fg é a cor do texto
# - Fb é a cor do widget
# - Side define que lado o widget ficará ( de acordo com o objeto pai ())
# - as configurações de cores são feitas com os mesmos codigos de css
