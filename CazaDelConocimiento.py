import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk

class VentanaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.centrar_ventana(600, 400)
        self.configure(bg="#f0f0f0")
        self.bg_image = Image.open("luffy.jpg")
        self.bg_image = self.bg_image.resize((600, 400))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.parent = parent

        self.label = tk.Label(self, text="Ingrese su nombre de usuario:", font=("Arial", 18, "bold"), bg="#E71D36", fg="white")
        self.entry = tk.Entry(self, font=("Arial", 18), justify="center", bd=1, relief="solid")
        self.button_entrar = tk.Button(self, text="Entrar", font=("Arial", 18, "bold"), bg="#FF0000", fg="white", activeforeground="#CF9D60", command=self.guardar_usuario)

        self.canvas.create_window(300, 100, window=self.label)
        self.canvas.create_window(300, 160, window=self.entry)
        self.canvas.create_window(300, 220, window=self.button_entrar)

        self.grab_set()

    def guardar_usuario(self):
        usuario = self.entry.get()
        if usuario:
            with open("usuarios.txt", "a", encoding='utf-8') as file:
                file.write(usuario + "\n")
            self.parent.deiconify()
            self.destroy()
        else:
            self.label.config(text="Por favor, ingrese un nombre de usuario", fg="white")

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f'{ancho}x{alto}+{x}+{y}')


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caza del Conocimiento")
        self.centrar_ventana(1280, 720)
        self.configure(bg="#f0f0f0")
        self.preguntas_mostradas = []
        self.lista = self.leer_preguntas()
        self.lista_original = list(self.lista)
        self.crear_interfaz()
        self.preguntas_respondidas = 0
        self.respu_corre = 0
        self.max_preguntas = 10

        self.withdraw()
        VentanaLogin(self)

    def crear_interfaz(self):
        self.canvas = tk.Canvas(self, width=1280, height=720)
        self.canvas.pack(fill="both", expand=True)

        self.img_fondo = Image.open("luffy1.jpg")
        self.img_fondo = self.img_fondo.resize((1280, 720))
        self.img_fondo_tk = ImageTk.PhotoImage(self.img_fondo)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_fondo_tk)

        tk.Label(self.canvas, text="¡Bienvenido al juego! \n \n Caza del Conocimiento", font=("Arial", 20, "bold"), bg="#E71D36", fg="white").pack(pady=100)
        tk.Button(self.canvas, text="INICIAR", font=("Arial", 18, "bold"), height=2, width=15, bg="#E71D36", activeforeground="#CF9D60", fg="white", command=self.start_action, relief=tk.FLAT, bd=10).pack(pady=20)
        tk.Button(self.canvas, text="RANKING", font=("Arial", 18, "bold"), height=2, width=15, bg="#0A3F84", activeforeground="#221D28", fg="white", command=self.mostrar_ranking, relief=tk.FLAT, bd=10).pack(pady=20)
        tk.Button(self.canvas, text="SALIR", font=("Arial", 18, "bold"), height=2, width=15, bg="#CF9D60", activeforeground="#E71D36", fg="white", command=self.salir, relief=tk.FLAT, bd=10).pack(pady=20) 

    def mostrar_ranking(self):
        VentanaRanking(self)

    def obtener_pregunta(self):
        if self.preguntas_respondidas >= self.max_preguntas+1:
            self.guardar_puntuacion()
            self.mostrar_mensaje_final("Fin del juego", "¡Has respondido todas las preguntas disponibles! \n \n El número de respuestas correctas es: {} \n \n Tu puntuación es: {} \n \n¡Gracias por jugar!".format(self.respu_corre, self.respu_corre * 100))
            return None

        preguntas_disponibles = [pregunta for pregunta in self.lista if pregunta not in self.preguntas_mostradas]
        pregunta = random.choice(preguntas_disponibles)
        self.preguntas_mostradas.append(pregunta)
        self.lista.remove(pregunta)
        return pregunta

    def leer_preguntas(self):
        try:
            with open("preguntas.txt", "r", encoding='utf-8') as file:
                lista = file.read()
                preguntas = lista.split("\n")
                lista = [pregunta.split(",") for pregunta in preguntas if pregunta]
            return lista
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo de preguntas no se encontró.")
            return []

    def comprobar_respuesta(self, respuesta, botones):
        pregunta_actual = self.new_window.pregunta_actual
        if respuesta == "A":
            respuesta = pregunta_actual[1]
        elif respuesta == "B":
            respuesta = pregunta_actual[2]
        elif respuesta == "C":
            respuesta = pregunta_actual[3]
        elif respuesta == "D":
            respuesta = pregunta_actual[4]
        for boton in botones:
            boton.config(state=tk.DISABLED)
        correcta = self.obtener_respuesta_correcta()
        if respuesta == correcta:
            salida = "¡Correcto! \n  \n La opción {} es la respuesta correcta.".format(correcta)
            self.respu_corre += 1
            self.mostrar_mensaje("Resultado", salida)
        else:
            salida = "Respuesta incorrecta. \n \n  La opción correcta era: {}.".format(correcta)
            self.mostrar_mensaje("Resultado", salida)

    def obtener_respuesta_correcta(self):
        pregunta_actual = self.new_window.pregunta_actual
        return pregunta_actual[-1]

    def cambiar_pregunta(self, new_window):
        self.preguntas_respondidas += 1
        pregunta = self.obtener_pregunta()
        if pregunta:
            new_window.actualizar_pregunta(pregunta)
            self.new_window = new_window
            for boton in new_window.botones:
                boton.config(state=tk.NORMAL)

    def start_action(self):
        self.withdraw()
        new_window = VentanaSecundaria(self, self.obtener_pregunta())
        self.cambiar_pregunta(new_window)

    def continuar_despues_respuesta(self):
        self.cambiar_pregunta(self.new_window)

    def salir(self):
        self.destroy()

    def mostrar_mensaje(self, titulo, mensaje):
        message_box = CustomMessageBox(self, titulo, mensaje)
        self.wait_window(message_box)
        self.continuar_despues_respuesta()

    def mostrar_mensaje_final(self, titulo, mensaje):
        message_box = FinalMessageBox(self, titulo, mensaje)
        self.wait_window(message_box)
        self.resetear_juego()
        self.deiconify()

    def resetear_juego(self):
        self.preguntas_mostradas.clear()
        self.lista = list(self.lista_original)
        self.preguntas_respondidas = 0
        self.respu_corre = 0

    def guardar_puntuacion(self):
        puntuacion = self.respu_corre * 100
        with open("puntuaciones.txt", "a", encoding='utf-8') as file:
            file.write(f"Puntuación: {puntuacion}\n")

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f'{ancho}x{alto}+{x}+{y}')


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, titulo, mensaje):
        super().__init__(parent)
        self.title(titulo)

        self.configure(bg="#f0f0f0")

        self.overrideredirect(True)

        self.parent = parent

        self.canvas = tk.Canvas(self, width=700, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.img_fondo = Image.open("luffy2.jpg")
        self.img_fondo = self.img_fondo.resize((700, 500))
        self.img_fondo_tk = ImageTk.PhotoImage(self.img_fondo)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_fondo_tk)

        self.label = tk.Label(self.canvas, text=mensaje, font=("Arial", 18, "bold"), bg="#f0f0f0", fg="black", padx=20, pady=20)
        self.label.pack(pady=20)

        self.button_ok = tk.Button(self.canvas, text="Aceptar", font=("Arial", 18), activeforeground="#CF9D60", bg="#E71D36", fg="white", command=self.cerrar, width=15, height=2)
        self.button_ok.pack(pady=20)

        self.grab_set()

        self.centrar_ventana(700, 500)

    def cerrar(self):
        self.parent.focus_set()
        self.destroy()

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f'{ancho}x{alto}+{x}+{y}')


