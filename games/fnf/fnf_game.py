import pygame
import random
import cv2
from games.fnf.config_fnf import WIDTH, HEIGHT, COLOR_BG, COLOR_LANE_LINE, LANE_COLORS, LANE_KEYS
from games import result

class Lane:
    NOTE_SIZE = 42 

    def __init__(self, nombre, x):
        self.nombre = nombre
        self.x = x
        self.color = LANE_COLORS[nombre]
        self.tecla = LANE_KEYS[nombre]

        imagen_original = pygame.image.load(f"images/games/fnf/{nombre}.png").convert_alpha()
        self.imagen = pygame.transform.scale(imagen_original, (self.NOTE_SIZE, self.NOTE_SIZE))
        self.receptor = pygame.transform.scale(imagen_original, (54, 54))


    def dibujar(self, screen):
        pygame.draw.line(screen, COLOR_LANE_LINE, (self.x, 0), (self.x, HEIGHT), 2)       

        hit_y = HEIGHT - 80

        rect = self.receptor.get_rect(center=(int(self.x), hit_y))

        screen.blit(self.receptor, rect)


class Nota:
    def __init__(self, carril, velocidad):
        self.carril = carril
        self.y = -30
        self.velocidad = velocidad
        self.resuelta = False
        self.acierto = False

    def actualizar(self, dt):
        self.y += self.velocidad * dt

    def dibujar(self, screen):
        imagen = self.carril.imagen
        rect = imagen.get_rect(center=(int(self.carril.x), int(self.y)))

        if self.resuelta:
            imagen_gris = imagen.copy()
            imagen_gris.fill((90, 90, 90, 180), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(imagen_gris, rect)
        else:
            screen.blit(imagen, rect)

    def fuera_de_pantalla(self):
        return self.y > HEIGHT + 40


def crear_carriles():
    nombres = ["izq", "aba", "arr", "der"]
    espacio_entre_carriles = 90  # separación entre cada flecha, ajústalo a gusto
    ancho_total_grupo = espacio_entre_carriles * (len(nombres) - 1)
    x_inicio = (WIDTH - ancho_total_grupo) / 2

    carriles = []
    for i, nombre in enumerate(nombres):
        x = x_inicio + espacio_entre_carriles * i
        carriles.append(Lane(nombre, x))

    return carriles


TECLA_PYGAME = {
    "LEFT": [pygame.K_a, pygame.K_LEFT],
    "DOWN": [pygame.K_s, pygame.K_DOWN],
    "UP": [pygame.K_w, pygame.K_UP],
    "RIGHT": [pygame.K_d, pygame.K_RIGHT],
}

def intentar_acierto(nombre_carril, notas, ventana_acierto_px=40):
    hit_y = HEIGHT - 80
    mejor_nota = None
    menor_distancia = float("inf")

    for nota in notas:
        if nota.resuelta or nota.carril.nombre != nombre_carril:
            continue
        distancia = abs(nota.y - hit_y)
        if distancia < menor_distancia:
            menor_distancia = distancia
            mejor_nota = nota

    if mejor_nota and menor_distancia <= ventana_acierto_px:
        mejor_nota.resuelta = True
        mejor_nota.acierto = True
        return True

    return False

def start(app, xp, id):
    try:
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
        clock = pygame.time.Clock()
        fuente = pygame.font.SysFont("Arial", 24)

        video = cv2.VideoCapture("images/games/fnf/Amlo_vidio.mp4")

        pygame.mixer.music.load("audio/fnf/2.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        sonido_hit = pygame.mixer.Sound("audio/fnf/hit_sound.mp3")

        carriles = crear_carriles()
        notas = []
        velocidad_nota = 150
        intervalo_spawn = 1200
        ultimo_spawn = pygame.time.get_ticks()

        aciertos = 0
        intentos = 0
        mensaje_feedback = ""

        duracion_sesion_ms = 60000
        tiempo_inicio = pygame.time.get_ticks()
        tiempo_restante = duracion_sesion_ms
        estado = "jugando"
        
        BPM = 128
        segundos_por_beat = 60 / BPM
        beats_por_nota = 2
        intervalo_spawn = segundos_por_beat * beats_por_nota * 1000 

        running = True
        while running:
            dt = clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if estado == "jugando" and event.type == pygame.KEYDOWN:
                    for carril in carriles:
                        if event.key == TECLA_PYGAME[carril.tecla][0] or event.key == TECLA_PYGAME[carril.tecla][1]:
                            if intentar_acierto(carril.nombre, notas):
                                aciertos += 1
                                intentos += 1
                                mensaje_feedback = "¡Bien!"
                                sonido_hit.play()

            if estado == "jugando":
                tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
                tiempo_restante = max(0, duracion_sesion_ms - tiempo_transcurrido)

                if tiempo_restante == 0:
                    estado = "resumen"
                    pygame.mixer.music.stop()

                ahora = pygame.time.get_ticks()
                if ahora - ultimo_spawn > intervalo_spawn:
                    carril_random = random.choice(carriles)
                    notas.append(Nota(carril_random, velocidad_nota))
                    ultimo_spawn = ahora

                for nota in notas:
                    nota.actualizar(dt)

                for nota in notas:
                    if nota.fuera_de_pantalla() and not nota.resuelta:
                        intentos += 1
                        mensaje_feedback = "Intenta de nuevo"

                notas = [n for n in notas if not n.fuera_de_pantalla()]

            ret, frame = video.read()
            if not ret:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = video.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            screen.blit(frame, (0, 0))

            if estado == "jugando":
                for carril in carriles:
                    carril.dibujar(screen)
                for nota in notas:
                    nota.dibujar(screen)

                texto_contador = fuente.render(f"Aciertos: {aciertos}/{intentos}", True, (230, 230, 230))
                screen.blit(texto_contador, (20, 20))

                texto_feedback = fuente.render(mensaje_feedback, True, (0, 255, 170))
                screen.blit(texto_feedback, (20, 60))

                segundos_restantes = tiempo_restante // 1000
                texto_tiempo = fuente.render(f"Tiempo: {segundos_restantes}s", True, (230, 230, 230))
                screen.blit(texto_tiempo, (WIDTH - 160, 20))

            elif estado == "resumen":
                result.results(app, intentos - aciertos, aciertos * 10, id, xp)
                pygame.quit()
                '''porcentaje = int((aciertos / intentos) * 100) if intentos > 0 else 0
                titulo = fuente.render("Sesión completada", True, (0, 255, 170))
                screen.blit(titulo, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
                resultado = fuente.render(f"Aciertos: {aciertos}/{intentos}  ({porcentaje}%)", True, (230, 230, 230))
                screen.blit(resultado, (WIDTH // 2 - 130, HEIGHT // 2 - 20))'''

            pygame.display.flip()

        pygame.quit()
    except:
        pass