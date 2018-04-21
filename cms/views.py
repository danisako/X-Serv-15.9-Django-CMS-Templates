from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout


formulario = """
<form action = "" method ="POST">
	Nombre: <input type="text" name="nombre" value=""><br>
    Pagina: <input type="text" name="page" value=""><br>
    <input type="submit" value="Enviar">
    </form>
"""


@csrf_exempt
def index(request):
	if request.user.is_authenticated():
		logged = "Logged in as -->  " + request.user.username + "</br></br>"
		logged += formulario
		if request.method == "POST":
			pagina = Pages(name = request.POST['nombre'], page = request.POST['page'])
			pagina.save()
	else:
		logged = 'Not logged in. Entra para poder añadir páginas </br></br>'

	
	respuesta = logged+ "<h1>Lista de páginas: </h1></br>"
	paginas = Pages.objects.all()
	
	for p in paginas:
		respuesta += "<h2>Nombre de pagina:" + p.name + "</h2><li>Contenido:" +str(p.page) + "    <li>Id:"+str(p.id)+"</br>"
		respuesta += "<li><a href=cms/" + str(p.name) + ">Enlace a la página de: " + p.name + "</a></li><br>"


	template = get_template("plantilla/index.html")
	c = Context({'logged':logged , 'title': "Pagina principal" , 'content':respuesta  , 'url': "http://google.es" , 'algo':"Google"})
	
	return HttpResponse(template.render(c))
		
	#return HttpResponse(respuesta)


def muestra(request,name):
	
	try:
		pagina = Pages.objects.get(name = name)
		respuesta = "<h1>"+pagina.page+"</h1>"

		template = get_template("plantilla/index.html")
		c = Context({ 'title': pagina.name , 'content':respuesta  , 'url': "http://google.es" , 'algo':"Google"})
		return HttpResponse(template.render(c))

	except Pages.DoesNotExist:
		respuesta = "<h2>La página que intentas acceder no existe, por favor vuelve a intentarlo</h2>"

	
		return HttpResponse(respuesta)
	

	
	#return HttpResponse(respuesta)

def redirect(request):

	resp = "<title>CMS</title><h2>Autenticado como: " +request.user.username +"</h2></br>"
	resp += '<head><meta http-equiv="Refresh" content="5;url='"http://127.0.0.1:8000"'"></head>'" Redirigiendo a la pagina principal " 
	
	template = get_template("plantilla/index.html")
	c = Context({'title': "Pagina principal" , 'content':resp })

	#return HttpResponse(resp)
	return HttpResponse(template.render(c))




def new_page(request,name,content):
	if request.method == "GET":
		new_page = Pages(name = name,page = content)
		new_page.save()
	elif request.method == "PUT" or request.method == "POST":
		new_page = Pages(name = name, page = request.body)
		new_page.save()
	return HttpResponse("<h2>Pagina añadida correctamente!</h2>")
