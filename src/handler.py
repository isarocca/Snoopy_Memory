import pygame
import sys
import constants

class EventHandler:
    def __init__(self, game):
        self.game = game

    def process_events(self):
        pos_mouse = pygame.mouse.get_pos()
        self._handle_hover_and_drag(pos_mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self._handle_mouse_click(pos_mouse)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.game.estado == "VENTANA_4":
                    self._confirmar_prenda_espacio()

    def _handle_hover_and_drag(self, pos):
        if self.game.estado == "VENTANA_1":
            rect_start = pygame.Rect(482,420,315,90) 
            rect_slider_musica = pygame.Rect(482,515,315,87) 
            rect_slider_sonidos = pygame.Rect(482,610,315,85)

            if rect_start.collidepoint(pos):
                if self.game.slider_seleccionado != 0:
                    self.game.slider_seleccionado = 0
                    self.game.sonidos["click_pasar"].play()

            elif rect_slider_musica.collidepoint(pos):
                if self.game.slider_seleccionado != 1:
                    self.game.slider_seleccionado = 1
                    self.game.sonidos["click_pasar"].play()

            elif rect_slider_sonidos.collidepoint(pos):
                if self.game.slider_seleccionado != 2:
                    self.game.slider_seleccionado = 2
                    self.game.sonidos["click_pasar"].play()

            if pygame.mouse.get_pressed()[0]:
                if self.game.slider_seleccionado == 1:
                    rel_x = pos[0] - rect_slider_musica.x
                    self.game.vol_musica = min(1.0, max(0.0, rel_x / rect_slider_musica.w))
                    self.game.actualizar_volumenes()

                elif self.game.slider_seleccionado == 2:
                    rel_x = pos[0] - rect_slider_sonidos.x
                    self.game.vol_sonidos = min(1.0, max(0.0, rel_x / rect_slider_sonidos.w))
                    self.game.actualizar_volumenes()

        elif self.game.estado == "VENTANA_2":
            rect_bajo = pygame.Rect(*constants.CON.LOW_BUTTON)
            rect_medio = pygame.Rect(*constants.CON.MEDIO_BUTTON)
            rect_alto = pygame.Rect(*constants.CON.HIHG_BUTTON)

            nuevo_indice = None
            if rect_bajo.collidepoint(pos): nuevo_indice = 0
            elif rect_medio.collidepoint(pos): nuevo_indice = 1
            elif rect_alto.collidepoint(pos): nuevo_indice = 2

            if nuevo_indice is not None and self.game.indice_menu != nuevo_indice:
                self.game.indice_menu = nuevo_indice
                self.game.sonidos["click_pasar"].play()

    def _handle_mouse_click(self, pos):
        if self.game.estado == "VENTANA_1":
            rect_start = pygame.Rect(482, 420, 315, 90)
            if rect_start.collidepoint(pos):
                self.game.sonidos["click_seleccionar"].play()
                self.game.estado = "VENTANA_2"
                self.game.indice_menu = 0

        elif self.game.estado == "VENTANA_2":
            rect_bajo = pygame.Rect(*constants.CON.LOW_BUTTON)
            rect_medio = pygame.Rect(*constants.CON.MEDIO_BUTTON)
            rect_alto = pygame.Rect(*constants.CON.HIHG_BUTTON)

            if any(r.collidepoint(pos) for r in [rect_bajo, rect_medio, rect_alto]):
                self.game.sonidos["click_seleccionar"].play()
                self.game.sonidos["musica_inicio"].stop()

                if self.game.indice_menu == 0:
                    self.game.logica.nivel_dificultad = "BAJO"
                    self.game.tiempo_memorizar = 8
                    self.game.tiempo_reconstruir = None
                elif self.game.indice_menu == 1:
                    self.game.logica.nivel_dificultad = "MEDIO"
                    self.game.tiempo_memorizar = 5
                    self.game.tiempo_reconstruir = 10
                elif self.game.indice_menu == 2:
                    self.game.logica.nivel_dificultad = "ALTO"
                    self.game.tiempo_memorizar = 3
                    self.game.tiempo_reconstruir = 5

                self.game._avanzar_a_memorizar()

        elif self.game.estado == "VENTANA_4":
            lista_categorias = list(self.game.personaje.opciones.keys())
            rect_flecha_arriba = pygame.Rect(310, 125, 60, 35)
            rect_flecha_abajo = pygame.Rect(310, 580, 60, 35)

            if rect_flecha_arriba.collidepoint(pos):
                if self.game.categoria_inicio > 0:
                    self.game.categoria_inicio -= 1
                    self.game.sonidos["click_pasar"].play()
                return

            if rect_flecha_abajo.collidepoint(pos):
                if self.game.categoria_inicio + self.game.max_visibles < len(lista_categorias):
                    self.game.categoria_inicio += 1
                    self.game.sonidos["click_pasar"].play()
                return

            y_fila = constants.CON.P_Y_CATE + 45 

            for i in range(self.game.max_visibles):
                indice_global_cat = self.game.categoria_inicio + i
                if indice_global_cat >= len(lista_categorias):
                    break

                cat_actual = lista_categorias[indice_global_cat]
                lista_prendas = self.game.personaje.opciones[cat_actual]
                x_offset = constants.CON.P_X_CATE

                for col_idx, item_apuntado in enumerate(lista_prendas):
                    rect_item = pygame.Rect(x_offset, y_fila, 80, 60)

                    if rect_item.collidepoint(pos):
                        self.game.fila_seleccionada = i
                        self.game.col_seleccionada = col_idx
                        self.game.sonidos["click_pasar"].play()
                        return

                    x_offset += 100
                y_fila += 130
            rect_competir = pygame.Rect(483, 625, 315, 87)
            if rect_competir.collidepoint(pos):
                self.game.sonidos["click_seleccionar"].play()
                self.game.logica.combinacion_usuario.clear()
                for cat, item in self.game.confirm.items():
                    self.game.logica.combinacion_usuario[cat] = item
                self.game._procesar_resultados()

        elif self.game.estado == "VENTANA_5":
            rect_ver_puntajes = pygame.Rect(483, 625, 315, 87)
            if rect_ver_puntajes.collidepoint(pos):
                self.game.sonidos["click_seleccionar"].play()
                self.game.sonidos["musica_vs"].stop()
                self.game._visualizar_resultados()

        elif self.game.estado == "VENTANA_6":
            rect_reintentar = pygame.Rect(483, 625, 315, 87)
            if rect_reintentar.collidepoint(pos):
                self.game.sonidos["click_seleccionar"].play()
                self.game.sonidos["victoria"].stop()
                self.game.sonidos["derrota"].stop()
                self.game.sonidos["empate"].stop()
                self.game.reiniciar_juego_completo()

    def _confirmar_prenda_espacio(self):
        lista_categorias = list(self.game.personaje.opciones.keys())
        indice_cat_global = self.game.categoria_inicio + self.game.fila_seleccionada

        if indice_cat_global < len(lista_categorias):
            cat_actual = lista_categorias[indice_cat_global]
            lista_prendas = self.game.personaje.opciones[cat_actual]

            col_index = min(self.game.col_seleccionada, len(lista_prendas) - 1)
            if col_index >= 0:
                item_actual = lista_prendas[col_index]
                self.game.confirm[cat_actual] = item_actual
                self.game.sonidos["click_seleccionar"].play()