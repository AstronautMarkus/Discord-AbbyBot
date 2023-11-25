import discord
from discord.ext import commands
import sqlite3


bot = commands.Bot(command_prefix="abby_", intents=discord.Intents.all())


# Conectar a la base de datos SQLite
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name} - {bot.user.id}')


@bot.command(name='sabiduria', help='Envía un mensaje aleatorio desde la base de datos')
async def mensaje_aleatorio(ctx):
    # Obtener un mensaje aleatorio de la base de datos
    cursor.execute("SELECT contenido FROM mensajes ORDER BY RANDOM() LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        mensaje = resultado[0]
        await ctx.send(f'# ᴜɴ ᴄᴏɴꜱᴇᴊᴏ ꜱᴀʙɪᴏ ᴘᴀʀᴀ ᴜꜱᴛᴇᴅ: ')
        await ctx.send(f'## {mensaje}')
    else:
        await ctx.send('No hay mensajes en la base de datos.')


@bot.command(name='consejos', help='Envía un mensaje aleatorio desde la base de datos')
async def mensaje_aleatorio(ctx, cantidad: int = 1):
    if cantidad <= 0:
        await ctx.send('Por favor, ingrese un número positivo mayor que cero.')
        return

    for _ in range(cantidad):
        # Obtener un mensaje aleatorio de la base de datos
        cursor.execute("SELECT contenido FROM mensajes ORDER BY RANDOM() LIMIT 1")
        resultado = cursor.fetchone()

        if resultado:
            mensaje = resultado[0]
            await ctx.send(f'# ᴜɴ ᴄᴏɴꜱᴇᴊᴏ ꜱᴀʙɪᴏ ᴘᴀʀᴀ ᴜꜱᴛᴇᴅ: ')
            await ctx.send(f'## {mensaje}')
        else:
            await ctx.send('No hay mensajes en la base de datos.')

@bot.command(name='fumo_img', help='Envía una imagen aleatoria desde la base de datos')
async def imagen_aleatoria(ctx):

    # Obtener una ruta local de imagen aleatoria de la base de datos
    cursor.execute("SELECT ruta_local FROM imagenes ORDER BY RANDOM() LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        ruta_local = resultado[0]

        # Enviar la imagen local
        with open(ruta_local, 'rb') as imagen_file:
            await ctx.send('Aquí tiene su fumo:')
            await ctx.send(file=discord.File(imagen_file, filename='imagen.png'))
    else:
        await ctx.send('No hay imágenes en la base de datos.')


@bot.command(name='codear')
async def codear(ctx, *, codigo):
    # Envia el mensaje con el código formateado

    await ctx.message.delete()

    await ctx.send(f"```\n{codigo}\n```")


@bot.command(name='saludar')
async def saludar(ctx):
    await ctx.send(f'Hola, {ctx.author.name}!')


@bot.command()
async def buenos_dias(ctx):


    await ctx.message.delete()
    # Crea un objeto Embed
    embed = discord.Embed(title="Buenos días!", description="Excepto a los Chinos que allá es de noche.", color=0x00ff00)

    # Añade campos al Embed (opcional)
    embed.add_field(name='''
    ¡Buenos días! 🌞🐦 Que tu día esté lleno de alegría y energía positiva. ¡A volar alto como los pajaritos! 🕊️✨''', value="AbbyBot", inline=False)

    # Puedes añadir más configuraciones al Embed según tus necesidades

    cursor.execute("SELECT ruta_local FROM bot_img WHERE ID = 1")
    resultado = cursor.fetchone()

    if resultado:
        ruta_local = resultado[0]
    
        with open(ruta_local, 'rb') as imagen_file:
            
            embed.set_image(url='attachment://imagen.png')
            file = discord.File(imagen_file, filename='imagen.png')

            # Enviar el embed con la imagen
            await ctx.send(embed=embed, file=file)





bot.run("SECRETO")