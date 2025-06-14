from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Criando a instância do Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db" # Configuração do banco de dados SQLite

db = SQLAlchemy(app) # Inicializando a conexão com o banco de dados


# Definindo o modelo de dados para a tabela de tarefas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Definindo o ID como chave primária
    description = db.Column(db.String(100), unique = True, nullable = False) # Definindo a descrição da tarefa como uma string única e não nula


#Definindo a rota raíz, que também está associada ao método GET
@app.route("/")
def index():
    tasks = Task.query.all() # Consultando todas as tarefas do banco de dados
    return render_template("index.html", tasks = tasks)  # Renderizando o template index.html e passando a lista de tarefas para ele


# Método POST para criar uma nova tarefa
@app.route("/add_task", methods = ["POST"])
def add_task():
    new_description = request.form["description"] # Obtém a descrição da tarefa do formulário
    
    # Validar se a tarefa já foi cadastrada
    task_done = Task.query.filter_by(description = new_description).first() # Variável que verfica se a tarefa já existe no banco de dados
    if task_done:
        return "Erro! Essa tarefa já existe", 400 # Se a tarefa já existir, retorna um erro 400
    
    new_task = Task(description = new_description) # Cria uma nova instância de Task com a descrição fornecida
    db.session.add(new_task) # Adiciona as alterações no banco de dados
    db.session.commit() # Efetua as alterações
    return redirect("/") # Redireciona o usuário para a página inicial


# Método POST(Envia as informações via formulário) para remover uma tarefa
@app.route("/delete_task/<int:task_id>", methods = ["POST"])
def delete_task(task_id): 
    task = Task.query.get(task_id) # Obtém a tarefa com o ID fornecido
    if task:
        db.session.delete(task)
        db.session.commit()
    else:
        return "Tarefa não encontrada", 404
    return redirect("/")    


# Método POST(Envia as informações via formulário) para atualizar uma tarefa
@app.route("/update_task/<int:task_id>", methods = ["POST"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        new_description = request.form["description"] # Obtém a nova descrição da tarefa do formulário
        task.description = new_description # Atualiza a descrição da tarefa
        db.session.commit()
        return redirect("/")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000) # Executa o servidor Flask em modo de depuração
