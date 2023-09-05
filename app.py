# Import Library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

#  Inisialisasi  flask
app = Flask(__name__)
api = Api(app)
CORS(app)

# Inisialisasi DB
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database
db = SQLAlchemy(app)


# DB Model
class ModelPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


with app.app_context():
    db.create_all()

person = {}


class IndexResource(Resource):
    @staticmethod
    def get():
        query = ModelPerson.query.all()
        output = [
            {
                'nama' : data.nama,
                'umur': data.umur,
                'alamat': data.alamat
            }
            for data in query
        ]

        response = {
            'code': 200,
            "msg": "Query Data Sukses",
            "data": output,
        }
        return response, 200

    @staticmethod
    def post():
        nama = request.form["nama"]
        umur = request.form["umur"]
        alamat = request.form["alamat"]

        model = ModelPerson(
            nama=nama,
            umur=umur,
            alamat=alamat
        )
        model.save()

        response = {
            "msg": "Data berhasil tersimpan",
            'code': 200
        }

        return response, 200


# Routing
api.add_resource(IndexResource, '/api', methods=["GET", "POST"])
# api.add_resource(IndexResource, '/api', methods=["POST"])

# Running Program
if __name__ == "__main__":
    app.run(debug=True, port=8000)
