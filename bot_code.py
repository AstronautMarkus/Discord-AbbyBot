import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sqlite3
import random



# Cargar variables de entorno desde el archivo .env
load_dotenv('access.env')

# Obtener el token del bot desde las variables de entorno
TOKEN = os.getenv('DISCORD_TOKEN')

# Conectar a la base de datos SQLite
conn = sqlite3.connect('mi_base_de_datos.db')
cursor = conn.cursor()

# Crear una tabla si no existe
# cursor.execute('''CREATE TABLE IF NOT EXISTS mensajes (
#                     id INTEGER PRIMARY KEY,
#                     contenido TEXT
#                 )''')


# Definir los intents que necesita el bot
intents = discord.Intents.default()
intents.all()

# Crear un objeto bot con un prefijo personalizado y los intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='mensaje_aleatorio', help='Envía un mensaje aleatorio desde la base de datos')
async def mensaje_aleatorio(ctx):
    # Obtener un mensaje aleatorio de la base de datos
    cursor.execute("SELECT contenido FROM mensajes ORDER BY RANDOM() LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        mensaje = resultado[0]
        await ctx.send(mensaje)
    else:
        await ctx.send('No hay mensajes en la base de datos.')

@bot.command(name='imagen_aleatoria', help='Envía una imagen aleatoria desde la base de datos')
async def imagen_aleatoria(ctx):
    # Obtener una ruta local de imagen aleatoria de la base de datos
    cursor.execute("SELECT ruta_local FROM imagenes ORDER BY RANDOM() LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        ruta_local = resultado[0]

        # Enviar la imagen local
        with open(ruta_local, 'rb') as imagen_file:
            await ctx.send(file=discord.File(imagen_file, filename='imagen.png'))
    else:
        await ctx.send('No hay imágenes en la base de datos.')

# Evento cuando el bot se ha conectado correctamente
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name} - {bot.user.id}')

# Comando simple para saludar al bot
@bot.command(name='saludar', help='Saluda al bot')
async def saludar(ctx):
    await ctx.send(f'Hola {ctx.author.mention}!')

@bot.command(name='info_bot', help='Saluda al bot')
async def bot_info(ctx):
    await ctx.send(f'Conectado como {bot.user.name} - {bot.user.id}')

# Ejecutar el bot con el token proporcionado
bot.run(TOKEN)

# Cerrar la conexión a la base de datos al cerrar el bot
conn.close()
