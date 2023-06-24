from pymongo import MongoClient
from imagen_string import *
from bson import ObjectId

#usuario:   admonlibreria
#clave:     vnAOeQPw9Ul24eCD


class Conexion(object):
    """docstring for Conexion."""

    def __init__(self, basedatos = 'libreria'):
        super(Conexion, self).__init__()
        self.client = MongoClient("mongodb+srv://admonlibreria:vnAOeQPw9Ul24eCD@liby.jinkq.mongodb.net/?retryWrites=true&w=majority")
        self.bd = self.client.liby
        self.collecciones = []

    def insertarDocumento(self, doc, colec):#se inserta un documento en la coleccion indicada
        coleccion = self.bd[colec]
        coleccion.insert_one(doc)

    def eliminarPrimerDocumento(self, colec, condicion):#se elimina el primer documento en encontrarse
        coleccion = self.bd[colec]
        coleccion.delete_one(condicion)

    def eliminarMuchosDocumentos(self, colec, condicion):#se eliminan todos los que cumplan la condicion
        coleccion = self.bd[colec]
        coleccion.delete_many(condicion)

    def eliminarTodosDocumentos(self, colec):#se vacia la coleccion
        coleccion = self.bd[colec]
        coleccion.delete_many({})

    def contarDocumentosCondicion(self, colec, condicion):#se cuentan cuantos documentos cumplen una condicion
        coleccion = self.bd[colec]
        resultado = coleccion.count_documents(condicion)
        return resultado

    def contarTodosDocumentos(self, colec):#se cuentan todos los documentos de una coleccion
        coleccion = self.bd[colec]
        resultado = coleccion.count_documents({})
        return resultado

    def buscarTodos(self, colec, condicion):#se buscan todos los elementos de una coleccion y se devuelven
        coleccion = self.bd[colec]
        resultado = coleccion.find(condicion)
        res = []
        for r in resultado:
            res.append(r)

        return res

    def buscarTermino(self, colec, termino):#se buscan todos los elementos de una coleccion y se devuelven
        coleccion = self.bd[colec]
        resultado = coleccion.find({"$text": {"$search": termino}})
        res = []
        for r in resultado:
            res.append(r)

        return res

    def buscarAleatorio(self,colec,n = 1):
        coleccion = self.bd[colec]
        resultado = coleccion.aggregate([{"$sample": {"size": n }}])
        res = []
        for r in resultado:
            res.append(r)

        return res

    def actualizarDocumentos(self,colec, condicion, newdoc):
        coleccion = self.bd[colec]
        coleccion.update_one(condicion,{ "$set": newdoc})

    def buscarN(self, colec, limite, condicion = "nada"):#se buscan todos los elementos de una coleccion y se devuelven
        coleccion = self.bd[colec]
        if condicion == "nada":
            resultado = coleccion.find().limit(limite)
        else:
            resultado = coleccion.find(condicion).limit(limite)

        res = []
        for r in resultado:
            res.append(r)

        return res

    def buscarUltimosN(self,colec,limite,condicion = "nada"):
        coleccion = self.bd[colec]
        cuantos = self.contarTodosDocumentos(colec)
        cuantos = cuantos - limite
        if condicion == "nada":
            resultado = coleccion.find().skip(cuantos)
        else:
            resultado = coleccion.find(condicion).skip(cuantos-1)

        res = []
        for r in resultado:
            res.append(r)

        return res

    def buscarPrimero(self, colec, condicion = "nada"):#se busca el primer documento de una coleccion que cumpla una condicion
        coleccion = self.bd[colec]
        if condicion == "nada":
            resultado = coleccion.find_one()
        else:
            resultado = coleccion.find_one(condicion)
        return resultado


    def crearColeccion(self, colec):#se crea una coleccion
        coleccion = self.bd[colec]
        self.collecciones.append(colec)


    def eliminarColeccion(self, colec):#se elimina una coleccion
        coleccion = self.bd[colec]
        coleccion.drop()

if __name__== '__main__':
#________________________________SECCION PARA GUARDAR UNA IMAGEN CONSULTADA
    BaseDatos = Conexion('libreria')
    #imagenstring = ImagenBase64()#creacion de la clase para convertir imagenes
    #consulta = BaseDatos.buscarPrimero('libros')#con esta consulta obtenenmos el primero de la lista
    #imagenstring.guardarImg('./static/PORTADAS/temp1.png',consulta['imagen'])
#________________________________________________________________________________
    #cadena = imagenstring.imagenString('./PORTADAS/ZONA_CIEGA.jpg')
    #las fechas se manejan asi: aaaa-mm-dd, se ingresan con un input de tipo date
    jsonson = {"articulos": ObjectId('6290481b56e48d5457a3e1b9'),
            "usuario": ObjectId('62942d715dd9d66f1c046ec7')
          }
    consulta = BaseDatos.insertarDocumento(jsonson,'favoritos')
