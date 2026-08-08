import pygame
from pathlib import Path
from character import Personaje
from logic import LogicaJuego
from visual import Renderer
import constants 
from handler import EventHandler

class AvatarGame:     
    def __init__(self, title="Memory Avatar Challenge"):
        
        # 1. CONFIGURACIÓN
        self.titulo = title
        self.ANCHO, self.ALTO = constants.CON.ANCHO, constants.CON.ALTO
        self.FPS = constants.CON.FPS    
        self.pantalla = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption(title)
        self.estado = "VENTANA_1" 
        self.tiempo_memorizar = 5
        self.tiempo_reconstruir = None
        self.tiempo_inicio_estado = 0
        self.timer_reconstruir_inicio = 0
    
        # 3. VARIABLES DE AUDIO Y VOLUMEN 
        self.vol_musica = 0.5  
        self.vol_sonidos = 0.5  
        self.slider_seleccionado = 0 
        self.rect_slider_musica = pygame.Rect(550, 570, 180, 10)
        self.rect_slider_sonidos = pygame.Rect(550, 665, 180, 10)
        
        # 4. RUTAS A LOS ASSETS
        ruta_src = Path(__file__).resolve().parent
        ruta_fondos = ruta_src / "assets" / "backgrounds"
        ruta_timer = ruta_src / "assets" / "timer"
        ruta_fuentes = ruta_src / "assets" / "font"
        ruta_sonidos = ruta_src / "assets" / "sounds"
        ruta_textos = ruta_src / "textos.json"
        
        # 5. DICCIONARIO DE AUDIO
        pygame.mixer.init()
        self.sonidos = {}
        archivos_sonidos = {
            "musica_inicio": "menu.mp3",       
            "click_pasar": "boton.mp3",         
            "click_seleccionar": "click.mp3",      
            "contador_timer": "timer.mp3",       
            "musica_memorizar": "reloj.mp3", 
            "musica_vs": "vs.mp3",      
            "victoria": "victoria.mp3",                 
            "derrota": "derrota.mp3",
            "empate": "empate.mp3",
            "vestir":"vestir.mp3"        
        }
        
        for clave, archivo in archivos_sonidos.items():
            ruta_s = ruta_sonidos / archivo
            self.sonidos[clave] = pygame.mixer.Sound(str(ruta_s))
    
        self.actualizar_volumenes()
        if self.sonidos["musica_inicio"]:
            self.sonidos["musica_inicio"].play(loops=-1)
            
        # 6. FUENTES DE TEXTO
        archivo_fuente = next(ruta_fuentes.glob(constants.CON.FUENTE_PRINCIPAL), None)
        archivo_relleno = next(ruta_fuentes.glob(constants.CON.FUENTE_RELLENO_P), None)
        archivo_instruc = next(ruta_fuentes.glob(constants.CON.FUENTE_INTRUCCIONES), None)
        
        self.fuente_start = pygame.font.Font(str(archivo_fuente), constants.CON.START_SIZE)
        self.fuente_title = pygame.font.Font(str(archivo_fuente), constants.CON.TITLE_SIZE)
        self.fuente_subtitle = pygame.font.Font(str(archivo_fuente), constants.CON.SUBTITLE_SIZE)
        self.fuente_num = pygame.font.Font(str(archivo_relleno), constants.CON.NUM_SIZE)
        self.fuente_category = pygame.font.Font(str(archivo_relleno), constants.CON.CATEGORY_SIZE)
        self.fuente_preparate = pygame.font.Font(str(archivo_fuente), constants.CON.TIMER_SIZE)
        self.fuente_instrucciones= pygame.font.Font(str(archivo_instruc), constants.CON.INST_SIZE)
        
        # 7. VARIABLES DE MENÚ ROPA
        self.indice_menu = 0   
        self.categoria_inicio = 0  
        self.max_visibles = 3      
        self.fila_seleccionada = 0   
        self.col_seleccionada = 0
        self.confirm = {} 
        
        # Elementos fijos
        self.btn_subir = pygame.Rect(290, 95, 60, 35)
        self.btn_bajar = pygame.Rect(290, 580, 60, 35)
        self.botones_ropa = []

        # 8. Componentes
        self.personaje = Personaje()
        self.logica = LogicaJuego(self.personaje.opciones)
        self.handler = EventHandler(self)
        self.renderer = Renderer(self)

        # 9. DICCIONARIO DE FONDOS
        self.fondos = {}
        archivos_fondos = {
            "VENTANA_1": "inicio.png",       
            "VENTANA_2": "menu.png",
            "VENTANA_3": "visualizar.png",
            "VENTANA_4": "juego.png",
            "VENTANA_5": "vs.png",
            "VENTANA_6": "resultado.png"
        }
        for estado, archivo in archivos_fondos.items():
            ruta_final = ruta_fondos / archivo
            try:
                imagen_cargada = pygame.image.load(str(ruta_final))
                self.fondos[estado] = pygame.transform.scale(imagen_cargada, (1280, 720))
            except pygame.error:
                fallback = pygame.Surface((1280, 720))
                fallback.fill((40, 40, 50))
                self.fondos[estado] = fallback

        self.superficie_transicion = pygame.Surface((1280, 720))
        self.superficie_transicion.fill((0, 0, 0))
        
        #9.1 DICCIONARIO DE IMÁGENES DE LA INTERFAZ
        self.ui_images = {}
        archivos_ui = {
            "logo_titulo": "Logo.png",         
            "fondo_dificultad": "fondo_dificultad.png",  
            "fondo_start": "fondo_titulo.png",
            "fondo_musica": "musica.png",
            "fondo_sonidos": "sonido.png",
            "fondo_categoria": "fondo_categoria.png",
            "marco_normal": "fondo_numero.png",
            "marco_seleccionado": "fondo_numero_seleccionado.png",
            "fondo_ropa":"fondo_ropa.png",
            "fondo_dificultad_bajo":"fondo_dificultad_bajo.png",
            "fondo_dificultad_medio":"fondo_dificultad_medio.png",
            "fondo_dificultad_alto":"fondo_dificultad_alto.png",
            "base":"BASE_M.png",
            "base1":"baseR.png",
            "base2":"baseA.png",
            "base3":"baseV.png",
            "barra":"barra.png",
            "p1":"fondo_puntos1.png",
            "p2":"fondo_puntos2.png",
            "p3":"fondo_puntos3.png",
            "cartelera":"cartelera.png"
        }
    
        for clave, archivo in archivos_ui.items():
            ruta_img = ruta_fondos / archivo
            if ruta_img.exists():
                self.ui_images[clave] = pygame.image.load(str(ruta_img)).convert_alpha()
        
        # 10. ANIMACIÓN DEL CONTADOR
        self.fotogramas_contador = []
        if ruta_timer.exists():
            archivos = sorted(list(ruta_timer.glob("*.png")), key=lambda x: int(x.stem))
            for archivo in archivos:
                img = pygame.image.load(str(archivo)).convert_alpha()
                img_escalada = pygame.transform.scale(img, (800, 400))
                self.fotogramas_contador.append(img_escalada)
                
        self.reproduciendo_intro = False
        self.frame_actual_idx = 0
        self.ultimo_cambio_frame = 0
        self.ms_por_frame = 111  
        self.superficie_borrosa = None
        
        self.activar_transiciones = False
        
    def run_independently(self):
        pygame.init()
        reloj = pygame.time.Clock()

        self.btn_start = pygame.Rect(constants.CON.START_BUTTON)
        self.btn_listo = pygame.Rect(constants.CON.READY_BUTTON)
        self.btn_resultados = pygame.Rect(constants.CON.RESULTS_BUTTON)
        
        self.btn_bajo = pygame.Rect(constants.CON.LOW_BUTTON)
        self.btn_medio = pygame.Rect(constants.CON.MEDIO_BUTTON)
        self.btn_alto = pygame.Rect(constants.CON.HIHG_BUTTON)

        while True:
            self.handler.process_events()
            self._update()
            self.renderer.render()
            reloj.tick(self.FPS)
    
    def actualizar_volumenes(self):
        musicas = ["musica_inicio", "musica_memorizar", "musica_vs"]
        efectos = ["click_pasar", "click_seleccionar", "contador_timer", "victoria", "derrota"]
        
        for clave, sound_obj in self.sonidos.items():
            if sound_obj:
                if clave in musicas: sound_obj.set_volume(self.vol_musica)
                elif clave in efectos: sound_obj.set_volume(self.vol_sonidos)
            
    def _crear_fondo_borroso(self, superficie_original):
        ancho, alto = superficie_original.get_size()
        mini = pygame.transform.smoothscale(superficie_original, (ancho // 10, alto // 10))
        return pygame.transform.smoothscale(mini, (ancho, alto))
            
    def _avanzar_a_memorizar(self):
        self.logica.iniciar_ronda()
        self.reproduciendo_intro = True
        self.sonidos["contador_timer"].play()
        self.frame_actual_idx = 0
        self.ultimo_cambio_frame = pygame.time.get_ticks()
        if "VENTANA_3" in self.fondos:self.superficie_borrosa = self._crear_fondo_borroso(self.fondos["VENTANA_3"])
        self.estado = "VENTANA_3" 
    
    def _procesar_resultados(self):
        self.logica.simular_ia_y_evaluar()
        self.sonidos["musica_vs"].play(loops=-1)      
        self.estado = "VENTANA_5" 

    def _visualizar_resultados(self):
        if self.logica.puntos_usuario > self.logica.puntos_ia: self.sonidos["victoria"].play()
        elif self.logica.puntos_usuario < self.logica.puntos_ia: self.sonidos["derrota"].play()
        else: self.sonidos["empate"].play()
        self.estado = "VENTANA_6" 
        
    def _update(self):
        if self.estado == "VENTANA_3":
            if self.reproduciendo_intro:
                ahora = pygame.time.get_ticks()
                if ahora - self.ultimo_cambio_frame >= self.ms_por_frame:
                    self.frame_actual_idx += 1
                    self.ultimo_cambio_frame = ahora
                    if self.frame_actual_idx >= len(self.fotogramas_contador):
                        self.reproduciendo_intro = False
                        self.tiempo_inicio_estado = pygame.time.get_ticks() 
                        self.sonidos["musica_memorizar"].play(loops=-1)
            else:
                tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio_estado) // 1000
                if tiempo_transcurrido >= self.tiempo_memorizar:
                    self.sonidos["musica_memorizar"].stop()
                    lista_categorias = list(self.personaje.opciones.keys())
                    if lista_categorias:
                        primera_cat = lista_categorias[0]
                        lista_prendas = self.personaje.opciones[primera_cat]
                        if lista_prendas:
                            primer_item = lista_prendas[0] 
                            self.logica.seleccionar_item_usuario(primera_cat, primer_item)
                    
                    self.timer_reconstruir_inicio = pygame.time.get_ticks()
                    self.estado = "VENTANA_4"

        elif self.estado == "VENTANA_4" and self.tiempo_reconstruir is not None:
            pasado_armar = (pygame.time.get_ticks() - self.timer_reconstruir_inicio) // 1000
            if pasado_armar >= self.tiempo_reconstruir:
                self._procesar_resultados()
    
    def reiniciar_juego_completo(self):
        self.confirm.clear()
        self.categoria_inicio = 0
        self.fila_seleccionada = 0
        self.col_seleccionada = 0
        self.logica.puntos_usuario = 0
        self.logica.puntos_ia = 0
        self.logica.combinacion_objetivo.clear()
        self.logica.combinacion_usuario.clear()
        self.logica.combinacion_ia.clear()
        self.slider_seleccionado = 0
        self.indice_menu = 0
        self.sonidos["musica_inicio"].play(loops=-1)
        self.estado = "VENTANA_1"
