from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import functools

app = Flask(__name__)
api = Api(app)

Tarefas = {
    'tarefa1': {'tarefa': 'Testar o sistema', 'ativo' : '1' },

}


def tarefa_nao_existe(tarefa_id):
    if tarefa_id not in Tarefas:
        if("tarefa"+tarefa_id in Tarefas):
            return "tarefa"+tarefa_id 
        abort(404, message="Tarefa {} não existe".format(tarefa_id))

parser = reqparse.RequestParser()
parser.add_argument('tarefa')


class Tarefa(Resource):
    def get(self, tarefa_id):
        tarefa_id=tarefa_nao_existe(tarefa_id)
        if(Tarefas[tarefa_id]["ativo"]=="1"):
            return {"tarefa":Tarefas[tarefa_id]["tarefa"]}
        else:
            abort(404, message="{} está inativa".format(tarefa_id))

    def delete(self, tarefa_id):
        tarefa_id=tarefa_nao_existe(tarefa_id)
        Tarefas[tarefa_id]={"tarefa":Tarefas[tarefa_id]["tarefa"],"ativo":'0'}
        return '', 204

    def put(self, tarefa_id):
        tarefa_id=tarefa_nao_existe(tarefa_id)
        args = parser.parse_args()
        tarefa = {'tarefa': args['tarefa'], 'ativo': '1'}
        Tarefas[tarefa_id] = tarefa
        return tarefa, 201



class ListaTarefas(Resource):
    def get(self):
        Tarefas_ativas=[Tarefas[tarefa_ativa] for tarefa_ativa in Tarefas if Tarefas[tarefa_ativa]["ativo"]!="0"]
        return Tarefas_ativas

    def post(self):
        args = parser.parse_args()
        tarefa_id = int(max(Tarefas.keys()).lstrip('tarefa')) + 1
        tarefa_id = 'tarefa%i' % tarefa_id
        Tarefas[tarefa_id] = {'tarefa': args['tarefa'], 'ativo': "1"}
        return Tarefas[tarefa_id], 201
class HealthCheck(Resource):
    def get(self):
        return 200

api.add_resource(ListaTarefas, '/Tarefa')
api.add_resource(Tarefa, '/Tarefa/<tarefa_id>')
api.add_resource(HealthCheck, '/healthcheck')


if __name__ == '__main__':
    app.run(debug=True)