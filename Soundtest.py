import pygame as pg
import sounddevice as sd


# Налаштування аудіо
fs = 44100
chunk = 1024


# Налаштування вікна
width, height = 800, 400
pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Live Audio (mic)")
clock = pg.time.Clock()


# Буфер для даних
data = [0.0] * chunk




def audio_callback(indata, frames, time_info, status):
   global data
   if status:
       print(status)
   # Масштабуємо амплітуду під половину висоти екрана
   data = [sample * (height // 2) for sample in indata[:, 0].tolist()]




# Запуск стриму мікрофона
stream = sd.InputStream(
   callback=audio_callback,
   channels=1,
   samplerate=fs,
   blocksize=chunk,
   dtype="float32"
)
stream.start()


running = True
while running:
   for e in pg.event.get():
       if e.type == pg.QUIT:
           running = False


   screen.fill((0, 0, 0))


   # Побудова точок для лінії
   points = []
   for i, sample in enumerate(data):
       x = int(i * width / chunk)
       y = int(height / 2 + sample)
       # Обмежуємо y, щоб лінії не вилітали за межі екрана
       y = max(0, min(height - 1, y))
       points.append((x, y))


   if len(points) > 1:
       pg.draw.lines(screen, (0, 255, 0), False, points, 2)


   pg.display.update()
   clock.tick(60)


stream.stop()
pg.quit()

