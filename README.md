# 📚 Grades Based

Sistema desktop de gerenciamento de notas escolares, feito em **Python** com **CustomTkinter** e **MongoDB**. Professores podem lançar notas de seus alunos por atividade, e alunos podem visualizar todas as suas notas em um painel próprio.

---

## ✨ Funcionalidades

- 🔐 **Login e Registro** de usuários, com senha protegida via hash (`bcrypt`)
- 🧑‍🏫 **Perfil de Professor**
  - Busca de alunos em tempo real (autocomplete) enquanto digita o nome
  - Lançamento de notas por atividade, vinculadas à matéria do professor
  - Validação de nota (0 a 10)
- 🧑‍🎓 **Perfil de Aluno**
  - Painel com todas as notas recebidas, organizadas por matéria e atividade
- 🚪 Logout disponível em ambos os painéis
- 🗄️ Persistência de dados em **MongoDB**

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| [Python 3](https://www.python.org/) | Linguagem principal |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interface gráfica (GUI) |
| [PyMongo](https://pymongo.readthedocs.io/) | Conexão com MongoDB |
| [bcrypt](https://pypi.org/project/bcrypt/) | Hash de senhas |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Variáveis de ambiente |
| [MongoDB](https://www.mongodb.com/) | Banco de dados |

---

## 🎥 Prévia

![Demonstração do sistema](./videoPreviaSysPaInel.gif)

> O GIF acima mostra o fluxo completo: registro, login, lançamento de nota pelo professor e visualização pelo aluno.

---

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Uma instância do MongoDB (local ou [MongoDB Atlas](https://www.mongodb.com/atlas))

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/DaviSO7/sys-painel-aluno_professor.git
cd sys-painel-aluno_professor
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com a sua string de conexão do MongoDB:

```env
MONGO_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/
```

> ⚠️ **Nunca** suba o arquivo `.env` para o GitHub. Ele já está incluído no `.gitignore` deste projeto.

### 5. Execute o sistema

```bash
python app.py
```

---

## 🗂️ Estrutura do banco de dados

O projeto usa o banco `registroDeUsuarios`, com duas coleções:

**`users`**
```json
{
  "nome": "string",
  "email": "string",
  "senha_hash": "bytes (bcrypt)",
  "tipo": "professor | aluno",
  "materia": "string (apenas se professor)",
  "conta_criada_em": "datetime"
}
```

**`grades`**
```json
{
  "nome_aluno": "string",
  "nota": "float",
  "atividade": "string",
  "materia": "string"
}
```

---

## 📁 Estrutura do projeto

```
grades-based/
├── app.py            # Código principal da aplicação
├── .env                # Variáveis de ambiente (não versionado)
├── requirements.txt    # Dependências do projeto
├── videoPreviaSysPaInel.gif  #GIF de demonstração
├── README.md
```

---

## 🧭 Roadmap / Possíveis melhorias

- [ ] Edição e exclusão de notas já lançadas
- [ ] Validação de formato de e-mail no registro
- [ ] Tela de "esqueci minha senha"
- [ ] Exportação de notas em PDF/Excel
- [ ] Suporte a múltiplas turmas por professor

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

Feito por [Davi Rocha](https://github.com/DaviSO7)
