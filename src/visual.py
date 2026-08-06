import pygame
import constants

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.pantalla.fill((15, 15, 15)) 
        self.game.pantalla.blit(self.game.fondos[self.game.estado], (0, 0))

        if self.game.estado == "VENTANA_1":
            self.game.pantalla.blit(self.game.ui_images.get("logo_titulo"), (289, 50))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_start"), (482, 420))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_musica"), (482, 515))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_sonidos"), (482, 610))
            
            color_start = (constants.CON.BLANCO) if self.game.slider_seleccionado == 0 else (constants.CON.NEGRO)
            self.game.pantalla.blit(self.game.fuente_start.render("START", True, color_start), (535, 440))
           
            #PARA MUSICA
            color_music = (constants.CON.BLANCO) if self.game.slider_seleccionado == 1 else (constants.CON.NEGRO)
            txt_musica = self.game.fuente_subtitle.render(f"{"MUSICA: "}{int(self.game.vol_musica * 100)}%", True, color_music)
            self.game.pantalla.blit(txt_musica, (535, 535))
            pygame.draw.rect(self.game.pantalla, (50, 50, 50), self.game.rect_slider_musica, border_radius=5)
            x_indicador_m = self.game.rect_slider_musica.x + int(self.game.vol_musica * self.game.rect_slider_musica.w)
            pygame.draw.circle(self.game.pantalla, color_music, (x_indicador_m, self.game.rect_slider_musica.centery), 8)

            #PARA SONIDO
            color_sonidos = (constants.CON.BLANCO) if self.game.slider_seleccionado == 2 else (constants.CON.NEGRO)
            txt_sonidos = self.game.fuente_subtitle.render(f"{"EFECTOS: "}{int(self.game.vol_sonidos * 100)}%", True, color_sonidos)
            self.game.pantalla.blit(txt_sonidos, (535, 630))
            pygame.draw.rect(self.game.pantalla, (50, 50, 50), self.game.rect_slider_sonidos, border_radius=5)
            x_indicador_s = self.game.rect_slider_sonidos.x + int(self.game.vol_sonidos * self.game.rect_slider_sonidos.w)
            pygame.draw.circle(self.game.pantalla, color_sonidos, (x_indicador_s, self.game.rect_slider_sonidos.centery), 8)

        elif self.game.estado == "VENTANA_2":
            self.game.pantalla.blit(self.game.ui_images.get("fondo_dificultad"), (90, 75))
            titulo = self.game.fuente_title.render("SELECCIONA LA DIFICULTAD", True, (constants.CON.BLANCO))
            self.game.pantalla.blit(titulo, (231, 155))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_dificultad_bajo"), (95, 350))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_dificultad_medio"), (490, 350))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_dificultad_alto"), (885, 350))
            
            botones = [self.game.btn_bajo, self.game.btn_medio, self.game.btn_alto]
            pygame.draw.rect(self.game.pantalla, (constants.CON.BLANCO), botones[self.game.indice_menu], width=4, border_radius=8)
            
            self.game.pantalla.blit(self.game.fuente_start.render("BAJO", True, (constants.CON.NEGRO)), (150, 400))
            self.game.pantalla.blit(self.game.fuente_start.render("MEDIO", True, (constants.CON.NEGRO)), (540, 400))
            self.game.pantalla.blit(self.game.fuente_start.render("ALTO", True, (constants.CON.NEGRO)), (940, 400))
            
        elif self.game.estado == "VENTANA_3":
            if self.game.reproduciendo_intro and self.game.fotogramas_contador:
                self.game.pantalla.blit(self.game.superficie_borrosa, (0,0))

                texto = self.game.fuente_preparate.render("PREPARATE PARA MEMORIZAR", True, (constants.CON.BLANCO))
                x_centro = (1280 - texto.get_width()) // 2
                self.game.pantalla.blit(texto, (x_centro, 100))
                img_frame = self.game.fotogramas_contador[self.game.frame_actual_idx]
                self.game.pantalla.blit(img_frame, ((1280 - img_frame.get_width()) // 2, (720 - img_frame.get_height()) // 2))    
            else:
                self.game.pantalla.blit(self.game.ui_images.get("fondo_dificultad"), (90, 20))
                self.game.pantalla.blit(self.game.ui_images.get("base"), (475, 550))
                quedan = self.game.tiempo_memorizar - (pygame.time.get_ticks() - self.game.tiempo_inicio_estado) // 1000
                txt = self.game.fuente_title.render(f"MEMORIZA EL AVATAR: {max(0, quedan)}s", True, (constants.CON.BLANCO))
                self.game.pantalla.blit(txt, (260, 100))
                self.game.personaje.dibujar(self.game.pantalla, 350, 150, self.game.logica.combinacion_objetivo)
            
        elif self.game.estado == "VENTANA_4":
            if self.game.tiempo_reconstruir is not None:
                quedan_armar = self.game.tiempo_reconstruir - (pygame.time.get_ticks() - self.game.timer_reconstruir_inicio) // 1000
                txt_tiempo = f"TIEMPO RESTANTE: {max(0, quedan_armar)}s"
            else:
                txt_tiempo = "TIEMPO: ILIMITADO"
                
            self.game.pantalla.blit(self.game.ui_images.get("base"), (730, 500))
            self.game.pantalla.blit(self.game.ui_images.get("barra"), (190, 5))
            
            superficie_texto = self.game.fuente_title.render(txt_tiempo, True, (constants.CON.BLANCO))
            ancho_texto = superficie_texto.get_width()
            text_x = 640 - (ancho_texto // 2)
            self.game.pantalla.blit(superficie_texto, (text_x, 40))
        
            lista_categorias = list(self.game.personaje.opciones.keys())
            
            previsualizacion_ropa = self.game.confirm.copy()
            
            
            indice_cursor_cat = self.game.categoria_inicio + self.game.fila_seleccionada
            if 0 <= indice_cursor_cat < len(lista_categorias):
                cat_bajo_cursor = lista_categorias[indice_cursor_cat]
                lista_items_cursor = self.game.personaje.opciones[cat_bajo_cursor]
                col_idx_cursor = self.game.col_seleccionada
                
                
                if 0 <= col_idx_cursor < len(lista_items_cursor):
                    previsualizacion_ropa[cat_bajo_cursor] = lista_items_cursor[col_idx_cursor]
            
            self.game.personaje.dibujar(self.game.pantalla, 610, 105, previsualizacion_ropa)
            
            lista_categorias = list(self.game.personaje.opciones.keys())
            color_flecha_arriba = constants.CON.NEGRO if self.game.categoria_inicio > 0 else constants.CON.BLANCO
            color_flecha_abajo = constants.CON.NEGRO if (self.game.categoria_inicio + self.game.max_visibles) < len(lista_categorias) else constants.CON.BLANCO
            pygame.draw.polygon(self.game.pantalla, color_flecha_arriba, [(constants.CON.FA_VS), (constants.CON.FA_VII), (constants.CON.FA_VID)]) 
            pygame.draw.polygon(self.game.pantalla, color_flecha_abajo, [(constants.CON.FB_VI), (constants.CON.FB_VSI), (constants.CON.FB_VSD)])
            
            y_fila_visual = constants.CON.M_Y 
            y_fila = constants.CON.P_Y_CATE
            
            for i in range(self.game.max_visibles):
                indice_global_cat = self.game.categoria_inicio + i
                if indice_global_cat >= len(lista_categorias):
                    break
                    
                cat_actual = lista_categorias[indice_global_cat]
                bg_dif = self.game.ui_images.get("fondo_categoria")
                self.game.pantalla.blit(bg_dif, (constants.CON.M_X, y_fila_visual))
                
                self.game.pantalla.blit(self.game.fuente_category.render(cat_actual.lower(), True, (constants.CON.BLANCO)), (constants.CON.M_X + 20, y_fila_visual + 5))
            
                lista_items = self.game.personaje.opciones[cat_actual]
                x_offset = constants.CON.P_X_CATE
                
                for col_idx, item in enumerate(lista_items):
                    rect_visual = pygame.Rect(x_offset, y_fila + 45, 80, 60)
                    activo = self.game.confirm.get(cat_actual) == item
                    esta_seleccionado = (i == self.game.fila_seleccionada and col_idx == self.game.col_seleccionada)
                    
                    if activo:
                        img_sel = self.game.ui_images.get("marco_seleccionado")
                        if img_sel:
                            img_escalada = pygame.transform.scale(img_sel, (rect_visual.w, rect_visual.h))
                            self.game.pantalla.blit(img_escalada, (rect_visual.x, rect_visual.y))
                    else:
                        img_norm = self.game.ui_images.get("marco_normal")
                        if img_norm:
                            img_escalada = pygame.transform.scale(img_norm, (rect_visual.w, rect_visual.h))
                            self.game.pantalla.blit(img_escalada, (rect_visual.x, rect_visual.y))
                    
                    if esta_seleccionado:
                        rect_cursor = rect_visual.inflate(8, 8)
                        pygame.draw.rect(self.game.pantalla, (248, 113, 113), rect_cursor, width=3, border_radius=5)
                    
                    self.game.pantalla.blit(self.game.fuente_num.render(item["id"], True, (constants.CON.NEGRO)), (rect_visual.x + 25, rect_visual.y + 4))
                    x_offset += 100 
                y_fila += 130
                y_fila_visual += 130
        
            bg_dif = self.game.ui_images.get("fondo_musica")
            self.game.pantalla.blit(bg_dif, (483, 625))
            self.game.pantalla.blit(self.game.fuente_subtitle.render(" IR A COMPETIR", True, (constants.CON.BLANCO)), (510, 655))
            self.game.pantalla.blit(self.game.fuente_instrucciones.render(" PRESIONAR ESPACIO ", True, (constants.CON.NEGRO)), (160, 640))
            self.game.pantalla.blit(self.game.fuente_instrucciones.render(" Para Confirmar Prenda ", True, (constants.CON.NEGRO)), (70, 675))
            
        elif self.game.estado == "VENTANA_5":
            self.game.pantalla.blit(self.game.ui_images.get("barra"), (190, 5))
            self.game.pantalla.blit(self.game.fuente_start.render("RESULTADOS", True, (constants.CON.BLANCO)), (450, 40))
        
            self.game.pantalla.blit(self.game.ui_images.get("base1"), (140, 470))
            self.game.pantalla.blit(self.game.ui_images.get("p1"), (133, 535))
            self.game.personaje.dibujar(self.game.pantalla, 15, 80, self.game.logica.combinacion_objetivo)
            self.game.pantalla.blit(self.game.fuente_subtitle.render("OBJETIVO", True, (constants.CON.BLANCO)), (200, 575))
            
            self.game.pantalla.blit(self.game.ui_images.get("base2"), (500, 470))
            self.game.pantalla.blit(self.game.ui_images.get("p2"), (493, 535))
            self.game.personaje.dibujar(self.game.pantalla, 375, 80, self.game.logica.combinacion_usuario)
            self.game.pantalla.blit(self.game.fuente_subtitle.render("TU INTENTO", True, (constants.CON.BLANCO)), (560, 575))
            
            self.game.pantalla.blit(self.game.ui_images.get("base3"), (860, 470))
            self.game.pantalla.blit(self.game.ui_images.get("p3"), (853, 535))
            self.game.personaje.dibujar(self.game.pantalla, 735, 80, self.game.logica.combinacion_ia)
            self.game.pantalla.blit(self.game.fuente_subtitle.render("INTENTO IA", True, (constants.CON.BLANCO)), (920, 575))
            
            self.game.pantalla.blit(self.game.ui_images.get("fondo_musica"), (483, 625))
            self.game.pantalla.blit(self.game.fuente_subtitle.render("VER PUNTAJES", True, (constants.CON.BLANCO)), (510, 655))

        elif self.game.estado == "VENTANA_6":
            self.game.sonidos["musica_inicio"].stop()
            self.game.pantalla.blit(self.game.ui_images.get("cartelera"), (190, 170))
            txt_usr = self.game.fuente_start.render(f"TUS PUNTOS: {self.game.logica.puntos_usuario}", True, (constants.CON.BLANCO))
            txt_ia = self.game.fuente_start.render(f"PUNTOS IA: {self.game.logica.puntos_ia}", True, (constants.CON.BLANCO))
            center_usr=(constants.CON.ANCHO-txt_usr.get_width())//2
            center_ia=(constants.CON.ANCHO-txt_ia.get_width())//2
            self.game.pantalla.blit(txt_usr, (center_usr, 300))
            self.game.pantalla.blit(txt_ia, (center_ia, 420))
            
            self.game.pantalla.blit(self.game.ui_images.get("barra"), (190, 5))
            if self.game.logica.puntos_usuario > self.game.logica.puntos_ia:
                msg = "GANASTE"
            elif self.game.logica.puntos_usuario < self.game.logica.puntos_ia:
                msg = "PERDISTE"
            else: 
                msg = "EMPATE"
            self.game.pantalla.blit(self.game.fuente_start.render(msg, True, (constants.CON.BLANCO)), (480, 40))
            self.game.pantalla.blit(self.game.ui_images.get("fondo_musica"), (483, 625))
            self.game.pantalla.blit(self.game.fuente_subtitle.render("VOLVER AL MENU", True, (constants.CON.BLANCO)), (495, 655))
        pygame.display.flip()