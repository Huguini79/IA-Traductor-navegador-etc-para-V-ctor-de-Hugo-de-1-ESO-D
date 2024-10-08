import requests
from bs4 import BeautifulSoup
import urllib.parse
from googletrans import Translator
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import pygame
from moviepy.editor import VideoFileClip
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl 
import random
from tkinter import simpledialog
import turtle
import os
import pickle


with open('tareas.txt', 'w') as archivo:
    
    archivo.write('Tareas:\n')


def traductor(texto, idioma_destino='en'):
    
        # Crear una instancia del traductor
        traductor = Translator()
        
        # Traducir el texto
        traduccion = traductor.translate(texto, dest=idioma_destino)
        
        return traduccion.text


def traductor2(texto, idioma_destino='es'):
    
        # Crear una instancia del traductor
        traductor = Translator()
        
        # Traducir el texto
        traduccion = traductor.translate(texto, dest=idioma_destino)
        
        return traduccion.text

def ia():

    def buscar_en_wikipedia(query):
        
        url = f"https://es.wikipedia.org/w/index.php?search={urllib.parse.quote(query)}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            primer_parrafo = soup.find('p')
            if primer_parrafo:
                return primer_parrafo.get_text()
            else:
                return "No se encontró información en Wikipedia."
        else:
            return "Error al acceder a Wikipedia."


    def buscar_en_google(query):
        
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            resultados = []
            for item in soup.find_all('h3'):
                resultados.append(item.get_text())
            if resultados:
                return "\n".join(resultados[:5])  # Devuelve los 5 primeros resultados
            else:
                return "No se encontraron resultados en Google."
        else:
            return "Error al acceder a Google."


    def buscar_en_duckduckgo(query):
        
        url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            resultados = []
            for item in soup.find_all('a', class_='result__link'):
                resultados.append(item.get_text())
            if resultados:
                return "\n".join(resultados[:5])  # Devuelve los 5 primeros resultados
            else:
                return "No se encontraron resultados en DuckDuckGo."
        else:
            return "Error al acceder a DuckDuckGo."


    def buscar_en_otros_lugares(query):
        
        urls = {
            "Google Académico": f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}",
            "Medline Plus": f"https://medlineplus.gov/search/search_result.html?query={urllib.parse.quote(query)}",
            "Archive.org": f"https://archive.org/search.php?query={urllib.parse.quote(query)}",
            "Quora": f"https://www.quora.com/search?q={urllib.parse.quote(query)}",
            "Cision Haro": f"https://www.cision.com/us/harotips/?s={urllib.parse.quote(query)}",
            "Wolfram Alpha": f"https://www.wolframalpha.com/input/?i={urllib.parse.quote(query)}",  # Para resolver matemáticas
            "Encyclopedia": f"https://www.encyclopedia.com/search?query={urllib.parse.quote(query)}",
            "Famous Birthdays": f"https://www.famousbirthdays.com/search?q={urllib.parse.quote(query)}",  # Para youtubers y celebridades
            "Mathway": f"https://www.mathway.com/Calculator/{urllib.parse.quote(query)}",  # Para matemáticas
            "GeoNames": f"https://www.geonames.org/search.html?q={urllib.parse.quote(query)}",  # Para geografía
            "Billboard": f"https://www.billboard.com/search/results/?q={urllib.parse.quote(query)}",  # Para músicos y cantantes
            "DJ Mag": f"https://djmag.com/top100djs/results?search={urllib.parse.quote(query)}",  # Para DJs
            "Biography": f"https://www.biography.com/search?q={urllib.parse.quote(query)}",  # Para biografías de personas famosas
            "GitHub": f"https://github.com/search?q={urllib.parse.quote(query)}",  # Para buscar en GitHub
            "Stack Overflow": f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}",  # Para buscar en Stack Overflow
            "W3Schools": f"https://www.w3schools.com/search/search.asp?q={urllib.parse.quote(query)}",  # Para tutoriales de programación
        }
        
        
        resultados = []
        
        
        for nombre, url in urls.items():
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if nombre == "Google Académico":
                    item = soup.find('h3')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "Medline Plus":
                    item = soup.find('div', class_='result')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "Quora":
                    item = soup.find('a', class_='q-box qu-mb--tiny')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "Wolfram Alpha":
                    resultados.append(f"{nombre}: {url}")  # URL porque Wolfram Alpha generalmente devuelve respuestas directas
                elif nombre == "Famous Birthdays":
                    item = soup.find('div', class_='bio')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "Mathway":
                    resultados.append(f"{nombre}: {url}")  # Solo se devuelve la URL
                elif nombre == "GeoNames":
                    item = soup.find('a', class_='result')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "Billboard":
                    item = soup.find('h3')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "DJ Mag":
                    item = soup.find('div', class_='top100dj-item-title')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                elif nombre == "Biography":
                    item = soup.find('h1')
                    if item:
                        resultados.append(f"{nombre}: {item.get_text()}")
                else:
                    resultados.append(f"{nombre}: {url}")  # Muestra la URL para que el usuario pueda ver el resultado
            else:
                resultados.append(f"Error al acceder a {nombre}.")
        
        if resultados:
            return "\n".join(resultados)
        else:
            return "No se encontró información en otras fuentes."


    def buscar_info(query):
        resultado_wikipedia = buscar_en_wikipedia(query)
        
        if "No se encontró información" in resultado_wikipedia:
            resultado_google = buscar_en_google(query)
            if "No se encontraron resultados" in resultado_google:
                resultado_duckduckgo = buscar_en_duckduckgo(query)
                if "No se encontraron resultados" in resultado_duckduckgo:
                    resultado_otros = buscar_en_otros_lugares(query)
                    return resultado_otros
                return resultado_duckduckgo
            return resultado_google
        
        return resultado_wikipedia


    def agregar_label(frame_contenido, texto):
        
        nuevo_label = tk.Label(frame_contenido, text=texto, font=("Arial", 12))
        nuevo_label.pack(pady=5)


    def enviar():
        # Definir la ventana secundaria primero
        root2 = tk.Toplevel(root)  # Cambié a Toplevel para que sea una ventana hija de la principal
        root2.configure(bg='yellow')
        root2.geometry('660x550')

        # Canvas y scrollbars para la nueva ventana desplazable
        canvas = tk.Canvas(root2)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar_y = tk.Scrollbar(root2, orient="vertical", command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal
        scrollbar_x = tk.Scrollbar(root2, orient="horizontal", command=canvas.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Crear el frame dentro del canvas
        frame_contenido = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")

        # Configurar el scroll para que funcione tanto en X como en Y
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Buscar la información y agregar el label
        resultado = buscar_info(texto.get('1.0', 'end-1c'))
        agregar_label(frame_contenido, f'Respuesta: {resultado}')

    root = tk.Tk()
    root.configure(bg='yellow')
    root.geometry('660x550')

    label = tk.Label(root, text='Introduce lo que quieras buscar:', wraplength=1000)
    texto = tk.Text(root, height='2', width='50')
    botónenvi = tk.Button(root, text='Enviar mensaje', height='2', width='50', command=enviar)


    label.grid(row=0, column=0, padx=10, pady=10)
    texto.grid(row=1, column=0, padx=10, pady=10)
    botónenvi.grid(row=2, column=0, padx=10, pady=10)


    root.mainloop()


def enviar1():
    
    def envitraduct():
    
        idioma_destino = 'en'
        traducción = traductor(textoo.get('1.0', 'end-1c'), idioma_destino)
        messagebox.showinfo('Mensaje', f'Mensaje traducido: {traducción}')
        
    rootraductor = tk.Tk()
    rootraductor.configure(bg='yellow')
    rootraductor.geometry('660x550')
    labell = tk.Label(rootraductor, text='Introduce tu palabra/frase para traducir del español al inglés', wraplength=1000)
    textoo = tk.Text(rootraductor, height='2', width='60')
    botóntraduct = tk.Button(rootraductor, text='Enviar', height='2', width='10', command=envitraduct)
    labell.grid(row=0, column=0, padx=10, pady=10)
    textoo.grid(row=1, column=0, padx=10, pady=10)
    botóntraduct.grid(row=2, column=0, padx=10, pady=10)
    
    rootraductor.mainloop()


def enviar2():
    
    def envitraduct2():
    
        idioma_destino = 'es'
        traducción2 = traductor2(textooo.get('1.0', 'end-1c'), idioma_destino)
        messagebox.showinfo('Mensaje', f'Mensaje traducido: {traducción2}')
        
    rootraductor2 = tk.Tk()
    rootraductor2.configure(bg='yellow')
    rootraductor2.geometry('660x550')
    labelll = tk.Label(rootraductor2, text='Introduce tu palabra/frase para traducir del inglés al español', wraplength=1000)
    textooo = tk.Text(rootraductor2, height='2', width='60')
    botóntraduct2 = tk.Button(rootraductor2, text='Enviar', height='2', width='10', command=envitraduct2)
    labelll.grid(row=0, column=0, padx=10, pady=10)
    textooo.grid(row=1, column=0, padx=10, pady=10)
    botóntraduct2.grid(row=2, column=0, padx=10, pady=10)
    rootraductor2.mainloop()


def obtener_chiste():
    
    response = requests.get("https://v2.jokeapi.dev/joke/Any?lang=es")
    
    if response.status_code == 200:
        joke = response.json()
        
        if joke['type'] == 'single':
            return joke['joke']
        else:
            return f"{joke['setup']} - {joke['delivery']}"
    else:
        return "No se pudo obtener un chiste."

def chistes():
    
    joke = obtener_chiste()  # Fetch the joke
    messagebox.showinfo('Chistes', f'Chiste: {joke}')


def gatos():
    
    response = requests.get("https://catfact.ninja/fact")
    cat_fact = response.json()['fact']
    idioma_destino = 'es'
    traduccióngat = traductor2(cat_fact, idioma_destino)
    messagebox.showinfo('Datos curiosos de gatos', f"Dato curiosos sobre gatos: {traduccióngat}")


def obtener_imagen_perro():
    # Obtener una imagen aleatoria de un perro
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    dog_image_url = response.json()['message']
    return dog_image_url

def mostrar_imagen():
    # Obtener la URL de la imagen del perro
    url = obtener_imagen_perro()
    
    # Solicitar la imagen
    response = requests.get(url)
    
    # Abrir la imagen
    img_data = response.content
    image = Image.open(BytesIO(img_data))

    # Crear una ventana
    ventana = tk.Toplevel()  # Cambiar a Toplevel para no bloquear la ventana principal
    ventana.title("Imagen de Perro")

    # Convertir la imagen a un formato que tkinter pueda usar
    img = ImageTk.PhotoImage(image)
    
    # Crear un Label para mostrar la imagen
    label = tk.Label(ventana, image=img)
    label.image = img  # Guardar la referencia de la imagen en el label
    label.pack()

    # Mostrar la ventana
    ventana.mainloop()





def super_mario():
    # Inicializa Pygame
    pygame.init()

    # Dimensiones de la ventana
    WIDTH, HEIGHT = 800, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Super Mario Clone")

    # Colores
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BROWN = (139, 69, 19)

    # Configuraciones del personaje
    character_x = 100
    character_y = 500
    character_width = 50
    character_height = 50
    character_velocity = 5
    is_jumping = False
    jump_count = 10

    # Bucle principal del juego
    run = True
    while run:
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and character_x > character_velocity:
            character_x -= character_velocity
        if keys[pygame.K_RIGHT] and character_x < WIDTH - character_width - character_velocity:
            character_x += character_velocity
        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                character_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Dibuja el fondo (verde) y el personaje (azul)
        window.fill(GREEN)  # Fondo verde
        pygame.draw.rect(window, BLUE, (character_x, character_y, character_width, character_height))  # Personaje azul

        # Dibuja el suelo (marrón)
        pygame.draw.rect(window, BROWN, (0, HEIGHT - 50, WIDTH, 50))  # Suelo marrón

        pygame.display.update()

    pygame.quit()


def pájaro_loco():
    video_path = "El Pájaro Loco en Español _ Fabricante de dolor _ Compilación de 1 Hora _ Dibujos Animados.mp4"
    clip = VideoFileClip(video_path)
    
    clip.preview()




def reloj():
    def actualizar_reloj():
        # Obtiene la hora actual
        hora_actual = time.strftime("%H:%M:%S")
        # Actualiza la etiqueta con la hora actual
        etiqueta.config(text=hora_actual)
        # Llama a esta función de nuevo después de 1000 ms (1 segundo)
        ventanaa.after(1000, actualizar_reloj)

    # Crea la ventana principal
    ventanaa = tk.Tk()
    ventanaa.title("Reloj Digital")

    # Crea una etiqueta para mostrar la hora
    etiqueta = tk.Label(ventanaa, font=("Helvetica", 48), fg="black")
    etiqueta.pack(pady=20)

    # Llama a la función para actualizar el reloj por primera vez
    actualizar_reloj()

    # Inicia el bucle de la interfaz
    ventanaa.mainloop()

def navegador():
    class Navegador(QMainWindow):
        def __init__(self):
            super(Navegador, self).__init__()

            # Inicializa el navegador
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl("http://www.google.com"))  # Página de inicio
            self.setCentralWidget(self.browser)

            # Barra de herramientas
            self.barra_de_herramientas = QToolBar()
            self.addToolBar(self.barra_de_herramientas)

            # Botón de "Atrás"
            self.boton_atras = QAction("Atrás", self)
            self.boton_atras.triggered.connect(self.browser.back)
            self.barra_de_herramientas.addAction(self.boton_atras)

            # Botón de "Adelante"
            self.boton_adelante = QAction("Adelante", self)
            self.boton_adelante.triggered.connect(self.browser.forward)
            self.barra_de_herramientas.addAction(self.boton_adelante)

            # Botón de "Recargar"
            self.boton_recargar = QAction("Recargar", self)
            self.boton_recargar.triggered.connect(self.browser.reload)
            self.barra_de_herramientas.addAction(self.boton_recargar)

            # Barra de URL
            self.barra_url = QLineEdit()
            self.barra_url.returnPressed.connect(self.navegar_a_url)
            self.barra_de_herramientas.addWidget(self.barra_url)

            # Conectar la barra de URL a la URL del navegador
            self.browser.urlChanged.connect(self.actualizar_barra_url)

            # Configurar la ventana principal
            self.setWindowTitle("Navegador Simple")
            self.setGeometry(100, 100, 1200, 800)
            self.show()

        def navegar_a_url(self):
            url = self.barra_url.text()
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url
            self.browser.setUrl(QUrl(url))  # Usar QUrl aquí

        def actualizar_barra_url(self, q):
            self.barra_url.setText(q.toString())
    app = QApplication(sys.argv)
    navegador = Navegador()
    sys.exit(app.exec_())

lista = ['4', '2', '8', '5']

def adivinanzas():
    
    entrada = simpledialog.askstring('Adivina', f'Adivina entre estos números: {lista}')
    pal_ale = random.choice(lista)
    if entrada == pal_ale:
        messagebox.showinfo('Mensaje', 'Los dos hemos adivinado lo mismo.')
    else:
        messagebox.showinfo('Mensaje', f'Los dos no hemos adivinado lo mismo: yo he pensado: {pal_ale} y tú: {entrada}')


def tturtle():
    
    # Configuración inicial
    t = turtle.Turtle()
    t.speed(10)  # Ajusta la velocidad del dibujo

    # Dibuja círculos girando
    for i in range(36):  # 36 círculos para completar un giro
        t.circle(50)  # Dibuja un círculo de radio 50
        t.right(10)   # Gira 10 grados a la derecha

    # Finaliza
    turtle.done()


def calculadora():
    
    def agregar_7():
        entrada.insert(tk.END, '7')

    def agregar_8():
        entrada.insert(tk.END, '8')

    def agregar_9():
        entrada.insert(tk.END, '9')

    def agregar_4():
        entrada.insert(tk.END, '4')

    def agregar_5():
        entrada.insert(tk.END, '5')

    def agregar_6():
        entrada.insert(tk.END, '6')

    def agregar_1():
        entrada.insert(tk.END, '1')

    def agregar_2():
        entrada.insert(tk.END, '2')

    def agregar_3():
        entrada.insert(tk.END, '3')

    def agregar_0():
        entrada.insert(tk.END, '0')

    def agregar_suma():
        entrada.insert(tk.END, '+')

    def agregar_resta():
        entrada.insert(tk.END, '-')

    def agregar_multiplicacion():
        entrada.insert(tk.END, '*')

    def agregar_division():
        entrada.insert(tk.END, '/')
        
    def calcular():
        try:
            resultado = eval(entrada.get())
            entrada.delete(0, tk.END)
            entrada.insert(tk.END, str(resultado))
        except:
            entrada.delete(0, tk.END)
            entrada.insert(tk.END, 'Error')
    
    def limpiar_entrada():
        entrada.delete(0, tk.END)
    
    ventana = tk.Tk()
    ventana.configure(bg='yellow')
    ventana.geometry('660x550')
    
    entrada = tk.Entry(ventana, width=16, font=("Arial", 24))
    entrada.grid(row=0, column=0, columnspan=4)
    
    # Crear los botones
    tk.Button(ventana, text='7', width=5, height=2, command=agregar_7).grid(row=1, column=0)
    tk.Button(ventana, text='8', width=5, height=2, command=agregar_8).grid(row=1, column=1)
    tk.Button(ventana, text='9', width=5, height=2, command=agregar_9).grid(row=1, column=2)
    tk.Button(ventana, text='/', width=5, height=2, command=agregar_division).grid(row=1, column=3)

    tk.Button(ventana, text='4', width=5, height=2, command=agregar_4).grid(row=2, column=0)
    tk.Button(ventana, text='5', width=5, height=2, command=agregar_5).grid(row=2, column=1)
    tk.Button(ventana, text='6', width=5, height=2, command=agregar_6).grid(row=2, column=2)
    tk.Button(ventana, text='*', width=5, height=2, command=agregar_multiplicacion).grid(row=2, column=3)

    tk.Button(ventana, text='1', width=5, height=2, command=agregar_1).grid(row=3, column=0)
    tk.Button(ventana, text='2', width=5, height=2, command=agregar_2).grid(row=3, column=1)
    tk.Button(ventana, text='3', width=5, height=2, command=agregar_3).grid(row=3, column=2)
    tk.Button(ventana, text='-', width=5, height=2, command=agregar_resta).grid(row=3, column=3)

    tk.Button(ventana, text='C', width=5, height=2, command=limpiar_entrada).grid(row=4, column=0)
    tk.Button(ventana, text='0', width=5, height=2, command=agregar_0).grid(row=4, column=1)
    tk.Button(ventana, text='=', width=5, height=2, command=calcular).grid(row=4, column=2)
    tk.Button(ventana, text='+', width=5, height=2, command=agregar_suma).grid(row=4, column=3)

    # Iniciar el bucle de la interfaz gráfica
    ventana.mainloop()


# Nombre del archivo donde se guardan las tareas
NOMBRE_ARCHIVO = 'tareas.bin'

def gestr():
    def cargar_tareas():
        """Carga las tareas del archivo binario al iniciar el programa."""
        if os.path.exists(NOMBRE_ARCHIVO):  # Verifica si el archivo existe
            with open(NOMBRE_ARCHIVO, 'rb') as archivo:
                try:
                    return pickle.load(archivo)  # Cargar las tareas usando pickle
                except EOFError:  # Manejo de archivo vacío
                    return []
        return []

    def guardar_tareas(tareas):
        """Guarda las tareas en un archivo binario."""
        with open(NOMBRE_ARCHIVO, 'wb') as archivo:
            pickle.dump(tareas, archivo)

    def agregar_tarea():
        """Agrega una tarea a la lista y la guarda en el archivo."""
        tarea = simpledialog.askstring("Agregar tarea", "¿Qué tarea quieres agregar?")
        if tarea:  # Verifica que la tarea no esté vacía
            tareas.append(tarea)  # Añadir la tarea a la lista
            guardar_tareas(tareas)  # Guardar la lista actualizada

    def quitar_tarea():
        """Elimina una tarea de la lista."""
        tarea = simpledialog.askstring("Eliminar tarea", "¿Qué tarea quieres eliminar?")
        if tarea in tareas:
            tareas.remove(tarea)  # Eliminar la tarea de la lista
            guardar_tareas(tareas)  # Guardar la lista actualizada
        else:
            messagebox.showerror("Error", "La tarea no existe.")  # Muestra un error si la tarea no está

    def ver_tareas():
        """Muestra las tareas en un messagebox."""
        if tareas:
            messagebox.showinfo("Lista de Tareas", "\n".join(tareas))  # Muestra las tareas en un messagebox
        else:
            messagebox.showinfo("Lista de Tareas", "No hay tareas.")  # Mensaje si no hay tareas

    # Cargar tareas desde el archivo
    tareas = cargar_tareas()

    # Crear la ventana principal
    rootar = tk.Tk()
    rootar.title("Gestor de Tareas")
    rootar.configure(bg='yellow')
    rootar.geometry('660x550')

    botonagreg = tk.Button(rootar, text='Agregar tarea', height='2', width='15', command=agregar_tarea)
    botonagreg.pack(pady=5)

    botonelim = tk.Button(rootar, text='Quitar tarea', height='2', width='15', command=quitar_tarea)
    botonelim.pack(pady=5)

    botonver = tk.Button(rootar, text='Ver tareas', height='2', width='15', command=ver_tareas)
    botonver.pack(pady=5)

    # Al cerrar la ventana, vaciar el archivo
    def cerrar():
        open(NOMBRE_ARCHIVO, 'wb').close()  # Vaciar el archivo al cerrar
        rootar.destroy()  # Cerrar la ventana


    rootar.mainloop()  # Iniciar el bucle de la ventana principal


def segunda_parte_del_programa():
    
    rootsegun = tk.Tk()
    rootsegun.configure(bg='yellow')
    rootsegun.geometry('660x550')
    
    botónprin11 = tk.Button(rootsegun, text='Adivinanzas', height='2', width='10', command=adivinanzas)
    botónprin12 = tk.Button(rootsegun, text='Gráficos', height='2', width='10', command=tturtle)
    botónprin13 = tk.Button(rootsegun, text='Calculadora', height='2', width='10', command=calculadora)
    botónprin14 = tk.Button(rootsegun, text='Gestor de tareas', height='2', width='60', command=gestr)
    
    botónprin11.grid(row=0, column=0, padx=10, pady=10)
    botónprin12.grid(row=1, column=0, padx=10, pady=10)
    botónprin13.grid(row=2, column=0, padx=10, pady=10)
    botónprin14.grid(row=3, column=0, padx=10, pady=10)
    
    rootsegun.mainloop()



rootprin = tk.Tk()
rootprin.configure(bg='yellow')
rootprin.geometry('660x550')

botónprin = tk.Button(rootprin, text='Inteligencia artificial', height='2', width='60', command=ia)
botón2prin = tk.Button(rootprin, text='Navegador casero', height='2', width='45', command=navegador)
botónprin2 = tk.Button(rootprin, text='Traductor del español al inglés', height='2', width='60', command=enviar1)
botónprin3 = tk.Button(rootprin, text='Traductor del inglés al español', height='2', width='60', command=enviar2)
botónprin4 = tk.Button(rootprin, text='Chistes', height='2', width='10', command=chistes)
botónprin5 = tk.Button(rootprin, text='Datos curiosos sobre gatos', height='2', width='60', command=gatos)
botónprin6 = tk.Button(rootprin, text='Imágenes aleatorias de Perros', height='2', width='60', command=mostrar_imagen)
botónprin8 = tk.Button(rootprin, text='Super Mario Bros Juego', height='2', width='60', command=super_mario)
botónprin9 = tk.Button(rootprin, text='Pájaro loco 1 hora episodios', height='2', width='60', command=pájaro_loco)
botónprin10 = tk.Button(rootprin, text='Reloj', height='2', width='10', command=reloj)
botónsegundo = tk.Button(rootprin, text='Segunda parte del programa', height='2', width='60', command=segunda_parte_del_programa)

botónprin.grid(row=0, column=0, padx=10, pady=10)
botón2prin.grid(row=1, column=0, padx=10, pady=10)
botónprin2.grid(row=2, column=0, padx=10, pady=10)
botónprin3.grid(row=3, column=0, padx=10, pady=10)
botónprin4.grid(row=4, column=0, padx=10, pady=10)
botónprin5.grid(row=5, column=0, padx=10, pady=10)
botónprin6.grid(row=6, column=0, padx=10, pady=10)
botónprin8.grid(row=8, column=0, padx=10, pady=10)
botónprin9.grid(row=9, column=0, padx=10, pady=10)
botónprin10.grid(row=10, column=0, padx=10, pady=10)
botónsegundo.grid(row=11, column=0, padx=10, pady=10)

rootprin.mainloop()