class FinalMessageBox(tk.Toplevel):
    def __init__(self, parent, titulo, mensaje):
        super().__init__(parent)
        self.title(titulo)

        self.configure(bg="#f0f0f0")

        self.overrideredirect(True)

        self.parent = parent

        self.canvas = tk.Canvas(self, width=700, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.img_fondo = Image.open("luffy2.jpg")
        self.img_fondo = self.img_fondo.resize((700, 500))
        self.img_fondo_tk = ImageTk.PhotoImage(self.img_fondo)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_fondo_tk)

        self.label = tk.Label(self.canvas, text=mensaje, font=("Arial", 18, "bold"), bg="#f0f0f0", fg="black", padx=20, pady=20)
        self.label.pack(pady=20)

        self.button_ok = tk.Button(self.canvas, text="Aceptar", font=("Arial", 18), activeforeground="#CF9D60", bg="#E71D36", fg="white", command=self.cerrar, width=15, height=2)
        self.button_ok.pack(pady=20)

        self.grab_set()
        self.centrar_ventana(700, 500)

    def cerrar(self):
        self.parent.focus_set()
        self.parent.deiconify()
        self.destroy()

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f'{ancho}x{alto}+{x}+{y}')


class VentanaSecundaria(tk.Toplevel):
    def __init__(self, parent, pregunta):
        super().__init__(parent)
        self.title("Preguntas")
        self.configure(bg="#f0f0f0")
        self.parent = parent
        self.pregunta_actual = pregunta
        self.centrar_ventana(1400, 600)
        self.crear_interfaz()

    def crear_interfaz(self):
        self.canvas = tk.Canvas(self, width=1400, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.img_fondo = Image.open("zoro.jpg")
        self.img_fondo = self.img_fondo.resize((1400, 600))
        self.img_fondo_tk = ImageTk.PhotoImage(self.img_fondo)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_fondo_tk)

        self.text_area = tk.Text(self.canvas, wrap=tk.WORD, font=("Arial", 18, "bold"), bg="#CF9D60", height=5)
        self.text_area.pack(pady=(200, 20), padx=20, expand=False)
        self.text_area.tag_configure("center", justify="center")
        self.text_area.tag_configure("big_bold", font=("Arial", 25, "bold"))
        self.text_area.configure(state='disabled')

        self.frame_botones = tk.Frame(self.canvas, bg="#CF9D60")
        self.frame_botones.pack(pady=20)

        self.botones = []

        self.actualizar_pregunta(self.pregunta_actual)

    def actualizar_pregunta(self, pregunta):
        self.pregunta_actual = pregunta
        texto_pregunta = "¿" + pregunta[0] + "?"
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, texto_pregunta, ("center", "big_bold"))

        self.text_area.insert("1.0", "\n\n")
        self.text_area.insert(tk.END, "\n\n")
        self.text_area.config(state=tk.DISABLED)

        opciones = pregunta[1:5]

        if not self.botones:
            for i, texto in enumerate(['A', 'B', 'C', 'D']):
                boton = tk.Button(self.frame_botones, text=f"{texto}: {opciones[i]}", font=("Arial", 18, "bold"), height=2, width=20,
                                  bg="#E71D36", fg="white", activeforeground="#CF9D60", command=lambda t=texto: self.parent.comprobar_respuesta(t, self.botones),
                                  relief=tk.FLAT, bd=0)
                boton.pack(side=tk.LEFT, padx=5)
                self.botones.append(boton)
        else:
            for i, boton in enumerate(self.botones):
                boton.config(text=f"{['A', 'B', 'C', 'D'][i]}: {opciones[i]}", state=tk.NORMAL)

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f'{ancho}x{alto}+{x}+{y}')


