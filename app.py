from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://<admin>:<password>@<database-url>:<0000>/<iii>'
db = SQLAlchemy(app)

#Classe Cadastro de Clientes
class Clientes(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)  
    nome = db.Column(db.String(100))
    cpf_cnpj = db.Column(db.String(14))
    endereco = db.Column(db.String(100))
    cep = db.Column(db.String(9))
    telefone = db.Column(db.String(25))
    email = db.Column(db.String(25))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nome,cpf_cnpj,endereco,cep,telefone,email):
        self.id = 12345
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.endereco = endereco
        self.cep = cep
        self.telefone = telefone
        self.email = email
    def __repr__(self):
        return '' % self.id
#db.create_all()

#Classe Casos com Processo
class CasosCom(db.Model):
    __tablename__ = "casos_com_processo"
    id_caso = db.Column(db.Integer, primary_key=True)  
    autor = db.Column(db.String(200))
    reu = db.Column(db.String(200))
    descricao = db.Column(db.String(1000000))
    prazo = db.Column(db.String(10))
    num_processo = db.Column(db.String(100))     
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,id_caso,autor,reu,descricao,prazo,num_processo,id_cliente):
        self.id_caso = id_caso
        self.autor = autor
        self.reu = reu 
        self.descricao = descricao
        self.prazo = prazo
        self.num_processo = num_processo
        self.id_cliente = id_cliente
    def __repr__(self):
        return '' % self.id_caso
#db.create_all()

#Classe Casos Sem Processo
class CasosSem(db.Model):
    __tablename__ = "casos_sem_processo"
    id_caso_sem = db.Column(db.Integer, primary_key=True)  
    autor = db.Column(db.String(200))
    reu = db.Column(db.String(200))
    descricao = db.Column(db.String(1000000))
    prazo = db.Column(db.String(10))
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,id_caso_sem,autor,reu,descricao,prazo,id_cliente):
        self.id_caso_sem = id_caso_sem
        self.autor = autor
        self.reu = reu 
        self.descricao = descricao
        self.prazo = prazo
        self.id_cliente = id_cliente
    def __repr__(self):
        return '' % self.id_caso_sem
#db.create_all()

