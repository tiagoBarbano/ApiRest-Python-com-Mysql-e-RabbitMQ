from flask import Flask
from flask_restful import Api
from resources.ordem import Ordem, OrdemById, OrdemList, OrdemByWallet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost:3306/teste'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

api.add_resource(Ordem, '/ordem',  endpoint='ordem') #cria ordem
api.add_resource(OrdemList, '/ordem',  endpoint='ordens') # busca todas as ordens
api.add_resource(OrdemById, '/ordem/<int:id>', endpoint='ordembyid') # busca ordem por ID
api.add_resource(OrdemByWallet, '/ordem/wallet/<int:id>', endpoint='ordembywallet') # busca ordem por wallet

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)