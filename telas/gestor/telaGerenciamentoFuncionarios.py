from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

# Tela do modulo
class telaGerenciamentoFuncionarios(Toplevel):
    def __init__(self, original, modo):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Gerenciamento do Cinema")

        # Titulo
        Label(self, text = "Gerenciamento de Funcionários", font = ("Georgia", 35)).pack(pady = 20)


        # O primeiro rotulo será uma entry caso o modo seja "cadastrar" ou uma combobox 
        # com os funcionarios existentes caso o modo seja "excluir"
        if modo == "cadastrar":
            # Rotulo da entrada
            Label(self, text="Nome:", font=("Georgia", 10)).pack(pady=5)
            self.entry_nome_funcionario = Entry(self, font=("Georgia", 10))
            self.entry_nome_funcionario.pack(pady=5)
        else:
            Label(self, text="Nome:", font=("Georgia", 10)).pack(pady=5)
            self.comboNomes = Combobox(self, width=20, font=("Georgia", 10))
            self.comboNomes['values'] = self.carregar_funcionario()
            self.comboNomes.pack(pady=5)

        # Rotulo para Senha
        Label(self, text="Senha:", font=("Georgia", 10)).pack(pady=5)
        self.entry_senha = Entry(self, font=("Georgia", 10))
        self.entry_senha.pack(pady=5)

        # Rotulo para Cargo
        Label(self, text="Cargo:", font=("Georgia", 10)).pack(pady=5)
        cargos = ["atendente", "gestor"]
        self.comboCargos = Combobox(self, width=20, font=("Georgia", 10))  
        self.comboCargos.pack(pady=5)
        self.comboCargos['values'] = cargos

        # O botao principal é definido com base no parametro "modo"
        if modo == "cadastrar":
            self.btnCad = Button(self, text = 'Cadastrar', font = ("Georgia", 10), width = 25, command = self.cadastrar_funcionario)
            self.btnCad.pack(pady = 10)
        else:
            self.btnCad = Button(self, text = 'Excluir', font = ("Georgia", 10), width = 25, command = self.excluir_funcionario)
            self.btnCad.pack(pady = 10)

        # Botao de sair
        self.btnSair = Button(self, text = 'Sair', font = ("Georgia", 10), width = 25, command = self.deslogar)
        self.btnSair.pack(pady = 10)




    # Metodo que carrega a lista de funcionarios
    # Funciona exatamente como o metodo carregar_filmes 
    def carregar_funcionario(self):
        caminho_arquivo = "infos/funcionarios.txt"
        funcionarios = []
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('gestor:') or linha.startswith('atendente:'):
                    nome_funcionario = linha.split(";")[0].split(": ")[1]
                    if nome_funcionario not in funcionarios:
                        funcionarios.append(nome_funcionario)
                    else:
                        None
        return funcionarios

    # Metodo de cadastro de novos funcionarios
    def cadastrar_funcionario(self):
        # Obtenha o nome, a senha e o cargo do novo funcionário
        nome = self.entry_nome_funcionario.get()
        senha = self.entry_senha.get()
        cargo = self.comboCargos.get()

        # Verifique se o nome, a senha e o cargo foram fornecidos
        if nome and senha and cargo:
            caminho_arquivo = "infos/funcionarios.txt"

            # Abra o arquivo "funcionarios.txt" no modo de escrita (append)
            with open(caminho_arquivo, 'a') as arquivo:
                # Escreva o novo funcionário no arquivo no formato apropriado
                arquivo.write(f"{cargo}: {nome}; senha_{cargo}: {senha}\n")
            

            # Limpe as entradas após cadastrar o funcionário
            self.entry_nome_funcionario.delete(0, END)
            self.entry_senha.delete(0, END)
            self.comboCargos.set("")  # Limpe a seleção da combobox
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")

    # Metodo de exclusão de funcionários existentes
    def excluir_funcionario(self):
        # Obtenha o nome e o cargo do funcionário que você deseja excluir
        nome = self.comboNomes.get()
        cargo = self.comboCargos.get()
        senha = self.entry_senha.get()

        if nome and cargo and senha:
            caminho_arquivo = "infos/funcionarios.txt"

            # Abra o arquivo "funcionarios.txt" no modo de leitura e leitura
            with open(caminho_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()

            # Crie uma nova lista de linhas sem a linha correspondente ao funcionário a ser excluído
            novas_linhas = []
            excluido = False
            for linha in linhas:
                if f'{cargo}: {nome}; senha_{cargo}: {senha}' in linha:
                    excluido = True
                else:
                    novas_linhas.append(linha)

            # Se o funcionário foi excluído, escreva as novas linhas no arquivo
            if excluido:
                with open(caminho_arquivo, 'w') as arquivo:
                    arquivo.writelines(novas_linhas)
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso")
            else:
                messagebox.showerror("Erro", "Senha ou Cargo incorretos")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")

        
    # Voltar para a tela de login
    def deslogar(self):
        self.destroy()
        self.original_frame.mostrar()  
