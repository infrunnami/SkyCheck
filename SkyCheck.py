import requests 
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os 
import geocoder
from datetime import datetime
import time
from PIL import Image

# -------------------------------- funciones --------------------------------


def cambiar_frame(frame):
    frame_inicio.pack_forget()
    frame_final.pack_forget()
    frame.pack(fill="both", expand=True)

def ubicacion():
    try:
        g = geocoder.ip("me")
        city = g.city if g and g.ok else "Ubicación no disponible"
    except Exception:
        city = "Error al obtener ubicación"
    
    entry.configure(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, city)
    entry.configure(state="disabled")

def habilitar_entry():
    entry.configure(state="normal")
    entry.delete(0, tk.END)

def consultar():
    # -------------------------------- INSERTAR API KEY --------------------------------
    API_KEY = "<api key acá>"
    CITY = entry.get().strip()

    if not CITY:
        messagebox.showwarning("Atención", "Por favor, ingresa una ciudad válida.")
        return
            
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&lang=es"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        mostrar_resultados(datos)
        cambiar_frame(frame_final)
        entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", f"No se pudo obtener el clima de {CITY}")

def is_day():
    hora_actual = datetime.now().hour
    return 6 <= hora_actual < 18

def mostrar_resultados(datos):

    #descripcion
    ciudad = datos["location"]["name"]
    region = datos["location"]["region"]
    temp_c = datos["current"]["temp_c"]
    desc = datos["current"]["condition"]["text"]
    max_temp = datos["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
    min_temp = datos["forecast"]["forecastday"][0]["day"]["mintemp_c"]
    feelslike = datos["current"]["feelslike_c"]
    horas = datos["current"]["last_updated"].split()[0]   
    tiempo = time.strftime('%H:%M')



    max_region = 20
    if len(region) > max_region:
        region = f"\n{region}"
        label_desc.configure(font=("Arial", 14))
    else:
        label_desc.configure(font=("Arial", 18))

    label_desc.configure(text=f"{ciudad}, {region} 📍\n{temp_c}°C | {desc}\n"f"Máx: {max_temp}°C / Mín: {min_temp}°C" f"\nSensación: {feelslike}°C \nFecha: {horas} | {tiempo}")


    #datos
    uv = datos["current"]["uv"]
    humedad = datos["current"]["humidity"]
    viento = datos["current"]["wind_kph"]
    Visibilidad = datos["current"]["vis_km"]
    Amanecer = datos["forecast"]["forecastday"][0]["astro"]["sunrise"]
    Atardecer = datos["forecast"]["forecastday"][0]["astro"]["sunset"]
    
    label_datos.configure(text=f"Índice UV: {uv}" f"\nHumedad: {humedad}%" f"\nViento: {viento}(km/h)" f"\nVisibilidad: {Visibilidad}(km)" f"\nAmanecer: {Amanecer}" f"\nAtardecer: {Atardecer}")


    #horas
    hora_actual = time.strftime('%H:%M')
    horas_texto = ""
    for hora in datos["forecast"]["forecastday"][0]["hour"]:
        time_string = hora["time"].split(" ")[1]
        temperatura = hora["temp_c"]
        condicion = hora["condition"]["text"]

        if time_string[:2] == hora_actual[:2]:
            horas_texto += f"➡ {time_string} - {condicion}, {temperatura}°C\n"
        else:
            horas_texto += f"{time_string} - {condicion}, {temperatura}°C\n"
    
    label_horas.configure(text=horas_texto)

def centrar_ventana():
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla - 800) // 2
    y = (alto_pantalla - 700) // 2
    root.geometry(f"800x700+{x}+{y}")


# -------------------------------- crear ventana --------------------------------


ctk.set_appearance_mode("System")  

imagenes = r"C:\Users\corre\OneDrive\Escritorio\DetectorClima\imagenes"
root = ctk.CTk() 
root.title("SkyCheck")
root.iconbitmap(os.path.join(imagenes, "LogoClima.ico"))
root.geometry("800x700")
root.resizable(False, False)

if is_day():
    logo_path = os.path.join(imagenes, "LogoDia.png")
    ctk.set_default_color_theme(r"C:\Users\corre\OneDrive\Escritorio\DetectorClima\temas\GhostTrain.json")
else:
    logo_path = os.path.join(imagenes, "LogoNoche.png")
    ctk.set_default_color_theme(r"C:\Users\corre\OneDrive\Escritorio\DetectorClima\temas\NightTrain.json")
#GhostTrains - dia
#NightTrain - noche

centrar_ventana()

# -------------------------------- frame inicio --------------------------------

frame_inicio = ctk.CTkFrame(master=root)

logo = ctk.CTkImage(Image.open(logo_path), size=(250, 250))
label_logo = ctk.CTkLabel(frame_inicio, image=logo, text="")
label_logo.place(relx = 0.5, rely = 0.25, anchor = tk.CENTER)

frame_botones = ctk.CTkFrame(frame_inicio, corner_radius=16)
frame_botones.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

label1 = ctk.CTkLabel(frame_botones, text="Ingrese su Ciudad", font=("Arial", 20, "bold"))
label1.pack(pady=20)
    
entry = ctk.CTkEntry(frame_botones, width=300)
entry.pack(pady=10)
ubicacion()

btn_buscar = ctk.CTkButton(frame_botones, text="Buscar Clima", command=consultar, corner_radius=32)
btn_buscar.pack(side="left", padx=10, pady=10)

btn_ubicacion = ctk.CTkButton(frame_botones, text="Ingreso Manual", command=habilitar_entry, corner_radius=32)
btn_ubicacion.pack(side="left", padx=10, pady=10)


# -------------------------------- frame final --------------------------------


frame_final = ctk.CTkFrame(master=root)


#izquierda
frame_izquierda = ctk.CTkFrame(frame_final)
frame_izquierda.place(relx=0, rely=0, relwidth=0.5, relheight=1)

frame_descripcion = ctk.CTkFrame(frame_izquierda, corner_radius=16)
frame_descripcion.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER, relwidth=0.8, relheight=0.3)

label_desc = ctk.CTkLabel(frame_descripcion, text="", font=("Arial", 18, "bold"), anchor="center", justify="center")
label_desc.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

frame_datos = ctk.CTkFrame(frame_izquierda, corner_radius=16)
frame_datos.place(relx = 0.5, rely = 0.7, anchor = tk.CENTER, relwidth=0.8, relheight=0.3)

label_datos = ctk.CTkLabel(frame_datos, text="", font=("Arial", 18, "bold"), anchor="center", justify="center")
label_datos.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)


#derecha
frame_derecha = ctk.CTkFrame(frame_final)
frame_derecha.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

frame_cont_r = ctk.CTkFrame(frame_derecha, corner_radius=16)
frame_cont_r.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER, relwidth=0.8, relheight=0.8)

frame_horas = ctk.CTkFrame(frame_cont_r, corner_radius=16)
frame_horas.place(relx = 0.5, rely = 0.45, anchor = tk.CENTER, relwidth=0.8, relheight=0.8)

label_horas = ctk.CTkLabel(frame_horas, text="", font=("Arial", 13), anchor="center", justify="center")
label_horas.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

btn_volver = ctk.CTkButton(frame_cont_r, text="⬅ Volver", command=lambda : cambiar_frame(frame_inicio))
btn_volver.place(relx = 0.5, rely = 0.92, anchor = tk.CENTER)
    




frame_inicio.pack(fill="both", expand=True)
root.mainloop()