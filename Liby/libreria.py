from ast import Pass
from crypt import methods
from flask import Flask, render_template,request, redirect, url_for, make_response, session, escape
from pymongo import MongoClient
from conexion_mongo import *
from imagen_string import *
from random import choice
from datetime import datetime
from bson.objectid import ObjectId

libreria = Conexion()# conexion con base de datos
imagenes = ImagenBase64()

liby = Flask(__name__)
liby.secret_key = "0000"

#Metodos para redireccionar a templates

@liby.route('/')
def index():
    #consultas
    moreselled = libreria.buscarN('libros',5)
    morerecent = libreria.buscarUltimosN('libros',6)
    recomended = libreria.buscarAleatorio('libros',6)

    #creacion de informacion para pasar a html______

    for e in moreselled:
        imagenes.guardarImg('./static/images/portadalibro'+e['ISSN']+'.png',e['imagen'])
    for e in morerecent:
        imagenes.guardarImg('./static/images/portadalibro'+e['ISSN']+'.png',e['imagen'])
    for r in recomended:
        imagenes.guardarImg('./static/images/portadalibro'+r['ISSN']+'.png',r['imagen'])

    loged = "no"
    if 'carrito' in session:
        loged = "si"


    return render_template('Liby.html', titulo_pagina = 'LiBy', masvendidos = moreselled, nuevos = morerecent, recomendados = recomended, logueado = loged)

@liby.route('/Perfil')
def perfil():
    return render_template('Perfil.html', titulo_pagina ='Perfil')

@liby.route('/Perfil_Administracion')
def perfil_admon():
    return render_template('Perfil_admon.html', titulo_pagina ='Administracion')

@liby.route('/Login', methods=['POST','GET'])
def login():
    if 'usuario' in session:
        return redirect(url_for('perfil'))
    elif 'admin' in session:
        return redirect(url_for('perfil_admon'))
    return render_template('Login.html',titulo_pagina = 'Iniciar Sesion')

@liby.route('/Registrarse',methods=['POST','GET'])
def registro():
    return render_template('Registro.html',titulo_pagina = 'Registrarse')

@liby.route('/Buscar/<string:termino>',methods=['POST','GET'])
def busqueda(termino):
    if termino == "__recomendar__":
        consulta1 = libreria.buscarAleatorio('libros',18)
    else:
        consulta1 = libreria.buscarTermino('libros',termino)

    for elemento in consulta1:
        cadena = elemento['imagen']
        imagenes.guardarImg('./static/images/portadalibro'+elemento['ISSN']+'.png',cadena)
    
    loged = "no"
    if 'carrito' in session:
        loged = "si"

    return render_template('busqueda.html', titulo_pagina = 'Buscando',libros = consulta1, valor = termino, logueado = loged)

@liby.route('/Buscar2/<string:termino>',methods=['POST','GET'])
def busqueda2(termino):
    if termino == "__recomendar__":
        consulta1 = libreria.buscarAleatorio('libros',18)
    else:
        consulta1 = libreria.buscarTermino('libros',termino)

    for elemento in consulta1:
        cadena = elemento['imagen']
        imagenes.guardarImg('./static/images/portadalibro'+elemento['ISSN']+'.png',cadena)

    return render_template('Administracion_libros_EL.html',titulo_pagina = 'Inventario', libros = consulta1, valor = termino)

@liby.route('/Buscar3/<string:termino>',methods=['POST','GET'])
def busqueda3(termino):
    if termino == "__recomendar__":
        consulta1 = libreria.buscarAleatorio('libros',18)
    else:
        consulta1 = libreria.buscarTermino('libros',termino)

    for elemento in consulta1:
        cadena = elemento['imagen']
        imagenes.guardarImg('./static/images/portadalibro'+elemento['ISSN']+'.png',cadena)

    return render_template('Administracion_libros_DL.html',titulo_pagina = 'Inventario', libros = consulta1, valor = termino)


