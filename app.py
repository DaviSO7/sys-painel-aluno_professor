# Sistema que envia nota para os alunos ou que permite os alunos verem suas notas
# Passo a Passo
    # Passo 1: Criar um sistema de login e registro
        # Login: Se o usuario ja estiver registrado
        # Registro: Nome, email, senha, e se é estudante ou professor
        # E para professor obter qual matéria ele da aula
    # Passo 2: Depois de Logar - Opções para estudante/professor
        # Estudante: Menu de abrir para ver as notas de cada matéria
        # Professor: Menu mais complexo que tenha um campo que coloque o nome completo do aluno como identificação, para passar as notas, tenha também um campo para notas e do lado qual foi a atividade, e o ultimo campo de qual materia é as notas com um botao de enviar
        # Para ambos: Um menu na parte superior direita/esquerda que tenha uma opção de deslogar da conta


from pymongo import MongoClient
from datetime import datetime, timezone
import bcrypt
import os
from dotenv import load_dotenv
from tkinter import messagebox, Listbox

load_dotenv()
url = os.getenv("MONGO_URL")
con = MongoClient(url)
db = con.get_database("registroDeUsuarios")
collection = db.get_collection("users")
gradesCollection = db.get_collection("grades")

# Passo 1: Criar um sistema de login e registro
    # Login: Se o usuario ja estiver registrado
    # Registro: Nome, email, senha, e se é estudante ou professor
    # E para professor obter qual matéria ele da aula

import customtkinter as ctk

# Configs da Janela de Login
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Grades Based - Login")
app.geometry("900x600")

# Janela de registro
def abaRegistrar():
    # Configs da Janela de Registro
    janelaRegistro = ctk.CTkToplevel(app)
    janelaRegistro.title("Grades Based - Registro")
    janelaRegistro.geometry("900x600")

    # Textos e Inputs Janela de Registro
    tituloRegistro = ctk.CTkLabel(janelaRegistro, text="Registro", font=("", 30))
    tituloRegistro.pack(pady=50)
    camponomeRegistro = ctk.CTkEntry(janelaRegistro, placeholder_text="Insira seu nome completo", width=250, justify="center")
    camponomeRegistro.pack(pady=30)
    campoEmailRegistro = ctk.CTkEntry(janelaRegistro, placeholder_text="Insira seu email", width=250, justify="center")
    campoEmailRegistro.pack()
    campoSenhaRegistro = ctk.CTkEntry(janelaRegistro, placeholder_text="Insira sua senha", width=250, justify="center")
    campoSenhaRegistro.pack(pady=30)
    perguntaTipoRegistro = ctk.CTkLabel(janelaRegistro, text="Você é professor?", font=("", 15))
    perguntaTipoRegistro.pack(pady=5)
    tipos = ["Sim (Sou Professor)", "Não (Sou Aluno)"]
    campoTipoRegistro = ctk.CTkOptionMenu(janelaRegistro, values=tipos)
    campoTipoRegistro.pack(pady=10)
    perguntaMateriaRegistro = ctk.CTkLabel(janelaRegistro, text="Qual Matéria você dá aula?")
    materias = ["Matemática", "Português", "História", "Geografia", "Física", "Química", "Biologia", "Inglês", "Espanhol", "Educação Física"]
    campoMateriasRegistro = ctk.CTkOptionMenu(janelaRegistro, values=materias)
    botaoRegistrar = ctk.CTkButton(janelaRegistro, text="Registrar", cursor="hand2", command=lambda: registrar())
    botaoRegistrar.pack(pady=10)


    def verificarTipo(opcao):
        if opcao == "Sim (Sou Professor)":
            perguntaMateriaRegistro.pack(pady=5)
            campoMateriasRegistro.pack(pady=15)
        else:
            perguntaMateriaRegistro.pack_forget()
            campoMateriasRegistro.pack_forget()

        botaoRegistrar.pack_forget()
        botaoRegistrar.pack(pady=10)
    
    campoTipoRegistro.set("Não (Sou Aluno)")
    campoTipoRegistro.configure(command=verificarTipo)
    

    # Passar info pro db
    def registrar():
        # Criando as variaveis para usar no banco de dados
        nome = camponomeRegistro.get()
        email = campoEmailRegistro.get()
        senha = campoSenhaRegistro.get()
        tipo = campoTipoRegistro.get()
        materia = campoMateriasRegistro.get()

        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

        user = {
            "nome":nome,
            "email": email,
            "senha_hash":senha_hash,
            "tipo":"professor" if "Professor" in tipo else "aluno",
            "conta_criada_em": datetime.now(timezone.utc)
        }
        if "Professor" in tipo:
            user["materia"] = materia
        
        if collection.find_one({"email": email}):
            messagebox.showerror("Erro", "Email já cadastrado! Insira outro!")
        else:
            collection.insert_one(user)
            messagebox.showinfo("Sucesso", "Conta registrada com Sucesso!")



