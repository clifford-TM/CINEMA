import sys
import os

"""Essas linhas são necessárias no código para dar um append do diretório de venda.py
ao nosso arquivo, já que a importação from convencional não consegue localizar pastas em
níveis superiores."""

# Obtendo o diretório atual e o adicionando ao caminho de pesquisa do python
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_venda = os.path.join(diretorio_atual, "CINEMA/infos/")
sys.path.append(diretorio_venda)

# Importações
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from infos import venda
from infos.carregar_salas_e_horarios import carregar_salas_e_horarios
from infos.carregar_filmes import filmes
from telaGerenciamentoSalaHora import telaGerenciamentoSalaHora
from telaGerenciamentoSalaHora import TelaExclusaoSalaHora


# Tela do modulo
class telaGerenciamentoFilmes(Toplevel):
    def __init__(self, original, modo):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Gerenciamento do Cinema - Cadastro de Filmes")
        self.filmes = filmes

        # Titulo
        Label(self, text="Gerenciamento de Filmes", font=("Georgia", 35)).pack(pady=5)


        # O primeiro rotulo será uma entry caso o modo seja "cadastrar" ou uma combobox 
        # com os filmes existentes caso o modo seja "excluir"
        if modo == "cadastrar":
            # Rótulo para cadastro de filme
            Label(self, text="Nome do Filme:", font=("Arial", 15)).pack(pady=5)
            self.entry_nome_filme = Entry(self, font=("Arial", 10))
            self.entry_nome_filme.pack(pady=5)
        else:
            # Rótulo para exlusão de filme
            Label(self, text="Filme:", font=("Arial", 15)).pack(pady=5)
            self.combobox_filme = Combobox(self, font=("Arial", 10))
            self.combobox_filme['values'] = self.filmes
            self.combobox_filme.pack(pady=5)
            

        # Rótulo para a seleção do horário
        Label(self, text="Horário:", font=("Arial", 15)).pack(pady = 5)
        self.combobox_horario = Combobox(self, font=("Arial", 10))
        self.combobox_horario.pack(pady=5)

        # Rótulo para a seleção da sala
        Label(self, text="Sala:", font=("Arial", 15)).pack(pady=5)
        self.combobox_sala = Combobox(self, font=("Arial", 10))
        self.combobox_sala.pack(pady=5)

        # O metodo carregar_salas_e_horarios atribui as variaveis retornadas aos values das comboboxes
        self.combobox_sala["values"], self.combobox_horario["values"] = carregar_salas_e_horarios()


        # O botao principal será definido com base no parametro "modo" da classe
        # seus nomes e funções serão diferentes em outro modo
        if modo == "cadastrar":
            # Botão para cadastrar o filme
            self.btnCadFilm = Button(self, text='Cadastrar Filme', font = ("Georgia", 10), width=30, command=self.cadastrar_filme)
            self.btnCadFilm.pack(pady=10)
        else:
            # Botão para excluir o filme
            self.btnExcluir = Button(self, text='Excluir Filme', font = ("Georgia", 10), width=30, command=self.excluir_filme)
            self.btnExcluir.pack(pady=10)

        
        if modo == "cadastrar":
            self.btnCadSH = Button(self, text='Cadastrar Sala/Horário', font = ("Georgia", 10), width=30, command=self.cad_sala_e_horario)
            self.btnCadSH.pack(pady=10)
        else:
            self.btnCadSH = Button(self, text='Excluir Sala/Horário', font = ("Georgia", 10), width=30, command=self.exc_sala_e_horario)
            self.btnCadSH.pack(pady=10)


        # Botão para sair
        self.btnSair = Button(self, text='Sair', font = ("Georgia", 10), width=30, command=self.deslogar)
        self.btnSair.pack(pady=10)


        
    # Esse metodo vai para a tela de cadastro de Salas e Horários
    def cad_sala_e_horario(self):
        telaGerenciamentoSalaHora(self)

    # Esse metodo vai para a tela de exclusão de Salas e Horários
    def exc_sala_e_horario(self):
        TelaExclusaoSalaHora(self)

    
    # Esse metodo adiciona as informações do filme na lista filmes.txt 
    # e cria a matriz de bilheteria na pasta Poltronas
    def cadastrar_filme(self):
        # Obtendo informações do Filme
        nome_filme = self.entry_nome_filme.get()
        sala_selecionada = self.combobox_sala.get()
        horario_selecionado = self.combobox_horario.get()

        # Verifique se o nome do filme não está em branco
        if nome_filme.strip() and sala_selecionada and horario_selecionado:
            caminho_arquivo = "infos/Filmes/filmes.txt"

            # Verifique se o filme já está cadastrado com a mesma sala e horário
            with open(caminho_arquivo, 'r') as arquivo:
                filmes = arquivo.readlines()
                for filme in filmes:
                    if f"Sala: {sala_selecionada}" in filme and f"Horario: {horario_selecionado}" in filme:
                        # Se a sessão já está cadastrada, mostre uma mensagem de erro
                        messagebox.showerror("Erro", "A sessão já está cadastrada.")
                        return


            # Abra o arquivo em modo de escrita e adicione o nome do filme, sala e horário
            with open(caminho_arquivo, 'a') as arquivo:
                arquivo.write(f"\nFilme: {nome_filme}; Sala: {sala_selecionada}; Horario: {horario_selecionado}")
                
                # Cria uma matriz 5x10 e coloca na pasta Poltronas
                destino = "infos/Filmes/Poltronas/"
                # O nome do arquivo deve ser tratado retirando ":" pois o formato txt nao aceita esse caractere
                nome_arquivo = f"Filme- {nome_filme}; Sala- {sala_selecionada}; Horario- {horario_selecionado}".replace(":", "-") + ".txt"
                
                # Caminho é uma referência para o metodo criar_matriz
                caminho = os.path.join(destino, nome_arquivo)
                venda.criar_matriz(caminho)

                # Append temporário na lista de Filmes carregada
                # Ao fechar e abrir o programa ele carregará o Filme cadastrado em filmes.txt
                self.filmes.append(nome_filme)

            # Exiba uma mensagem informando que o filme foi cadastrado
            messagebox.showinfo("Sucesso", "Filme cadastrado com Sucesso")
            # Limpe as entradas para cadastrar um novo filme
            self.entry_nome_filme.delete(0, END)
            self.combobox_sala.set("")
            self.combobox_horario.set("")
        else:
            # Exiba uma mensagem de erro se algum dos campos estiver em branco
            messagebox.showerror("Erro", "Preencha todos os campos.")
    
    # Esse metodo exclui as informações do filme na lista filmes.txt 
    # e exclui a matriz de bilheteria na pasta Poltronas
    def excluir_filme(self):
        # Obtendo informações do Filme a ser excluído
        nome_filme = self.combobox_filme.get()
        sala_selecionada = self.combobox_sala.get()
        horario_selecionado = self.combobox_horario.get()

        # Verificando se todos os campos foram preenchidos
        if nome_filme.strip() and sala_selecionada and horario_selecionado:
            caminho_arquivo = "infos/Filmes/filmes.txt"

            # Abra o arquivo em modo de leitura e leia todas as linhas
            with open(caminho_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()

            # Criando uma nova lista de linhas sem as linhas correspondentes ao filme a ser excluído
            novo_conteudo = []
            excluido = False
            for linha in linhas:
                if f"Filme: {nome_filme}" in linha and f"Sala: {sala_selecionada}" in linha and f"Horario: {horario_selecionado}" in linha:
                    # Caso o filme da linha seja o excluído ele não retornará a lista
                    excluido = True
                else:
                    # Se o filme da linha não for o excluído ele retorna para a lista
                    novo_conteudo.append(linha)

            # Com o filme excluído, escreva o novo conteúdo no arquivo
            if excluido:
                with open(caminho_arquivo, 'w') as arquivo:
                    arquivo.writelines(novo_conteudo)

                    # Removendo o filme cadastrado da lista self.filmes
                    # Ao reiniciar o programa o filme não será carregado por não estar em filmes.txt
                    self.filmes.remove(nome_filme)

                # Excluindo o arquivo da matriz de poltronas
                nome_arquivo = f"Filme- {nome_filme}; Sala- {sala_selecionada}; Horario- {horario_selecionado}".replace(":", "-") + ".txt"
                caminho_arquivo_poltronas = os.path.join("infos/Filmes/Poltronas", nome_arquivo)
                if os.path.exists(caminho_arquivo_poltronas):
                    os.remove(caminho_arquivo_poltronas)
                
                # Exiba uma mensagem informando que o filme foi excluído
                messagebox.showinfo("Sucesso", "Filme excluído com Sucesso")
            else:
                # Exiba uma mensagem de erro se o filme não foi encontrado
                messagebox.showerror("Erro", "O filme não foi encontrado.")
        else:
            # Exiba uma mensagem de erro se algum dos campos estiver em branco
            messagebox.showerror("Erro", "Preencha todos os campos.")

        # Limpe os campos após a execução
        self.combobox_filme.set("")
        self.combobox_sala.set("")
        self.combobox_horario.set("")

    # Metodo deslogar
    def deslogar(self):
        self.destroy()
        self.original_frame.mostrar()