@liby.route('/VerLibro/<string:codigo>')
def informacionLibro(codigo):
    consulta = libreria.buscarPrimero('libros',{"ISSN": codigo})
    consulta2 = libreria.buscarTodos('favoritos',{"articulos": consulta['_id']})
    consulta['_id'] = str(consulta['_id'])
    idc = "ninguno"
    if 'id' in session:
        userr = "si"
        favorito = "no"
        
        for c in consulta2:
            if session['id'] == str(c['usuario']):
                favorito = "si"
                idc = str(c['_id'])
    else:
        userr = "no"
        favorito = "no"

    imagenes.guardarImg('./static/images/portadalibro'+consulta['ISSN']+'.png',consulta['imagen'])
    if consulta['ISSN'] == codigo:
        recomended = libreria.buscarTodos('libros',{"genero": consulta['genero']})
        recomended2 = []
        for r in range(len(recomended)):
            elemento = choice(recomended)
            recomended2.append(elemento)
            imagenes.guardarImg('./static/images/portadalibro'+elemento['ISSN']+'.png',elemento['imagen'])
        loged = "no"
        agregaded = "no"
        if 'carrito' in session:
            carritoarts = session['carrito']
            for art in carritoarts:
                if consulta['_id'] == art[0]:
                    agregaded = "si"
            loged = "si"
        return render_template('libro.html',titulo_pagina = consulta['titulo'],informacion = consulta, recomendados = recomended2, cantidad = len(recomended),fav = favorito, cliente = userr, idfav = idc, logueado = loged, added = agregaded)
    else:
        return 'Error: No encontramos lo que estan buscando'

@liby.route('/EditarLibro/<string:codigo>')
def editarInformacionLibro(codigo):
    
    consulta = libreria.buscarPrimero('libros',{"ISSN": codigo})
    
    consulta['_id'] = str(consulta['_id'])

    if consulta['ISSN'] == codigo:
        return render_template('Administracion_libros_EL_libro.html',titulo_pagina = consulta['titulo'],informacion = consulta)
    else:
        return 'Error: No encontramos lo que estan buscando'

@liby.route('/SuprimirLibro/<string:codigo>')
def eliminacionLibro(codigo):
    
    consulta = libreria.buscarPrimero('libros',{"ISSN": codigo})
    
    cadenisius = str(consulta['_id'])

    if consulta['ISSN'] == codigo:
        return render_template('Administracion_libros_DL_confirmar.html',titulo_pagina = "Confirmacion",informacion = cadenisius, titulolibro = consulta['titulo'])
    else:
        return 'Error: No encontramos lo que estas buscando'

#Metodos y rutas para modificaciones en perfil usuario

@liby.route('/Actualizar_perfil',methods=['POST','GET'])
def actualizarPerfil():
    if 'id' in session:
        consulta = libreria.buscarPrimero('usuarios',{"_id": ObjectId(session['id'])})
        consulta['_id'] = session['id']
        return render_template('update_perfil.html',titulo_pagina = 'Perfil', usuario = consulta)
    return "Ha ocurrido un problema"

@liby.route('/Favoritos',methods=['POST','GET'])
def favoritos():
    if 'id' in session:
        consulta = libreria.buscarTodos('favoritos',{"usuario": ObjectId(session['id'])})
        ids = []
        print(consulta)
        for e in consulta:
            info = libreria.buscarPrimero('libros', {"_id": e['articulos']})
            ids.append(info)
        for e in ids:
            imagenes.guardarImg('./static/images/portadalibro'+e['ISSN']+'.png',e['imagen'])

        return render_template('favoritos.html',titulo_pagina = 'Perfil', libros = ids)

@liby.route('/Reservas',methods=['POST','GET'])
def reservas():
    consulta = libreria.buscarTodos('reservaspagos',{"tipo": "reserva", "usuario": ObjectId(session['id'])})#esto se debe cambiar, agregar id usuario
    return render_template('mis_reservas.html',titulo_pagina = 'Perfil',reservas = consulta)

@liby.route('/Historial',methods=['POST','GET'])
def historial():
    consulta = libreria.buscarTodos('reservaspagos',{"tipo": "pago", "usuario": ObjectId(session['id'])})#esto se debe cambiar, agregar id usuario
    return render_template('historial.html',titulo_pagina = 'Perfil', reservas = consulta)

