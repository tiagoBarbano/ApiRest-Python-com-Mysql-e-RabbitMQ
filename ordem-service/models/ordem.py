import marshmallow
from db import db
from flask import jsonify

class OrdemModelSchema(marshmallow.Schema):
    class Meta:
        fields = ('id','tipo_transacao','nome_ativo','valor_ordem','qtd_ordem',
                  'preco_medio', 'data_ordem', 'status_ordem', 'id_wallet')

ordem_schema = OrdemModelSchema
ordem_schema = OrdemModelSchema(many=True)

class OrdemModel(db.Model):
    __tablename__ = 'ordem'

    id = db.Column(db.Integer, primary_key=True)
    tipo_transacao = db.Column(db.String(15))
    nome_ativo = db.Column(db.String(15))
    valor_ordem = db.Column(db.Float(precision=2))
    qtd_ordem = db.Column(db.Integer)
    preco_medio = db.Column(db.Float(precision=2))
    data_ordem = db.Column(db.DateTime)
    status_ordem = db.Column(db.String(15))
    id_wallet = db.Column(db.Integer)

    def __init__(self, tipo_transacao, nome_ativo, valor_ordem, qtd_ordem, preco_medio, data_ordem, status_ordem, id_wallet):
        self.nome_ativo = nome_ativo
        self.tipo_transacao = tipo_transacao
        self.valor_ordem = valor_ordem
        self.qtd_ordem = qtd_ordem
        self.preco_medio = preco_medio
        self.data_ordem = data_ordem
        self.status_ordem = status_ordem
        self.id_wallet = id_wallet

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_idwallet(cls, idwallet):
        ordens = db.session.query(OrdemModel).filter_by(id_wallet=idwallet)
        print(ordens)
        result = ordem_schema.dump(ordens)
        print(result)
        return jsonify(result)    

    @classmethod
    def find_by_id(cls, _id):
        ordens = db.session.query(OrdemModel).filter_by(id=_id)
        print(ordens)
        result = ordem_schema.dump(ordens)
        print(result)
        return jsonify(result)

    @classmethod
    def find_all(cls):
        ordens = db.session.query(OrdemModel).all()
        print(ordens)
        result = ordem_schema.dump(ordens)
        print(result)
        return jsonify(result)