# Janela de Login - Textos e Inputs
tituloLogin = ctk.CTkLabel(app, text="Login", font=("", 30))
tituloLogin.pack(pady=80)
campoEmailLogin = ctk.CTkEntry(app, placeholder_text="Insira seu email", width=250, justify="center")
campoEmailLogin.pack(pady=30)
campoSenhaLogin = ctk.CTkEntry(app, placeholder_text="Insira sua senha", width=250, justify="center", show="*")
campoSenhaLogin.pack()
botaoLogin = ctk.CTkButton(app, text="Login", cursor="hand2", command=lambda: logar())
botaoLogin.pack(pady=20)
registrarLogin = ctk.CTkButton(app, text="Ainda não tem uma conta? Registre-se!", fg_color="transparent", text_color="blue", hover=False, cursor="hand2", command=abaRegistrar)
registrarLogin.pack()

# Voltar info do db pro login
def logar():
    emailLogar = campoEmailLogin.get()
    senhaLogar = campoSenhaLogin.get()

    userLogar = collection.find_one({"email": emailLogar})

    if not userLogar:
        messagebox.showerror("Erro", "Email não encontrado!")
        return
    
    # Passo 2: Depois de Logar - Opções para estudante/professor
    # Estudante: Menu de abrir para ver as notas de cada matéria
    # Professor: Menu mais complexo que tenha um campo que coloque o nome completo do aluno como identificação, para passar as notas, tenha também um campo para notas e do lado qual foi a atividade, e o ultimo campo de qual materia é as notas com um botao de enviar
    # Para ambos: Um menu na parte superior direita/esquerda que tenha uma opção de deslogar da conta

    if bcrypt.checkpw(senhaLogar.encode("utf-8"), userLogar["senha_hash"]):
        if userLogar["tipo"] == "professor":
            messagebox.showinfo("Sucesso", "Prossiga para o painel!")
            app.withdraw()
            painelDoProfessor = ctk.CTkToplevel(app)
            painelDoProfessor.title("Grades Based - Painel do Professor")
            painelDoProfessor.geometry("900x600")
            nomeProfessorPainel = ctk.CTkLabel(painelDoProfessor, text=f"Professor(a): {userLogar['nome']}", fg_color="slateblue1", width=150, corner_radius=15)
            nomeProfessorPainel.place(relx=.02, rely=.02, anchor="nw")
            botaoDeslogarProfessor = ctk.CTkButton(painelDoProfessor, text="Deslogar", fg_color="red", cursor="hand2", command=lambda: deslogar(painelDoProfessor), hover_color="red3")
            botaoDeslogarProfessor.place(relx=.98, rely=.02, anchor="ne")

            def buscarAlunos(event):
                nomeDigitado = campoEscolherAluno.get()

                if nomeDigitado == "":
                    listaAlunos.delete(0, "end")
                    listaAlunos.place_forget()
                    return

                listaAlunos.place(rely=.60, anchor="center", relx=.50)
                listaAlunos.delete(0, "end")

                resultados = collection.find({
                    "tipo": "aluno",
                    "nome": {"$regex": f"^{nomeDigitado}", "$options": "i"}
                }).limit(5)
                for aluno in resultados:
                    listaAlunos.insert("end", aluno["nome"])

            def selecionarAluno(event):
                alunoSelecionado = listaAlunos.get(listaAlunos.curselection())
                campoEscolherAluno.delete(0, "end")
                campoEscolherAluno.insert(0, alunoSelecionado)
                listaAlunos.delete(0, "end")

                if not listaAlunos.curselection():
                    return

            campoEscolherAluno = ctk.CTkEntry(painelDoProfessor, placeholder_text="Digite o nome do aluno", width=300, justify="center", font=("", 20))
            campoEscolherAluno.place(rely=.40, anchor="center", relx=.50)
            campoEscolherAluno.bind("<KeyRelease>", buscarAlunos)
            listaAlunos = Listbox(painelDoProfessor, height=5, font=("", 14), bg="#242424", fg="white", selectbackground="blue", selectforeground="white", bd=0, highlightthickness=0, justify="center")
            listaAlunos.place(rely=.60, anchor="center", relx=.50)
            listaAlunos.bind("<<ListboxSelect>>", selecionarAluno)
            campoNotas = ctk.CTkEntry(painelDoProfessor, placeholder_text="Insira a nota do Aluno", justify="center")
            campoNotas.place(anchor="center", rely=.70, relx=.35)
            campoAtividade = ctk.CTkEntry(painelDoProfessor, placeholder_text="Insira sobre a atividade realizada", justify="center", width=300)
            campoAtividade.place(anchor="center", rely=.70, relx=.61)
            botaoEnviarNota = ctk.CTkButton(painelDoProfessor, text="Enviar Nota", command=lambda:enviarNota())
            botaoEnviarNota.place(anchor="center", rely=.80, relx=.50)

            def enviarNota():
                nota = float(campoNotas.get())
                if nota < 0 or nota > 10:
                    messagebox.showerror("Erro", "Nota Inválida!")
                elif nota >= 0 or nota <= 10:
                    messagebox.showinfo("Sucesso", "Nota enviada com êxito!")
                    # Enviar nota pro banco de dados
                    alunoEnviado = campoEscolherAluno.get()
                    notaEnviada = float(campoNotas.get())
                    AtividadeEnviada = campoAtividade.get()
                    grades = {
                        "nome_aluno":alunoEnviado,
                        "nota":notaEnviada,
                        "atividade":AtividadeEnviada,
                        "materia": userLogar["materia"]
                    }
                    gradesCollection.insert_one(grades)

        else:
            messagebox.showinfo("Sucesso", "Prossiga para o painel!")
            app.withdraw()
            painelDoAluno = ctk.CTkToplevel(app)
            painelDoAluno.title("Grades Based - Painel do Aluno")
            painelDoAluno.geometry("900x600")
            nomeAlunoPainel = ctk.CTkLabel(painelDoAluno, text=f"Aluno(a): {userLogar['nome']}", fg_color="slateblue1", width=150, corner_radius=15)
            nomeAlunoPainel.place(relx=.02, rely=.02, anchor="nw")
            botaoDeslogarAluno = ctk.CTkButton(painelDoAluno, text="Deslogar", fg_color="red", cursor="hand2", command=lambda: deslogar(painelDoAluno), hover_color="red3")
            botaoDeslogarAluno.place(relx=.98, rely=.02, anchor="ne")

            tituloPainelAluno = ctk.CTkLabel(painelDoAluno, text="Minhas Notas", font=("", 20))
            tituloPainelAluno.place(anchor="center", relx=.50, rely=.20)
            mostrarNotasAluno = ctk.CTkScrollableFrame(painelDoAluno, width=700, height=400)
            mostrarNotasAluno.place(anchor="center", rely=.60, relx=.50)
            # Pegar notas no banco de dados
            notaDoAluno = gradesCollection.find({"nome_aluno":userLogar["nome"]})
            for i, nota in enumerate(notaDoAluno):
                texto = f"{nota['materia']} | Atividade: {nota['atividade']} | Nota: {nota['nota']}"
                label = ctk.CTkLabel(mostrarNotasAluno, text=texto)
                label.pack(pady=5, padx=10, anchor="center")
    else:
        messagebox.showerror("Erro", "Senha incorreta!")

# Função de Deslog
def deslogar(janelaPainel):
    janelaPainel.destroy()
    app.deiconify()

# Rodar o app
app.mainloop()