from django.shortcuts import render
import requests
# Create your views here.

## GeoCoding api
## api key = '0e3a9889a5e449af9feda4c9e1e82dd2'
## api = https://api.opencagedata.com/geocode/v1/json?q=URI-ENCODED-PLACENAME&key=0e3a9889a5e449af9feda4c9e1e82dd2
# r = requests.get('https://api.opencagedata.com/geocode/v1/json?q=Jalgaon%20Maharashtra&key=0e3a9889a5e449af9feda4c9e1e82dd2')
# print(r.json())

## weather api
# APIkey = 'e86d313cd350cc88b11d2a12b51a4107'
# r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=e86d313cd350cc88b11d2a12b51a4107')

place = ""
def home(request):
    if request.method=='POST':
        global place
        place = request.POST.get('query')
        place = place.replace(' ', '%20')
        r = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={place}%20Maharashtra&key=0e3a9889a5e449af9feda4c9e1e82dd2')
        lat = r.json()['results'][0]['annotations']['DMS']['lat'][:6].replace('° ', '.')
        lon = r.json()['results'][0]['annotations']['DMS']['lng'][:6].replace('° ', '.')

        context = {}
        r2 = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=e86d313cd350cc88b11d2a12b51a4107')
        context['place'] = place.replace('%20', ' ')
        context['cloud'] = r2.json()['weather'][0]['description']
        context['deg'] = round(int(r2.json()['main']['temp']) - 273.15, 2)
        context['maxdeg'] = round(int(r2.json()['main']['temp_max']) - 273.15, 2)
        context['mindeg'] = round(int(r2.json()['main']['temp_min']) - 273.15, 2)
        context['pressure'] = str(r2.json()['main']['pressure']) + ' hPa'
        context['windspeed'] = r2.json()['wind']['speed']
        context['winddeg'] = r2.json()['wind']['deg']
        return render(request, 'result.html', context)
    return render(request, 'home.html')

# def resultpage(request):
#     return render(request, 'result.html')