#Processos
class Processos(db.Model):
    __tablename__ = "processos"
    id_processos = db.Column(db.Integer, primary_key=True)  
    lista_prazos = db.Column(db.String(10))
    novo_prazo_sem_cliente = db.Column(db.String(10))
    id_caso_processo = db.Column(db.Integer, db.ForeignKey('casos_com_processo.id_caso'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,id_processos,lista_prazos,novo_prazo_sem_cliente,id_caso_processo,id_cliente):
        self.id_processos = id_processos
        self.lista_prazos = lista_prazos
        self.novo_prazo_sem_cliente = novo_prazo_sem_cliente
        self.id_caso_processo = id_caso_processo
        self.id_cliente = id_cliente
    def __repr__(self):
        return '' % self.id_processos
db.create_all()

#Model Cadastro de Clientes
class ClientesModel(ModelSchema):      #schema e meta são HTML?
    class Meta(ModelSchema.Meta):
        model = Clientes
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    nome = fields.String(required=True)
    cpf_cnpj = fields.String(required=True)
    endereco = fields.String(required=True)
    cep = fields.String(required=True)
    telefone = fields.String(required=True)
    email = fields.String(required=True)

#Model Casos com Processo
class CasosComModel(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CasosCom
        sqla_session = db.session
    id_caso = fields.Number(dump_only=True)
    autor = fields.String(required=True)
    reu = fields.String(required=True)
    descricao = fields.String(required=True)
    prazo = fields.String(required=True)
    num_processo = fields.String(required=True)
    id_cliente = fields.Number(required=True)

#Model Casos sem Processo
class CasosSemModel(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CasosSem
        sqla_session = db.session
    id_caso_sem = fields.Number(dump_only=True)
    autor = fields.String(required=True)
    reu = fields.String(required=True)
    descricao = fields.String(required=True)
    prazo = fields.String(required=True)
    id_cliente = fields.Number(required=True)

#Model Processos
class ProcessosModel(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Processos
        sqla_session = db.session
    id_processos = fields.Number(dump_only=True)
    lista_prazos = fields.String(required=True)
    novo_prazo_sem_cliente = fields.String(required=True)
    id_caso = fields.Number(required=True)
    id_cliente = fields.Number(required=True)


#CRUD Clientes
@app.route('/clientes', methods = ['GET'])
def get_clientes():
    get_clientes = Clientes.query.all()
    print(get_clientes)
    clientes_model = ClientesModel(many=True)
    print(clientes_model)
    clientes = clientes_model.dump(get_clientes)
    print(clientes)
    return make_response(jsonify({"clientes": clientes}))

@app.route('/clientes', methods = ['POST'])
def criar_cliente():
    data = request.get_json()
    print(data)
    clientes_model = ClientesModel()
    print(clientes_model)
    clientes = clientes_model.load(data)
    print(clientes)
    result = clientes_model.dump(clientes.create())
    print(result)
    return make_response(jsonify({"clientes": result}),200)

@app.route('/clientes/<id>', methods = ['PUT'])
def atualizar_cliente_por_id(id):
    print(id)
    data = request.get_json()
    print(data)
    get_clientes = Clientes.query.get(id)
    print(get_clientes)
    if data.get('nome'):
        get_clientes.nome = data['nome']
    if data.get('cpf_cnpj'):
        get_clientes.cpf_cnpj = data['cpf_cnpj']
    if data.get('endereco'):
        get_clientes.endereco = data['endereco']
    if data.get('cep'):
        get_clientes.cep = data['cep']
    if data.get('telefone'):
        get_clientes.telefone = data['telefone']
    if data.get('email'):
        get_clientes.email = data['email']
    db.session.add(get_clientes)
    db.session.commit()
    clientes_model = ClientesModel(only=['id', 'nome', 'cpf_cnpj','endereco','cep','telefone','email'])
    cliente = clientes_model.dump(get_clientes)
    return make_response(jsonify({"clientes": data}))

@app.route('/clientes/<id>', methods = ['DELETE'])
def deletar_cliente_por_id(id):
    get_clientes = Clientes.query.get(id)
    db.session.delete(get_clientes)
    db.session.commit()
    return make_response("",204)

#CRUD Casos Com Processo
@app.route('/casos_com_processo', methods = ['GET'])
def get_casos_com():
    get_casos_com = CasosCom.query.all()
    print(get_casos_com)
    casos_com_model = CasosComModel(many=True)
    print(casos_com_model)
    casos_com = casos_com_model.dump(get_casos_com)
    print(casos_com)
    return make_response(jsonify({"casos_com": casos_com}))

@app.route('/casos_com_processo', methods = ['POST'])
def criar_casos_com():
    data = request.get_json()
    print(data)
    casos_com_model = CasosComModel()
    print(casos_com_model)
    casos_com = casos_com_model.load(data)
    print(casos_com)
    result = casos_com_model.dump(casos_com.create())
    print(result)
    return make_response(jsonify({"casos_com": result}),200)

@app.route('/casos_com_processo/<id_caso>', methods = ['PUT'])
def atualizar_casos_com_por_id(id_caso):
    print(id_caso)        #vínculo ao ID primário ou ao id do caso?
    data = request.get_json()
    print(data)
    get_casos_com = CasosComModel.query.get(id_caso)
    print(get_casos_com)
    if data.get('autor'):
        get_casos_com.autor = data['autor']
    if data.get('reu'):
        get_casos_com.reu = data['reu']
    if data.get('descricao'):
        get_casos_com.descricao = data['descricao']
    if data.get('prazo'):
        get_casos_com.prazo = data['prazo']
    if data.get('num_processo'):
        get_casos_com.num_processo = data['num_processo']
    if data.get('id_cliente'):
        get_casos_com.id_cliente = data['id_cliente']    
    db.session.add(get_casos_com)
    db.session.commit()
    casos_com_model = CasosComModel(only=['id_caso', 'autor', 'reu', 'descricao','prazo','num_processo','id_cliente'])
    casos_com = casos_com_model.dump(get_casos_com)
    return make_response(jsonify({"casos_com": data}))

@app.route('/casos_com_processo/<id_caso>', methods = ['DELETE'])
def deletar_casos_com_por_id(id_caso):
    get_casos_com = CasosCom.query.get(id_caso)
    db.session.delete(get_casos_com)
    db.session.commit()
    return make_response("",204)

#CRUD Casos Sem Processo
@app.route('/casos_sem_processo', methods = ['GET'])
def get_casos_sem_processo():
    get_casos_sem = CasosSem.query.all()
    print(get_casos_sem)
    casos_sem_model = CasosSemModel(many=True)
    print(casos_sem_model)
    casos_sem = casos_sem_model.dump(get_casos_sem)
    print(casos_sem)
    return make_response(jsonify({"casos_sem": casos_sem}))

@app.route('/casos_sem_processo', methods = ['POST'])
def criar_casos_sem():
    data = request.get_json()
    print(data)
    casos_sem_model = CasosSemModel()
    print(casos_sem_model)
    casos_sem = casos_sem_model.load(data)
    print(casos_sem)
    result = casos_sem_model.dump(casos_sem.create())
    print(result)
    return make_response(jsonify({"casos_sem": result}),200)

@app.route('/casos_sem_processo/<id_caso_sem>', methods = ['PUT'])
def atualizar_casos_sem_por_id(id_caso_sem):
    print(id_caso_sem)        #vínculo ao ID primário ou ao id do caso?
    data = request.get_json()
    print(data)
    get_casos_sem = CasosSemModel.query.get(id_caso_sem)
    print(get_casos_sem)
    if data.get('autor'):
        get_casos_sem.autor = data['autor']
    if data.get('reu'):
        get_casos_sem.reu = data['reu']
    if data.get('descricao'):
        get_casos_sem.descricao = data['descricao']
    if data.get('prazo'):
        get_casos_sem.prazo = data['prazo']
    if data.get('id_cliente'):
        get_casos_sem.id_cliente = data['id_cliente']    
    db.session.add(get_casos_sem)
    db.session.commit()
    casos_sem_model = CasosSemModel(only=['id_caso', 'autor', 'reu', 'descricao','prazo','num_processo','id_cliente'])
    casos_sem = casos_sem_model.dump(get_casos_sem)
    return make_response(jsonify({"casos_sem": data}))

@app.route('/casos_sem_processo/<id_caso_sem>', methods = ['DELETE'])
def deletar_casos_sem_por_id(id_caso_sem):
    get_casos_sem = CasosSem.query.get(id_caso_sem)
    db.session.delete(get_casos_sem)
    db.session.commit()
    return make_response("",204)

#CRUD Processos
@app.route('/processos', methods = ['GET'])
def get_processos():
    get_processos = Processos.query.all()
    print(get_processos)
    processos_model = ProcessosModel(many=True)
    print(processos_model)
    processos = processos_model.dump(get_processos)
    print(processos)
    return make_response(jsonify({"processos": processos}))

@app.route('/processos', methods = ['POST'])
def criar_processos():
    data = request.get_json()
    print(data)
    processos_model = ProcessosModel()
    print(processos_model)
    processos = processos_model.load(data)
    print(processos)
    result = processos_model.dump(processos.create())
    print(result)
    return make_response(jsonify({"processos": result}),200)

@app.route('/processos/<id_processos>', methods = ['PUT'])
def atualizar_processos_por_id(id_processos):
    print(id_processos)      
    data = request.get_json()
    print(data)
    get_processos = ProcessosModel.query.get(id_processos)
    print(get_processos)
    if data.get('id_processos'):
        get_processos.id_processos = data['id_processos']
    if data.get('lista_prazos'):
        get_processos.lista_prazos = data['lista_prazos']
    if data.get('novo_prazo_sem_cliente'):
        get_processos.novo_prazo_sem_cliente = data['novo_prazo_sem_cliente']
    if data.get('id_caso_processo'):
        get_processos.id_caso_processo = data['id_caso_processo']
    if data.get('id_cliente'):
        get_processos.id_cliente = data['id_cliente']    
    db.session.add(get_processos)
    db.session.commit()
    processos_model = ProcessosModel(only=['id_processos', 'lista_prazos', 'novo_prazo_sem_cliente', 'id_caso_processo', 'id_cliente'])
    processos = processos_model.dump(get_processos)
    return make_response(jsonify({"processos": data}))

@app.route('/processos/<id_processos>', methods = ['DELETE'])
def deletar_processos_por_id(id_processos):
    get_processos = Processos.query.get(id_processos)
    db.session.delete(get_processos)
    db.session.commit()
    return make_response("",204)

if __name__ == "__main__":          #!!!
    app.run(debug=True)