@liby.route('/Noticias',methods=['POST','GET'])
def noticias():
    if 'id' in session:
        consulta = libreria.buscarPrimero('usuarios', {"_id": ObjectId(session['id'])})
        return render_template('news.html',titulo_pagina = 'Perfil',estado = consulta['suscripcion'], informacion = session['id'])
    
    return "Ha ocurrido un problema"

@liby.route('/Carrito',methods=['POST','GET'])
def carrito():
    articulos = session['carrito']
    total = 0
    print(datetime.today().strftime('%Y'))
    print(datetime.today().strftime('%m'))
    print(datetime.today().strftime('%d'))
    for e in articulos:
        info = libreria.buscarPrimero('libros', {"_id": ObjectId(e[0])})
        info['_id'] = e[0]
        e[0] = info
        total2 = info['precio'] * e[1]
        total = total + total2
        
    return render_template('carrito.html',titulo_pagina = "Carrito de compras", articles = articulos, total = total)

@liby.route('/Resumen_Compra',methods=['POST','GET'])
def resumenCompra():
    articulos = session['carrito']
    total = 0
    print(datetime.today().strftime('%Y'))

    for e in articulos:
        info = libreria.buscarPrimero('libros', {"_id": ObjectId(e[0])})
        print(e[0])
        info['_id'] = e[0]
        e[0] = info
        total2 = info['precio'] * e[1]
        total = total + total2
        
    return render_template('resumencompra.html',titulo_pagina = "Pasarela", articles = articulos, total = total)

@liby.route('/Pagar_Ahora/<int:total>',methods=['POST','GET'])
def pagarAhora(total):
    return render_template('pagar_ahora.html', titulo_pagina = "Realizar Pago", total = total)

@liby.route('/Pagar_Ahora2/<string:id>/<string:total>',methods=['POST','GET'])
def pagarAhora2(id,total):
    return render_template('pagar_ahora2.html', titulo_pagina = "Realizar Pago", total = total, id = id)

@liby.route('/Pagar_Despues/<int:total>',methods=['POST','GET'])
def pagarDespues(total):
    articulos = session['carrito']
    for e in articulos:
        info = libreria.buscarPrimero('libros', {"_id": ObjectId(e[0])})
        print(e[0])
        info['_id'] = e[0]
        e[0] = info
    return render_template('pagar_despues.html', titulo_pagina = "Reservar", total = total,articles = articulos)

@liby.route('/Pagar',methods=['POST'])
def pagar():
    articulos = session['carrito']
    precio = request.form['cantida']
    ano = datetime.today().strftime('%Y')
    mes = datetime.today().strftime('%m')
    dia = datetime.today().strftime('%d')

    for e in articulos:
        e[0] = ObjectId(e[0])

    jsonson = {"diar": dia,
          "mesr": mes,
          "anor": ano,
          "diap": dia,
          "mesp": mes,
          "anop": ano,
          "articulos": articulos,
          "valortotal": precio,
          "usuario": ObjectId(session['id']),
          "tipo": "pago"
    }
    libreria.insertarDocumento(jsonson,'reservaspagos')
    session['carrito'] = []
    return redirect(url_for('index'))

@liby.route('/Pagar2',methods=['POST'])
def pagar2():
    id = request.form['identificador']
    ano = datetime.today().strftime('%Y')
    mes = datetime.today().strftime('%m')
    dia = datetime.today().strftime('%d')

    consulta = libreria.buscarPrimero('reservaspagos',{"_id": ObjectId(id)})

    jsonson = {"diar": consulta['diar'],
          "mesr": consulta['mesr'],
          "anor": consulta['anor'],
          "diap": dia,
          "mesp": mes,
          "anop": ano,
          "articulos": consulta['articulos'],
          "valortotal": consulta['valortotal'],
          "usuario": consulta['usuario'],
          "tipo": "pago"
    }
    libreria.insertarDocumento(jsonson,'reservaspagos')
    libreria.eliminarPrimerDocumento('reservaspagos',{"_id": ObjectId(id)})
    return redirect(url_for('reservas'))


