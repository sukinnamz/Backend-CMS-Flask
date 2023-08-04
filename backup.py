from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Categories(db.Model):
    id_kategori = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100))
    news = db.relationship('News', backref='post')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

class News(db.Model):
    id_news = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT)
    id_kategori = db.Column(db.Integer, db.ForeignKey('categories.id_kategori'))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

class PageCustom(db.Model):
    id_page = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    page_content = db.Column(db.TEXT)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

db.create_all()

class Kategori(Resource):
    def get(self):
        query = Categories.query.all()
        list = [{
            "ID Kategori" : data.id_kategori,
            "Kategori" : data.nama_kategori
        }
        for data in query
        ]
        output = {
            "msg" : "List Kategori :",
            "list" : list
        }
        return output
        
    def post(self):
        input_kategori = request.form["nama_kategori"]
        kat = Categories(nama_kategori = input_kategori)
        kat.save()
        query = Categories.query.all()
        id = []
        for data in query:
            id.append(data.id_news)
        output = id[-1]
        return {"Data tersimpan dengan ID kategori" : output}
    
class SeleksiKategori(Resource):
    def get(self, id):
        query = Categories.query.filter_by(id_kategori=id).first()
        if not query:
            return {"msg" : "Data tidak ditemukan"}
        detail = {
            "ID Kategori" : query.id_kategori,
            "Nama Kategori" : query.nama_kategori
        }
        return detail
    
    def put(self, id):
        query = Categories.query.filter_by(id_kategori=id).first()
        try: 
            editKategori = request.form["nama_kategori"]
            query.nama_kategori = editKategori
            db.session.commit()
            return {"msg" : "Data berhasil diedit"}
        except:
            return {"msg" : "Gagal edit"}
    
    def delete(self, id):
        query = Categories.query.filter_by(id_kategori=id).first()
        if not query:
            return {"msg" : "Gagal hapus data"}
        db.session.delete(query)
        db.session.commit()
        return {"msg" : "Data berhasil dihapus"}

api.add_resource(Kategori, "/kategori", methods=["GET", "POST"])
api.add_resource(SeleksiKategori, "/kategori/<int:id>", methods=["GET", "PUT", "DELETE"])

class Berita(Resource):
    def get(self):
        query = db.session.query(News, Categories).join(Categories).all()
        list = [{
            "ID Berita" : data.id_news,
            "Isi berita" : data.content,
            "Kategori" : data2.nama_kategori
        }
        for data, data2 in query 
        ]
        output = {
            "msg" : "List Berita :",
            "list" : list
        }
        return output
        
    def post(self):
        input_berita = request.form["content"]
        input_kategori = request.form["id_kategori"]
        cek = Categories.query.filter_by(id_kategori=input_kategori).first()
        if not cek:
            return {"msg" : "Kategori tidak tersedia"}
        ber = News(content = input_berita, id_kategori = input_kategori)
        ber.save()
        query = News.query.all()
        id = []
        for data in query:
            id.append(data.id_news)
        output = id[-1]
        return {"Data tersimpan dengan ID berita" : output}
    
class SeleksiBerita(Resource):
    def get(self, id):
        query = News.query.filter_by(id_news=id).first()
        if not query:
            return {"msg" : "Data tidak ditemukan"}
        cat = Categories.query.filter_by(id_kategori = query.id_kategori).first()
        detail = {
            "ID Berita" : query.id_news,
            "Isi Berita" : query.content,
            "Kategori" : cat.nama_kategori
        }
        return detail
    
    def put(self, id):
        query = News.query.filter_by(id_news=id).first()
        try:
            editIsi = request.form["content"]
            editKategori = request.form["id_kategori"]
            query.content = editIsi
            query.id_kategori = editKategori
            db.session.commit()
            return {"msg" : "Data berhasil diedit"}
        except:
            return {"msg" : "ID telah digunakan"}
    
    def delete(self, id):
        query = News.query.filter_by(id_news=id).first()
        if not query:
            return {"msg" : "Gagal hapus data"}
        db.session.delete(query)
        db.session.commit()
        return {"msg" : "Data berhasil dihapus"}

api.add_resource(Berita, "/berita", methods=["GET", "POST"])
api.add_resource(SeleksiBerita, "/berita/<int:id>", methods=["GET", "PUT", "DELETE"])

class Halaman(Resource):
    def get(self):
        query = PageCustom.query.all()
        list = [{
            "ID Halaman" : data.id_page,
            "URL" : data.url,
            "Konten" : data.page_content
        }
        for data in query
        ]
        output = {
            "msg" : "List Page Custom :",
            "list" : list
        }
        return output
        
    def post(self):
        input_url = request.form["url"]
        input_content = request.form["page_content"]
        pag = PageCustom(url = input_url, page_content=input_content)
        pag.save()
        query = PageCustom.query.all()
        id = []
        for data in query:
            id.append(data.id_page)
        output = id[-1]
        return {"Data tersimpan dengan ID Page" : output}
    
class SeleksiHalaman(Resource):
    def get(self, id):
        query = PageCustom.query.filter_by(id_page=id).first()
        if not query:
            return {"msg" : "Data tidak ditemukan"}
        detail = {
            "ID Page" : query.id_page,
            "URL" : query.url,
            "Isi Halaman" : query.page_content
        }
        return detail
    
    def put(self, id):
        query = PageCustom.query.filter_by(id_page=id).first()
        try:
            edit_url = request.form["url"]
            editIsi = request.form["page_content"]
            query.url = edit_url
            query.page_content = editIsi
            db.session.commit()
            return {"msg" : "Data berhasil diedit"}
        except:
            return {"msg" : "ID telah digunakan"}
    
    def delete(self, id):
        query = PageCustom.query.filter_by(id_page=id).first()
        if not query:
            return {"msg" : "Gagal hapus data"}
        db.session.delete(query)
        db.session.commit()
        return {"msg" : "Data berhasil dihapus"}

api.add_resource(Halaman, "/halaman", methods=["GET", "POST"])
api.add_resource(SeleksiHalaman, "/halaman/<int:id>", methods=["GET", "PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True)