from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse
from models.ordem import OrdemModel, OrdemModelSchema
from datetime import datetime
from resources.rabbitmq import emit_user_profile_update

ordem_schema = OrdemModelSchema
ordem_schema = OrdemModelSchema(many=False)
message_help = "This field cannot be blank."

class Ordem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tipo_transacao', type=str, required=True, help=message_help)
    parser.add_argument('valor_ordem', type=float, required=True, help=message_help)
    parser.add_argument('qtd_ordem', type=int, required=True, help=message_help)
    parser.add_argument('id_wallet', type=int, required=True, help=message_help)

    def post(self):
        try:
            data = Ordem.parser.parse_args()
            preco_medio = data['valor_ordem'] / data['qtd_ordem']
            nome_ativo = "Vibranium"
            status_ordem = "PENDENTE"
            ordem = OrdemModel(data['tipo_transacao'], nome_ativo, data['valor_ordem'],
                               data['qtd_ordem'], preco_medio, str(datetime.now()),
                               status_ordem, data['id_wallet'])
            ordem.save_to_db()
            response = jsonify(message='Order added successfully.', id=ordem.id)
            response.status_code = 201

            #Envio para o RabbitMQ
            message = ordem_schema.dumps(ordem)
            emit_user_profile_update(message);
        except Exception as e:
            print(e)
            response = jsonify('Failed to add Order.!!!')
            response.status_code = 400
        finally:
            return(response)

class OrdemList(Resource):
    def get(self):
        try:
            ordens = OrdemModel.find_all()
            response = jsonify(message='Consulta Realizada com sucesso.')
            response.status_code = 200
            response = ordens
        except Exception as e:
            print(e)
            response = jsonify(message='Problema na consulta.')
            response.status_code = 400
        finally:
            return(response)
        
class OrdemById(Resource):
    def get(self, id):
        try:
            ordem = OrdemModel.find_by_id(id)
            response = jsonify(message='Consulta Realizada com sucesso.')
            response.status_code = 200
            response = ordem
        except Exception as e:
            print(e)
            response = jsonify(message='Problema na consulta.')
            response.status_code = 400
        finally:
            return(response)               