@liby.route('/Reservar',methods=['POST'])
def reservar():
    articulos = session['carrito']
    precio = request.form['cantida']
    ano = datetime.today().strftime('%Y')
    mes = datetime.today().strftime('%m')
    dia = datetime.today().strftime('%d')

    for e in articulos:
        e[0] = ObjectId(e[0])

    jsonson = {"diar": dia,
          "mesr": mes,
          "anor": ano,
          "articulos": articulos,
          "valortotal": precio,
          "usuario": ObjectId(session['id']),
          "tipo": "reserva"
    }
    libreria.insertarDocumento(jsonson,'reservaspagos')
    session['carrito'] = []
    return redirect(url_for('index'))

#Metodos y rutas para modificaciones de administracion
    #Rutas principales
@liby.route('/Administrar_inventario',methods=['POST','GET'])
def admonInventario():
    return render_template('Administracion_libros.html',titulo_pagina = 'Inventario')

@liby.route('/Administrar_RP',methods=['POST','GET'])
def admonRP():
    return render_template('Administracion_rp.html',titulo_pagina = 'RP')

#Rutas secundarias de administracion

@liby.route('/Administrar_inventario/Agregar_libro',methods=['POST','GET'])
def agregarLibro():
    return render_template('Administracion_libros_AL.html',titulo_pagina = 'Inventario')

@liby.route('/Administrar_inventario/Editar_libro',methods=['POST','GET'])
def editarLibro():
    return render_template('Administracion_libros_EL.html',titulo_pagina = 'Inventario')

@liby.route('/Administrar_inventario/Eliminar_libro',methods=['POST','GET'])
def eliminarLibro():
    return render_template('Administracion_libros_DL.html',titulo_pagina = 'Inventario')

@liby.route('/Administrar_RP/Reservas',methods=['POST','GET'])
def gestionreservas():

    consulta = libreria.buscarTodos('reservaspagos',{"tipo": "reserva"})

    return render_template('Administracion_R.html',titulo_pagina = 'RP',reservas = consulta)

@liby.route('/Administrar_RP/Pagos',methods=['POST','GET'])
def gestionpagos():
    consulta = libreria.buscarTodos('reservaspagos',{"tipo": "pago"})
    return render_template('Administracion_P.html',titulo_pagina = 'RP', reservas = consulta)

#Metodos para comprobaciones
@liby.route('/Buscar',methods=['POST'])
def buscar():
    if request.method == "POST":
        if request.form:
            term = request.form['entrada']
            if term == "":
                term = "__recomendar__"
        else:
            term = "__recomendar__"

    return redirect(url_for('busqueda',termino = term))

@liby.route('/Buscar2',methods=['POST'])
def buscar2():
    if request.method == "POST":
        if request.form:
            term = request.form['entrada']
            if term == "":
                term = "__recomendar__"
        else:
            term = "__recomendar__"

    return redirect(url_for('busqueda2',termino = term))

@liby.route('/Buscar3',methods=['POST'])
def buscar3():
    if request.method == "POST":
        if request.form:
            term = request.form['entrada']
            if term == "":
                term = "__recomendar__"
        else:
            term = "__recomendar__"

    return redirect(url_for('busqueda3',termino = term))

@liby.route('/Modificar_Clave/<string:id>',methods=['GET','POST'])
def cambiarClave(id):
    return render_template('update_perfil_CC.html', titulo_pagina = "Confirmacion", informacion = id)

@liby.route('/Modificar_Clave',methods=['POST'])
def changepassword():
    aidi = request.form['identificador']
    contra = request.form['clave']

    usuarisius = libreria.buscarPrimero('usuarios', {"_id": ObjectId(aidi)})

    if contra == usuarisius['clave']:
        return render_template('update_perfil_CC2.html', titulo_pagina = "Confirmacion", informacion = aidi)
    
    return redirect(url_for('actualizarPerfil'))

@liby.route('/Modificar_Clave_Final',methods=['POST'])
def changepasswordf():
    aidi = request.form['identificador']
    contra = request.form['clave']

    usuarisius = libreria.buscarPrimero('usuarios', {"_id": ObjectId(aidi)})

    usuarisius['clave'] = contra

    libreria.actualizarDocumentos('usuarios',{"_id": ObjectId(aidi)},usuarisius)
    return redirect(url_for('actualizarPerfil'))

