import pygame
import random
from games.fnf.config_fnf import WIDTH, HEIGHT, COLOR_BG, COLOR_LANE_LINE, LANE_COLORS, LANE_KEYS


class Lane:
    def __init__(self, nombre, x):
        self.nombre = nombre
        self.x = x
        self.color = LANE_COLORS[nombre]
        self.tecla = LANE_KEYS[nombre]

    def dibujar(self, screen):
        pygame.draw.line(screen, COLOR_LANE_LINE, (self.x, 0), (self.x, HEIGHT), 2)
        hit_y = HEIGHT - 80
        pygame.draw.circle(screen, self.color, (int(self.x), hit_y), 28, 3)


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
        color = self.carril.color if not self.resuelta else (90, 90, 90)
        pygame.draw.circle(screen, color, (int(self.carril.x), int(self.y)), 16)

    def fuera_de_pantalla(self):
        return self.y > HEIGHT + 40


def crear_carriles():
    nombres = ["izq", "aba", "arr", "der"]
    margen = 100
    espacio_util = WIDTH - margen * 2
    carriles = []

    for i, nombre in enumerate(nombres):
        x = margen + (espacio_util / (len(nombres) - 1)) * i
        carriles.append(Lane(nombre, x))

    return carriles


TECLA_PYGAME = {
    "LEFT": pygame.K_LEFT,
    "DOWN": pygame.K_DOWN,
    "UP": pygame.K_UP,
    "RIGHT": pygame.K_RIGHT,
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

def iniciar_juego():
    try:
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("FNF buenestar")
        clock = pygame.time.Clock()
        fuente = pygame.font.SysFont("Arial", 24)

        pygame.mixer.music.load("audio/fnf/bg.mp3")
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
                        if event.key == TECLA_PYGAME[carril.tecla]:
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

            screen.fill(COLOR_BG)

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
                porcentaje = int((aciertos / intentos) * 100) if intentos > 0 else 0
                titulo = fuente.render("Sesión completada", True, (0, 255, 170))
                screen.blit(titulo, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
                resultado = fuente.render(f"Aciertos: {aciertos}/{intentos}  ({porcentaje}%)", True, (230, 230, 230))
                screen.blit(resultado, (WIDTH // 2 - 130, HEIGHT // 2 - 20))

            pygame.display.flip()

        pygame.quit()
    except:
        pass