class VentanaRanking(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ranking")
        self.centrar_ventana(600, 400)
        self.configure(bg="#f0f0f0")
        self.overrideredirect(True)
        
        self.canvas = tk.Canvas(self, width=1400, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.img_fondo = Image.open("ranking.jpg")
        self.img_fondo = self.img_fondo.resize((600, 400))
        self.img_fondo_tk = ImageTk.PhotoImage(self.img_fondo)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_fondo_tk)
        self.parent = parent

        self.label_titulo = tk.Label(self.canvas, text="Ranking de Puntuaciones", font=("Arial", 24, "bold"), bg="#E71D36", fg="white")
        self.label_titulo.pack(pady=10)

        self.frame_ranking = tk.Frame(self.canvas, bg="#f0f0f0")
        self.frame_ranking.pack(pady=10)

        self.cargar_puntuaciones()

        self.boton_volver = tk.Button(self.canvas, text="Volver", font=("Arial", 18, "bold"), bg="#E71D36",activeforeground="#CF9D60", fg="white", command=self.volver)
        self.boton_volver.pack(pady=10)

    def cargar_puntuaciones(self):
        try:
            with open("puntuaciones.txt", "r",  encoding='utf-8') as file:
                puntuaciones = file.readlines()
                puntuaciones = [int(line.split(": ")[1]) for line in puntuaciones if line.strip()]
                puntuaciones.sort(reverse=True)

                for idx, puntuacion in enumerate(puntuaciones):
                    label_puntuacion = tk.Label(self.frame_ranking, text=f"Puntuación  {idx + 1}. {puntuacion} Pts", font=("Arial", 18), bg="#f0f0f0", fg="black")
                    label_puntuacion.pack(anchor="w")
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo de puntuaciones no se encontró.")

    def volver(self):
        self.destroy()
        self.parent.deiconify()

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f'{ancho}x{alto}+{x}+{y}')


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