@liby.route('/Logout',methods=['POST','GET'])
def logout():
    if 'usuario' in session:
        session.pop('usuario',None)
        session.pop('clave',None)
        session.pop('id',None)
        session.pop('carrito',None)
    elif 'admin' in session:
        session.pop('admin',None)
        session.pop('clave',None)

    return redirect(url_for('index'))

@liby.route('/login_check',methods=['POST'])
def login_check():
    if request.method == "POST":
        user = request.form['usuario']
        contra = request.form['clave']

        consulta = libreria.buscarPrimero('usuarios',{"usuario": user})

        if user == consulta['usuario']:
            if contra == consulta['clave']:
                if consulta['admin'] == 0:
                    session['usuario'] = user
                    session['clave'] = contra
                    session['id'] = str(consulta['_id'])
                    session['carrito'] = []
                elif consulta['admin'] == 1:
                    session['admin'] = user
                    session['clave'] = contra
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@liby.route('/register_check',methods=['POST'])
def register_check():
    name = request.form['nombre']
    lastname = request.form['apellido']
    datete = request.form['fecha']
    mail = request.form['correo']
    user = request.form['usuario']
    contra = request.form['clave']
    identification = request.form['documento']
    tipe = request.form['tipo']

    consulta = libreria.buscarPrimero('usuarios',{"usuario": user})

    if not consulta:
        jsonson = {"nombre": name,
            "apellido": lastname,
            "nacimiento": datete,
            "correo": mail,
            "usuario": user,
            "clave": contra,
            "documento": identification,
            "tipodocumento": tipe,
            "admin": 0,
            "suscripcion": 0
          }
        libreria.insertarDocumento(jsonson,'usuarios')

        session['usuario'] = user
        session['clave'] = contra

        consulta2 = libreria.buscarPrimero('usuarios',{"usuario": user})

        session['id'] = str(consulta2['_id'])
        session['carrito'] = []

        return redirect(url_for('perfil'))
    else:
        return redirect(url_for('registro'))

@liby.route('/update_check',methods=['POST'])
def update_check():
    aidi = request.form['identificador']
    name = request.form['nombre']
    lastname = request.form['apellido']
    datete = request.form['nacimiento']
    email = request.form['correo']
    user = request.form['usuarioso']
    contra = request.form['clave']

    consulta = libreria.buscarPrimero('usuarios',{"_id": ObjectId(aidi)})

    if not name == consulta['nombre']:
        consulta['nombre'] = name
    if not lastname == consulta['apellido']:
        consulta['apellido'] = lastname
    if not datete == consulta['nacimiento']:
        consulta['nacimiento'] = datete
    if not email == consulta['correo']:
        consulta['correo'] = email
    if not user == consulta['usuario']:
        consulta['usuario'] = user
    if not contra == consulta['clave']:
        consulta['clave'] = contra

    libreria.actualizarDocumentos('usuarios',{"_id": ObjectId(aidi)},consulta)
    return redirect(url_for('actualizarPerfil'))

@liby.route('/add_book',methods=['POST','GET'])
def addbook():
    title = request.form['titulo']
    autorr = request.form['autor']
    ano = request.form['anopublicacion']
    mes = request.form['mespublicacion']
    dia = request.form['diapublicacion']
    gender = request.form['genero']
    pages = request.form['paginas']
    edit = request.form['editorial']
    idISSN = request.form['issn']
    language = request.form['idioma']
    amount = request.form['cantidad']
    price = request.form['precio']
    imagenlibro = request.form['portada']

    print(imagenlibro)

    cadena = imagenes.imagenString("./static/PORTADAS/"+imagenlibro)

    jsonson = {"titulo": title,
            "autor": autorr,
            "imagen": cadena,
            "anopublicacion": ano,
            "mespublicacion": mes,
            "diapublicacion": dia,
            "genero": gender,
            "paginas": int(pages),
            "editorial": edit,
            "ISSN": idISSN,
            "idioma": language,
            "estado": "Nuevo",
            "disponibilidad": "disponible",
            "cantidad": int(amount),
            "precio": int(price)
            }

    libreria.insertarDocumento(jsonson,'libros')

    return redirect(url_for('admonInventario'))

