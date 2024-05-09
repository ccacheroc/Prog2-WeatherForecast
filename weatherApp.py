import tkinter as tk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import requests
import pytz
from PIL import Image,ImageTk  #pillow


#https://openweathermap.org/price -> free plan -> CREO API KEY
#https://openweathermap.org/forecast5 -> copio API CALL



def getWeather():
    city=ciudad_entry.get() #texto que ha introducido el usuario en el campo de entrada
    #devuelve las coordenadas de cualquier dirección
    geolocator=Nominatim(user_agent="ccachero_prev_tiempo")
    location = geolocator.geocode(city)

    tzf=TimezoneFinder()
    #nombre de la zona horaria, compatible con muchas librerías
    what_timezone= tzf.timezone_at(lng=location.longitude, lat=location.latitude)

    #visualizamos datos
    timezone_label.config(text=what_timezone)
    long_lat_label.config(text=f"{round(location.longitude,2)}°N,{round(location.latitude,2)}°E")

    #pytz utiliza la cadena para crear un objeto de zona horaria que tiene en cuenta horarios de verano etc.
    objZonaHoraria=pytz.timezone(what_timezone)
    local_time=datetime.now(objZonaHoraria)
    clock_label.config(text=f"{local_time.strftime('%I:%M %p')}")

    #las API CALLS SE pueden probar en Postman
    api_key="896c25bc74199d03bd84d8bb90a2763f"
    api_call = f'https://api.openweathermap.org/data/2.5/forecast?lat={str(location.latitude)}&lon={str(location.longitude)}&appid={api_key}'

    #llamada a API desde Python

    response=requests.get(api_call)
    #print(response.text)  #esto es un string: representación en texto plano del json

    json_response=response.json() #para que la respuesta tenga el formato de diccionario o lista
    #en https://openweathermap.org/forecast5 está la estructura del JSON de respuesta

    #print(json_response)
    # Extraer los iconos de json
    #icons = [entry['weather'][0]['icon'] for entry in json_response['list']]
    # Imprimir los iconos
    #print(icons)

    def dameElementosJSON(json_response,dia):

        imagen=json_response['list'][dia]['weather'][0]['icon']
        #tiempo actual
        temperature=json_response['list'][dia]['main']['temp']
        humidity=json_response['list'][dia]['main']['humidity']
        pressure=json_response['list'][dia]['main']['pressure']
        wind_speed=json_response['list'][dia]['wind']['speed']
        description=json_response['list'][dia]['weather'][0]['description']

        return(imagen,temperature,humidity,pressure,wind_speed,description)

    kelvin_to_celsius=lambda k: k-273.15
    mps_to_kmph = lambda mps: mps * 3.6

    #mostrar datos de hoy
    imagen,temperature,humidity,pressure,wind_speed,description=dameElementosJSON(json_response,0)
    temp_value.config(text=f'{round(kelvin_to_celsius(temperature),1)} ºC')
    hum_value.config(text=f'{humidity}%')
    pres_value.config(text=f'{pressure}hPa')
    wind_value.config(text=f'{round(mps_to_kmph(wind_speed),1)} Km/h')
    descr_value.config(text=description)

    #muestra nombres de los días cubiertos por la predicción
    labels = [day1_label, day2_label, day3_label, day4_label, day5_label, day6_label, day7_label]
    current_date = datetime.now()
    # Configurar las etiquetas con los nombres de los días
    for i, label in enumerate(labels):
        # Configura el texto de cada etiqueta con el nombre del día
        label.config(text=(current_date + timedelta(days=i)).strftime('%A'))


    #muestra icono previsiones siguientes días
    labels = [day1_iconlabel, day2_iconlabel, day3_iconlabel, day4_iconlabel, day5_iconlabel, day6_iconlabel, day7_iconlabel]
    for i, label in enumerate(labels):
        imagen, temperature, humidity, pressure, wind_speed, description = dameElementosJSON(json_response, i)
        print(f"Día {i}:{imagen},{temperature}")
        img=Image.open(f"images/forecast_icons/{imagen}@2x.png")
        if i==0:
            resized_img=img
        else:
            resized_img=img.resize((50,50))
        day_imagen=ImageTk.PhotoImage(resized_img)
        # Configura el texto de cada etiqueta con el nombre del día
        label.config(image=day_imagen)
        label.image=day_imagen




root = tk.Tk()
root.title('Previsión del Tiempo')
#+300+300 indica la posición de la ventana en el momento de ser creada
root.geometry('890x470+300+300')
root.resizable(width=False, height=False)
root.configure(bg="#57adff")  # blue

# Icono (cuando se minimiza)
image_icon = tk.PhotoImage(file="images/logo.png")
root.iconphoto(False, image_icon)

current_weather_background = tk.PhotoImage(file="images/current_weather_background.png")
# ponemos la imagen en una label
current_weather_label =tk.Label(root, image=current_weather_background, bg="#57adff")
current_weather_label.place(x=30, y=110)

# labels sobre la label que representa el fondo azul
temp_title = tk.Label(root, text="Temperature", font=("Helvetica", 11), fg="white", bg="#203243")
temp_title.place(x=50, y=120)

temp_value=tk.Label(root,font=('Helvetica',11),fg="white",bg="#203243")
temp_value.place(x=130, y=120)

hum_title = tk.Label(root, text="Humidity", font=("Helvetica", 11), fg="white", bg="#203243")
hum_title.place(x=50, y=140)

hum_value=tk.Label(root,font=('Helvetica',11),fg="white",bg="#203243")
hum_value.place(x=130, y=140)

