import random

class LogicaJuego:
    def __init__(self, opciones_personaje):
        self.opciones = opciones_personaje
        self.combinacion_objetivo = {}
        self.combinacion_usuario = {}
        self.combinacion_ia = {}
        self.puntos_usuario = 0
        self.puntos_ia = 0

        self.nivel_dificultad = "MEDIO"
    def iniciar_ronda(self):
        self.combinacion_objetivo = {cat: random.choice(lista) for cat, lista in self.opciones.items()}
        self.combinacion_usuario = {cat: None for cat in self.opciones}
        self.combinacion_ia = {}
        self.puntos_usuario = 0
        self.puntos_ia = 0

    def seleccionar_item_usuario(self, categoria, item):
        self.combinacion_usuario[categoria] = item

    def simular_ia_y_evaluar(self):
        if self.nivel_dificultad == "BAJO":
            pobabilidad_acierto = 0.4
        elif self.nivel_dificultad == "MEDIO":
            pobabilidad_acierto = 0.6
        else:  
            pobabilidad_acierto = 0.8
            
        for cat in self.opciones:
            if random.random() < pobabilidad_acierto:
                self.combinacion_ia[cat] = self.combinacion_objetivo[cat]
            else:
                self.ia_eleccion = random.choice(self.opciones[cat])
                self.combinacion_ia[cat] = random.choice(self.opciones[cat])
                
        self.puntos_usuario = sum(100 for cat in self.opciones if self.combinacion_usuario.get(cat) == self.combinacion_objetivo.get(cat))
        self.puntos_ia = sum(100 for cat in self.opciones if self.combinacion_ia.get(cat) == self.combinacion_objetivo.get(cat))