@liby.route('/edit_book',methods=['POST','GET'])
def editbook():
    aidi = request.form['identificador']
    title = request.form['titulo']
    autorr = request.form['autor']
    ano = request.form['anopublicacion']
    mes = request.form['mespublicacion']
    dia = request.form['diapublicacion']
    gender = request.form['genero']
    pages = request.form['paginas']
    edit = request.form['editorial']
    idISSN = request.form['issn']
    language = request.form['idioma']
    amount = request.form['cantidad']
    price = request.form['precio']
    imagenlibro = request.form['portada']

    consulta = libreria.buscarPrimero('libros',{"_id": ObjectId(aidi)})

    if not title == consulta['titulo']:
        consulta['titulo'] = title

    if not autorr == consulta['autor']:
        consulta['autor'] = autorr

    if not ano == consulta['anopublicacion']:
        consulta['anopublicacion'] = ano

    if not mes == consulta['mespublicacion']:
        consulta['mespublicacion'] = mes

    if not dia == consulta['diapublicacion']:
        consulta['diapublicacion'] = dia

    if not gender == consulta['genero']:
        consulta['genero'] = gender
    
    if not pages == consulta['paginas']:
        consulta['paginas'] = pages

    if not edit == consulta['editorial']:
        consulta['editorial'] = edit
    
    if not idISSN == consulta['ISSN']:
        consulta['ISSN'] = idISSN

    if not language == consulta['idioma']:
        consulta['idioma'] = language

    if not amount == consulta['cantidad']:
        consulta['cantidad'] = amount

    if not price == consulta['precio']:
        consulta['precio'] = price

    if len(imagenlibro) > 3:#3 es la longuitud minima, ya que debe tener el .png
        cadena = imagenes.imagenString("./static/PORTADAS/"+imagenlibro)
        consulta['imagen'] = cadena

    libreria.actualizarDocumentos('libros',{"_id": ObjectId(aidi)},consulta)

    return redirect(url_for('admonInventario'))

@liby.route('/delete_book',methods=['POST','GET'])
def deletebook():
    aidi = request.form['identificador']

    libreria.eliminarPrimerDocumento('libros',{"_id": ObjectId(aidi)})

    return redirect(url_for('admonInventario'))

#METODOS PARA OPERACIONES EN PERFIL DE USUARIO
@liby.route('/Eliminar_Favorito/<string:id>/<string:cod>')
def eliminarFavorito(id,cod):
    libreria.eliminarPrimerDocumento('favoritos',{"_id": ObjectId(id)})
    return redirect(url_for('informacionLibro',codigo = cod))

@liby.route('/Agregar_Favorito/<string:id>/<string:cod>')
def agregarFavorito(id,cod):
    jsonson = {"articulos": ObjectId(id),
        "usuario": ObjectId(session['id'])
      }
    libreria.insertarDocumento(jsonson,'favoritos')
    return redirect(url_for('informacionLibro',codigo = cod))

@liby.route('/Agregar_Carrito/<string:id>/<string:cod>')
def agregarCarrito(id,cod):
    incluir = [id,1]
    carritoactual = session['carrito']
    carritoactual.append(incluir)
    session['carrito'] = carritoactual
    return redirect(url_for('informacionLibro',codigo = cod))

@liby.route('/Aumentar_Cantidad/<string:id>')
def aumentarCantidad(id):
    carritoactual = session['carrito']
    for a in carritoactual:
        if a[0] == id:
            print("entra")
            a[1] = a[1]+1
            print(a[1])
    session['carrito'] = carritoactual
    return redirect(url_for('carrito'))

@liby.route('/Disminuir_Cantidad/<string:id>')
def disminuirCantidad(id):
    carritoactual = session['carrito']
    for a in carritoactual:
        if a[0] == id:
            a[1] = a[1]-1

    for a in carritoactual:
        if a[1] == 0:
            carritoactual.remove(a)
    session['carrito'] = carritoactual
    return redirect(url_for('carrito'))

@liby.route('/Vaciar_Carrito')
def vaciarCarrito():
    session['carrito'] = []
    return redirect(url_for('carrito'))


@liby.route('/Eliminar_Carrito/<string:id>/<string:cod>')
def eliminarCarrito(id,cod):
    carritoactual = session['carrito']
    for e in carritoactual:
        if e[0] == id:
            carritoactual.remove(e)
    session['carrito'] = carritoactual
    return redirect(url_for('informacionLibro',codigo = cod))


