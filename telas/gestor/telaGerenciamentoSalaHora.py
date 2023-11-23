# Importações
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from infos.carregar_salas_e_horarios import carregar_salas_e_horarios
import os

# Tela do modulo
class telaGerenciamentoSalaHora(Toplevel):
    # Construindo a tela
    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Gerenciamento do Cinema")

        # Titulo
        Label(self, text="Cadastro de Salas/Horários", font=("Georgia", 30)).grid(row=0, column=0, padx=100, columnspan=3, pady=5)

        # Rotulo de seleção da sala
        Label(self, text="Selecione a Sala (Opcional):", font=("Georgia", 15)).grid(row=1, column=0, columnspan=3, pady=5)
        self.combobox_sala = Combobox(self, font=("Georgia", 10))
        self.combobox_sala['values'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Adicione as salas disponíveis
        self.combobox_sala.grid(row=2, column=0, columnspan=3, pady=5)

        # Rotulo de seleção de horário
        novo_horario_frame = Frame(self)
        novo_horario_frame.grid(row=3, column=0, columnspan=3, pady=5)
        Label(novo_horario_frame, text="Novo Horário (Opcional): ", font=("Georgia", 15)).grid(row=0, column=0, padx=5)


        # Spinboxes para ajustar horário 
        # São duas: uma para hora e outra para minutos
        self.spin_hora = Spinbox(novo_horario_frame, from_=0, to=23, width=3, format="%02.0f", font=("Georgia", 10))
        self.spin_hora.grid(row=0, column=1)

        Label(novo_horario_frame, text=":", font=("Georgia", 10)).grid(row=0, column=2)
        self.spin_minuto = Spinbox(novo_horario_frame, from_=0, to=59, width=3, format="%02.0f", font=("Georgia", 10))
        self.spin_minuto.grid(row=0, column=3)


        # Botão de cadastro de sala
        btn_cadastrar_sala = Button(self, text="Cadastrar Sala", width=20, font=("Georgia", 10), command=self.cadastrar_sala)
        btn_cadastrar_sala.grid(row=4, column=0, pady=10, padx=50)

        # Botão de cadastro de horário
        btn_cadastrar_horario = Button(self, text="Cadastrar Horário", width=20, font=("Georgia", 10), command=self.cadastrar_horario)
        btn_cadastrar_horario.grid(row=4, column=1, pady=10)


    # Adiciona nova sala
    def cadastrar_sala(self):
        nova_sala = int(self.combobox_sala.get())
        if nova_sala:
            self.adicionar_informacao("salas", nova_sala)

    # Adiciona novo horario
    def cadastrar_horario(self):
        novo_horario = f"{self.spin_hora.get()}:{self.spin_minuto.get()}"
        if novo_horario:
            self.adicionar_informacao("horarios", novo_horario)

    # Adiciona nova informação
    def adicionar_informacao(self, chave, valor):
        # Construa o caminho absoluto para o arquivo
        caminho_arquivo = "infos/Filmes/salas_e_horarios.txt"

        # Abra o arquivo em modo de leitura
        with open(caminho_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()

        # Procure pela linha que começa com a chave e adicione a nova informação
        for i, linha in enumerate(linhas):
            if linha.startswith(f"{chave}:"):
                salas, horarios = carregar_salas_e_horarios()
                
                chaves = {"salas": salas,
                          "horarios": horarios}
                
                valores_existentes = chaves[chave]
                
                if valor in valores_existentes:
                    messagebox.showerror("Erro", f"{chave[:-1]} já existente")
                    return
                linhas[i] = f"{linha.strip()}, {valor}\n"

                messagebox.showinfo("Sucesso", f"{chave[:-1]} cadastrad{chave[1]} com sucesso")
                break
        else:
            # Se a chave não foi encontrada, adicione uma nova linha com a informação
            linhas.append(f"{chave}: {valor}\n")

        # Escreva novamente o arquivo com as modificações
        with open(caminho_arquivo, "w") as arquivo:
            arquivo.writelines(linhas)

# Tela do modulo
class TelaExclusaoSalaHora(Toplevel):
    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Exclusão de Salas/Horários")

        # Titulo
        Label(self, text="Exclusão de Salas/Horários", font=("Georgia", 30)).grid(row=0, column=0, padx=100, columnspan=3, pady=5)

        salas, horarios = carregar_salas_e_horarios()

        # Combobox para seleção da sala a ser excluída
        Label(self, text="Selecione a Sala:", font=("Georgia", 15)).grid(row=1, column=0, columnspan=3, pady=5)
        self.combobox_sala = Combobox(self, font=("Georgia", 10))
        self.combobox_sala['values'] = salas  # Carregue as salas disponíveis
        self.combobox_sala.grid(row=2, column=0, columnspan=3, pady=5)

        # Combobox para seleção do horário a ser excluído
        Label(self, text="Selecione o Horário:", font=("Georgia", 15)).grid(row=3, column=0, columnspan=3, pady=5)
        self.combobox_horario = Combobox(self, font=("Georgia", 10))
        self.combobox_horario['values'] = horarios  # Carregue os horários disponíveis
        self.combobox_horario.grid(row=4, column=0, columnspan=3, pady=5)

        # Botao para excluir sala
        btn_excluir_sala = Button(self, text="Excluir Sala", width=20, font=("Georgia", 10), command=self.excluir_sala)
        btn_excluir_sala.grid(row=5, column=0, pady=10, padx=50)

        # Botao para excluir horario
        btn_excluir_horario = Button(self, text="Excluir Horário", width=20, font=("Georgia", 10), command=self.excluir_horario)
        btn_excluir_horario.grid(row=5, column=1, pady=10)

    # Exclui uma sala
    def excluir_sala(self):
        sala_selecionada = int(self.combobox_sala.get())
        if sala_selecionada:
            self.excluir_informacao("salas", sala_selecionada)

    # Exclui um horário
    def excluir_horario(self):
        horario_selecionado = self.combobox_horario.get()
        if horario_selecionado:
            self.excluir_informacao("horarios", horario_selecionado)

    # Exclui uma informação
    def excluir_informacao(self, chave, valor):
        caminho_arquivo = "infos/Filmes/salas_e_horarios.txt"

        # Carregue as salas e horários uma vez fora do loop
        salas, horarios = carregar_salas_e_horarios()
        chaves = {"salas": salas, "horarios": horarios}

        with open(caminho_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()

        for i, linha in enumerate(linhas):
            if linha.startswith(f"{chave}:"):
                valores_existentes = chaves[chave]

                if valor not in valores_existentes:
                    messagebox.showerror("Erro", f"{chave} não encontrad{chave[1]}")
                    return

                valores_existentes.remove(valor)
                novos_valores = list(map(str, valores_existentes))
                print(type(novos_valores[0]))
                linhas[i] = f"{chave}: {', '.join(novos_valores)}\n"
                messagebox.showinfo("Sucesso", f"{chave[:-1]} excluíd{chave[1]} com sucesso")
                break
        else:
            messagebox.showerror("Erro", f"Nenhuma {chave} encontrada")

        with open(caminho_arquivo, "w") as arquivo:
            arquivo.writelines(linhas)