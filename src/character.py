from pathlib import Path
import pygame

class Personaje:
    def __init__(self):
        ruta_src = Path (__file__).resolve().parent

        self.ruta_images = ruta_src / "assets" / "images"
        
        ruta_base = self.ruta_images / "snoppybase" / "base.png"
        self.imagen_base = pygame.image.load(str(ruta_base))
        
        self.opciones = {
            "sombreros": [
                {"id": "1", "img": self._cargar_asset("sombreros", "s1.png")},
                {"id": "2", "img": self._cargar_asset("sombreros", "s2.png")},
                {"id": "3", "img": self._cargar_asset("sombreros", "s3.png")}
            ],
            "camisas": [
                {"id": "1", "img": self._cargar_asset("camisas", "camisa1.png")},
                {"id": "2", "img": self._cargar_asset("camisas", "camisa2.png")},
                {"id": "3", "img": self._cargar_asset("camisas", "camisa3.png")}
            ],
            "pantalones": [
                {"id": "1", "img": self._cargar_asset("pantalones", "pantalon1.png")},
                {"id": "2", "img": self._cargar_asset("pantalones", "pantalon2.png")},
                {"id": "3", "img": self._cargar_asset("pantalones", "pantalon3.png")}
            ],
            "accesorios": [
                {"id": "1", "img": self._cargar_asset("accesorios", "ac1.png")},
                {"id": "2", "img": self._cargar_asset("accesorios", "ac2.png")},
                {"id": "3", "img": self._cargar_asset("accesorios", "ac3.png")}
            ]
        }

    def _cargar_asset(self, carpeta, archivo):
        ruta_archivo = self.ruta_images / carpeta / archivo
        return pygame.image.load(str(ruta_archivo))

    def dibujar(self, pantalla, x, y, combinacion):
        pantalla.blit(self.imagen_base, (x, y))
        orden_capas = ["pantalones", "camisas", "accesorios", "sombreros"]
        
        for categoria in orden_capas:
            prenda = combinacion.get(categoria) or combinacion.get(categoria.lower())
            if prenda and isinstance(prenda, dict) and "img" in prenda:
                if prenda["img"] is not None:
                    pantalla.blit(prenda["img"], (x, y))