@liby.route('/InfoReservaUser/<string:id>')
def informacionReserva2(id):
    reserva = libreria.buscarPrimero('reservaspagos', {"_id": ObjectId(id)})
    usuarisius = libreria.buscarPrimero('usuarios', {"_id": reserva['usuario']})
    articulosreserva = []
    cantidades = []

    for ar in reserva['articulos']:
        consulta = libreria.buscarPrimero('libros',{"_id": ar[0]})
        articulosreserva.append(consulta)
        cantidades.append(ar[1])
    
    return render_template('informacion_reservapago2.html',titulo_pagina = "Administracion Reservas",reserva = reserva,articulos = articulosreserva, cantidad = cantidades, usuario = usuarisius)

@liby.route('/EliminarReservaUserConfirmar/<string:id>')
def eliminarReserva2c(id):
    return render_template('mis_reservas_c.html',titulo_pagina = "Confirmar", identificador = id)


@liby.route('/EliminarReservaUser/<string:id>')
def eliminarReserva2(id):
    libreria.eliminarPrimerDocumento('reservaspagos',{"_id": ObjectId(id)})
    return redirect(url_for('reservas'))


@liby.route('/InfoPagoUser/<string:id>')
def informacionPago2(id):
    reserva = libreria.buscarPrimero('reservaspagos', {"_id": ObjectId(id)})
    usuarisius = libreria.buscarPrimero('usuarios', {"_id": reserva['usuario']})
    articulosreserva = []
    cantidades = []

    for ar in reserva['articulos']:
        consulta = libreria.buscarPrimero('libros',{"_id": ar[0]})
        articulosreserva.append(consulta)
        cantidades.append(ar[1])
    
    return render_template('informacion_reservapago2.html',titulo_pagina = "Administracion Reservas",reserva = reserva,articulos = articulosreserva, cantidad = cantidades, usuario = usuarisius)


@liby.route('/NoSub',methods=['POST'])
def nosub():
    identifi = request.form['identificador']
    consulta = libreria.buscarPrimero('usuarios',{"_id": ObjectId(identifi)})

    if consulta['suscripcion'] == 1:
        consulta['suscripcion'] = 0
    else:
        if consulta['suscripcion'] == 0:
            consulta['suscripcion'] = 1

    libreria.actualizarDocumentos('usuarios',{"_id": ObjectId(identifi)},consulta)

    return redirect(url_for('noticias'))

#METODOS PARA OPERACIONES EN PAGOS Y RESERVAS
@liby.route('/InfoPago/<string:id>')
def informacionPago(id):
    reserva = libreria.buscarPrimero('reservaspagos', {"_id": ObjectId(id)})
    usuarisius = libreria.buscarPrimero('usuarios', {"_id": reserva['usuario']})
    articulosreserva = []
    cantidades = []

    for ar in reserva['articulos']:
        consulta = libreria.buscarPrimero('libros',{"_id": ar[0]})
        articulosreserva.append(consulta)
        cantidades.append(ar[1])
    
    return render_template('informacion_reservapago.html',titulo_pagina = "Administracion Reservas",reserva = reserva,articulos = articulosreserva, cantidad = cantidades, usuario = usuarisius)

@liby.route('/InfoReserva/<string:id>')
def informacionReserva(id):
    reserva = libreria.buscarPrimero('reservaspagos', {"_id": ObjectId(id)})
    usuarisius = libreria.buscarPrimero('usuarios', {"_id": reserva['usuario']})
    articulosreserva = []
    cantidades = []

    for ar in reserva['articulos']:
        consulta = libreria.buscarPrimero('libros',{"_id": ar[0]})
        articulosreserva.append(consulta)
        cantidades.append(ar[1])
    
    return render_template('informacion_reservapago.html',titulo_pagina = "Administracion Reservas",reserva = reserva,articulos = articulosreserva, cantidad = cantidades, usuario = usuarisius)

@liby.route('/EliminarReserva/<string:id>')
def eliminarReserva(id):
    return 'reserva '+id+' eliminada'

#____________CICLO PRINCIPAL_____________________
if __name__=='__main__':
    liby.run(debug=True)