pres_title = tk.Label(root, text="Pressure", font=("Helvetica", 11), fg="white", bg="#203243")
pres_title.place(x=50, y=160)

pres_value=tk.Label(root,font=('Helvetica',11),fg="white",bg="#203243")
pres_value.place(x=130, y=160)

wind_title = tk.Label(root, text="Wind Speed", font=("Helvetica", 11), fg="white", bg="#203243")
wind_title.place(x=50, y=180)

wind_value=tk.Label(root,font=('Helvetica',11),fg="white",bg="#203243")
wind_value.place(x=130, y=180)

descr_title = tk.Label(root, text="Description", font=("Helvetica", 11), fg="white", bg="#203243")
descr_title.place(x=50, y=200)

descr_value=tk.Label(root,font=('Helvetica',10),fg="white",bg="#203243")
descr_value.place(x=130, y=200)



# search box
search_background = tk.PhotoImage(file="images/search_box_background.png")
busqueda_label = tk.Label(root, image=search_background, bg="#57adff")
busqueda_label.place(x=270, y=120)

imagen_nube = tk.PhotoImage(file="images/nubes.png")
weather_label = tk.Label(root, image=imagen_nube, bg="#203243")
weather_label.place(x=290, y=130)

ciudad_entry = tk.Entry(root, justify="center", width=15, font=("Poppins", 25, 'bold'), bg="#203243", border=0,
                        relief="flat", fg="white")
ciudad_entry.place(x=360, y=130)
ciudad_entry.focus()  # para escribir sin tener que seleccionar previamente

#Ojo: el command del botón va sin () (si no se llamaría directamente al método)
imagen_search = tk.PhotoImage(file="images/lupa.png")
search_button = tk.Button(root, command=getWeather, image=imagen_search, bg="#203243", cursor='hand2', borderwidth=0)
search_button.place(x=635, y=123)


# clock: here we will place time
clock_label = tk.Label(root, font=("Helvetica", 30, 'bold'), fg="white", bg="#57adff")
clock_label.place(x=30, y=20)

# timezone
timezone_label = tk.Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
timezone_label.place(x=700, y=20)

long_lat_label = tk.Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
long_lat_label.place(x=700, y=60)

# parte inferior de la pantalla: predicciones
marco_predicciones = tk.Frame(root, bg="#203243", width=900, height=180, relief="sunken")
marco_predicciones.pack(side=tk.BOTTOM)

current_day_background = tk.PhotoImage(file="images/current_day_background.png")
next_days_background = tk.PhotoImage(file="images/next_days_background.png")

tk.Label(marco_predicciones, image=current_day_background, bg="#212120").place(x=30, y=20)
tk.Label(marco_predicciones, image=next_days_background, bg="#212120").place(x=300, y=30)
tk.Label(marco_predicciones, image=next_days_background, bg="#212120").place(x=400, y=30)
tk.Label(marco_predicciones, image=next_days_background, bg="#212120").place(x=500, y=30)
tk.Label(marco_predicciones, image=next_days_background, bg="#212120").place(x=600, y=30)
tk.Label(marco_predicciones, image=next_days_background, bg="#212120").place(x=700, y=30)
tk.Label(marco_predicciones, image=next_days_background, bg="#212120").place(x=800, y=30)


#muestra previsiones del tiempo
#si pones en cada frame wl bg a white, verás que se posicionan justo encima de los recuadros de color
day1_frame=tk.Frame(root, width=230, height=132, bg="#282829")
day1_frame.place(x=35, y=315)

day1_label=tk.Label(day1_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day1_label.place(x=90,y=5)
day1_iconlabel=tk.Label(day1_frame,bg="#282829")
day1_iconlabel.place(x=60,y=25)


day2_frame=tk.Frame(root, width=70, height=115, bg="#282829")
day2_frame.place(x=305, y=325)

day2_label=tk.Label(day2_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day2_label.place(x=10,y=5)
day2_iconlabel=tk.Label(day2_frame,bg="#282829")
day2_iconlabel.place(x=7,y=20)

day3_frame=tk.Frame(root, width=70, height=115, bg="#282829")
day3_frame.place(x=405, y=325)

day3_label=tk.Label(day3_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day3_label.place(x=10,y=5)
day3_iconlabel=tk.Label(day3_frame,bg="#282829")
day3_iconlabel.place(x=7,y=20)

day4_frame=tk.Frame(root, width=70, height=115, bg="#282829")
day4_frame.place(x=505, y=325)

day4_label=tk.Label(day4_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day4_label.place(x=10,y=5)
day4_iconlabel=tk.Label(day4_frame,bg="#282829")
day4_iconlabel.place(x=7,y=20)

day5_frame=tk.Frame(root, width=70, height=115, bg="#282829")
day5_frame.place(x=605, y=325)

day5_label=tk.Label(day5_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day5_label.place(x=10,y=5)
day5_iconlabel=tk.Label(day5_frame,bg="#282829")
day5_iconlabel.place(x=7,y=20)

day6_frame=tk.Frame(root, width=70, height=115, bg="#282829")
day6_frame.place(x=705, y=325)

day6_label=tk.Label(day6_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day6_label.place(x=10,y=5)
day6_iconlabel=tk.Label(day6_frame,bg="#282829")
day6_iconlabel.place(x=7,y=20)

day7_frame=tk.Frame(root, width=70, height=115, bg="#282829")
day7_frame.place(x=805, y=325)

day7_label=tk.Label(day7_frame,font=("Arial", 11), bg="#282829",fg="#fff")
day7_label.place(x=10,y=5)
day7_iconlabel=tk.Label(day7_frame,bg="#282829")
day7_iconlabel.place(x=7,y=20)

tk.mainloop()
