from dataclasses import dataclass

@dataclass (frozen=True)
class constantes:
    ANCHO=1280
    ALTO=720
    FPS=60
    
    START_SIZE=60
    TITLE_SIZE=52
    SUBTITLE_SIZE=30
    TIMER_SIZE=40
    NUM_SIZE=65
    CATEGORY_SIZE=40
    INST_SIZE=30
    
    START_BUTTON = (540, 400, 200, 60)
    READY_BUTTON = (540, 600, 200, 60)
    
    #botones de la ventana de dificultad
    LOW_BUTTON=(85, 350, 320, 150)
    MEDIO_BUTTON=(480, 350, 320, 150)
    HIHG_BUTTON= (875, 350, 320, 150)
    
    #boton vestidor
    RESULTS_BUTTON = (540, 620, 200, 50)

    #fuentes
    FUENTE_PRINCIPAL = "Golden Age Shad.ttf"
    FUENTE_RELLENO_P="Golden Age.ttf"
    FUENTE_INTRUCCIONES="Golden Age.ttf"
    
    #cuadros morados
    M_ALTO=35
    M_ANCHO=230
    M_X=200
    M_Y=180

    #FLECHA ARRIBA
    FA_VS=(340,125)
    FA_VII=(310,160)
    FA_VID=(370,160)

    #FLECHA ABAJO
    FB_VI=(340,615)
    FB_VSI=(310,580)
    FB_VSD=(370,580)

    #cuadros de seleccion
    P_X_CATE=200
    P_Y_CATE=195

    #COLORES
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    
CON = constantes()


