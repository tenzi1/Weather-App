import requests
from django.shortcuts import render,  redirect
from .models import City
from .forms import CityModelForm
import env
def home(request):
   
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={env.api_key}&units=imperial'
    
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityModelForm(request.POST)
        
        if form.is_valid():
            print('valid data arrived')
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the World'

                
            else:
                err_msg = 'City already exists in the database'
        
    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    else:
        message = 'City added successfully'
        message_class = 'is-success'
    
    form = CityModelForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        res = requests.get(url.format(city)).json()

        city_weather = {
        'city': city.name,
        'temperature': res['main']['temp'],
        'description': res['weather'][0]['description'],
        'icon': res['weather'][0]['icon'],
            }

        weather_data.append(city_weather)
    
        
    
    context = {
        'weather_data':weather_data,
        'form':form,
        'message':message,
        'message_class': message_class
        
    }
        
    return render(request, 'weather/weather.html', context)



    

    
    


