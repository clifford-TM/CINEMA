# Leia instruções.txt antes de usar o programa
# Importações
import sys
from tkinter import *
from tkinter import messagebox
from telas.gestor.telaGestor import telaGestor
from telas.atendente.atendente_tela import telaAtendente

# Classe funcionários
class funcionarios:
    def __init__(self):
        # Carrega os dados de funcionários no construtor
        self.dados_funcionarios = self.carregar_dados()

    # Este metodo verifica o banco de dados e formata as informações para o código
    def carregar_dados(self):
        self.dados = {}
        caminho_arquivo = "infos/funcionarios.txt"
        with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        for linha in linhas:
            partes = linha.strip().split("; ")
            cargo = partes[0].split(": ")[0]
            nome = partes[0].split(": ")[1]
            senha = partes[1].split(": ")[1]

            self.dados[nome] = {"cargo": cargo, "senha": senha}
        return self.dados

    # Este metodo verifica o cargo para direcionar o usuário para a tela o qual é responsável.
    def login(self, usuario, senha):
        if usuario in self.dados_funcionarios:
            if senha == self.dados_funcionarios[usuario]["senha"]:
                return self.dados_funcionarios[usuario]["cargo"]
        return ""


# Tela incial do Programa (Construção)
class telaLogin:
    def __init__(self, parent):
        # self.root agora atribuído a classe agora recebe a classe Tk() para chamar funções 
        # como withdraw, update ou destroy e manipular o Frame principal
        self.root = parent
        
        # Instância da classe funcionarios dentro da classe TelaLogin
        # Com ela é possível chamar todos os metodos da classe
        self.funcionarios_instancia = funcionarios()  

        # Frame de Tk() da inicio a nossa primeira tela
        self.frame = Frame(parent)
        self.frame.pack()

        # Labels sao objetos usados para colocar texto na tela
        Label(self.frame, text="Login", font=("Georgia", 35)).pack(pady=50)

        # Rotulo do Usuário
        Label(self.frame, text="Usuário:", font=("Georgia", 20)).pack()
        self.txtUsuario = Entry(self.frame, width=50) # Entrys sao objetos usados para capturar o texto/entrada do usuário
        self.txtUsuario.pack()

        # Rotulo da Senha
        Label(self.frame, text="Senha:", font=("Georgia", 20)).pack()
        self.txtSenha = Entry(self.frame, width=50)
        self.txtSenha.pack()
        
        # Buttons sao objetos para capturarem eventos de clique do usuário

        # o botão de login chamará a função clicklogin
        self.btnLogin = Button(self.frame, text="Login", font=("Georgia", 10), command=self.clickLogin).pack(pady=20)
        
        # o botao de sair chamará a função sair
        self.btnSair = Button(self.frame, text="Sair", font=("Georgia", 10), command= self.sair).pack(pady=10)

    def clickLogin(self):
        # usuario e senha são obtidos das entrys txtUsuario e txtSenha
        usuario = self.txtUsuario.get()
        senha = self.txtSenha.get()

        # Utilizando a instancia dentro da classe é possível obter o resultado do login
        resultadoLogin = self.funcionarios_instancia.login(usuario, senha)

        if resultadoLogin == '':
            # Caso o resultado nao encontre o cargo do usuário ele deve retornar um erro
            messagebox.showinfo("Erro", "Usuário ou Senha Inválidos")
            self.txtSenha.delete(0, END)
            self.txtUsuario.delete(0, END)
            
        elif resultadoLogin == 'gestor':
            # Caso o resultado do login seja gestor, ele irá para a tela do Gestor
            self.esconder()
            telaGestor(self)

        elif resultadoLogin == 'atendente':
            # Caso o resultado do login seja atendente, ele irá para a tela do Atendente.
            self.esconder()
            telaAtendente(self)

    def esconder(self):
        self.root.withdraw() # Esconder o frame original para avançar nos modulos

    def mostrar(self):
        # o metodo mostrar nao é usado nesse modulo, somente quando a função sair for usada em
        # outros modulos
        self.root.update()
        self.root.deiconify()

    def sair(self):
        self.root.destroy() # o comando destroy encerra o programa

if __name__ == "__main__":
    # A Classe Tk() será reponsável por ser nosso frame principal dono de 
    # todos os metodos de manipulação de tela incluindo fechar e abrir novas telas
    root = Tk()
    root.title("Cinema")
    root.geometry("720x512")
    # Passando root (Tk) como parametro parent para telaLogin
    telaLogin(root)
    root.mainloop()
