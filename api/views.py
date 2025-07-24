import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Company
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class CompanyView(View):

    # Este método se ejecuta cada vez que hacemos una peticion es decir un request
    @method_decorator(csrf_exempt) # Con esto evitamos la validacion de csrf
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:

            companies = list(Company.objects.filter(id=id).values())

            if len(companies) > 0: # Existe el registro
                datos = {'message': 'Success', 'company': companies[0]}
            else:
                datos = {'message': 'Company not found'}
        else:

            companies = list(Company.objects.values()) # Obtenemos los datos de esta forma para poder serializarlo como un JSON

            if len(companies) > 0:
                datos = {'message': 'Success', 'companies': companies}
            else:
                datos = {'message': 'Companies not found'}
            
        return JsonResponse(datos)


    def post(self, request):
        # print(request.body) # -> información en formato JSON
        jd = json.loads(request.body) # Transformamos el JSON en diccionario
        # print(jd)
        Company.objects.create(name= jd['name'], website= jd['website'], foundation= jd['foundation'])
        datos = {'message': 'Success'}
        return JsonResponse(datos)

    def put(self, request, id):

        jd = json.loads(request.body)
        companies = list(Company.objects.filter(id=id).values())

        if len(companies) > 0: # Existe el registro
            """ Diferencia entre Company.objects.get y Company.objects.filter 
            Con get obtenemos el objeto en sí, podemos cambiar el valor de sus atributos
            Con filter es como hacer una consulta, filtramos los registros pero no tenemos los objetos en sí
            """
            # company = Company.objects.get(id=id)
            # company.name = jd['name']
            # company.website = jd['website']
            # company.foundation = jd['foundation']
            # company.save()

            # Otra manera de actualizar:
            Company.objects.filter(id=id).update(
                name= jd['name'],
                website= jd['website'],
                foundation= jd['foundation']
            )

            datos = {'message': 'success'}

        else:
            datos = {'message': 'Company not found'}
        
        return JsonResponse(datos)


    def delete(self, request, id):
        companies = list(Company.objects.filter(id=id).values())

        if len(companies) > 0: # Existe el registro
            Company.objects.filter(id=id).delete()
            datos = {'message': 'success'}
        else:
            datos = {'message': 'Company not found'}

        return JsonResponse(datos)