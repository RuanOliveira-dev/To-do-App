from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Criando a instância do Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db" # Configuração do banco de dados SQLite

db = SQLAlchemy(app) # Inicializando a conexão com o banco de dados


# Definindo o modelo de dados para a tabela de tarefas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Definindo o ID como chave primária
    description = db.Column(db.String(100), unique = True, nullable = False) # Definindo o título da tarefa como string não nula


#Definindo a rota raíz, que já está associada ao método GET
@app.route("/")
def index():
    tasks = Task.query.all() # Consultando todas as tarefas do banco de dados
    return render_template("index.html", tasks= tasks)  # Rota padrão que retorna uma mensagem simples

# Método POST para criar uma nova tarefa
@app.route("/add_task", methods=["POST"])
def add_task():
    description = request.form["description"] # Obtém a descrição da tarefa do formulário
    # Validar se a tarefa já foi realizada
    task_done = Task.query.filter_by(description=description).first() # Variável que recebe a tarefa feita, e verifica se essa tarefa é igual a que eu inseri
    if task_done:
        return "Erro! Essa tarefa já existe"
    new_task = Task(description=description) # Cria uma nova instância de Task com a descrição fornecida
    db.session.add(new_task) # Adiciona as alterações no banco de dados
    db.session.commit() # Efetua as alterações
    return redirect("/") # Redireciona o usuário para a página inicial


if __name__ == "__main__":
    app.run(debug=True, port=5000) # Executa o servidor Flask em modo de depuração