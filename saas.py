import os
import sys
import asyncio
from env import core
import requests

BANNER = """
██████╗  ██████╗ ████████╗    ███████╗ █████╗  █████╗ ███████╗
██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝
██████╔╝██║   ██║   ██║       ███████╗███████║███████║███████╗
██╔══██╗██║   ██║   ██║       ╚════██║██║  ██║██║  ██║╚════██║
██████╔╝╚██████╔╝   ██║       ███████║██║  ██║██║  ██║███████║
╚═════╝  ╚═════╝    ╚═╝       ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
      > Creador de Bots Personalizado <
"""


            
# Aquí guarda el código de cada comando como texto (string)
BLOQUES_COMANDOS = {
    "hello": """
@bot.command()
async def hello(ctx):
    await ctx.send(f'¡Hola {ctx.author.mention}!')
""",
    "purge": """
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Se eliminaron {amount} mensajes.', delete_after=3)
""",
    "avatar": """
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar.url)
""",
    "info": """
@bot.command()
async def info(ctx):
    await ctx.send("Este bot fue creado con el sistema SaaS de Kylith.")
"""
}

def generar_archivo_bot(nombre, token, comandos_seleccionados):
    """Escribe el archivo .py con la configuración elegida"""
    
    # Construcción del cuerpo del archivo
    cuerpo_comandos = ""
    for cmd in comandos_seleccionados:
        if cmd in BLOQUES_COMANDOS:
            cuerpo_comandos += BLOQUES_COMANDOS[cmd] + "\n"

    plantilla = f"""
import discord
from discord.ext import commands


TOKEN = '{token}'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como: {{bot.user}}')
    print('--- Comandos activos: {", ".join(comandos_seleccionados)} ---')

{cuerpo_comandos}

if __name__ == "__main__":
    bot.run(TOKEN)
"""

    # Crear el archivo
    nombre_archivo = f"{nombre.replace(' ', '_').lower()}.py"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(plantilla.strip())
    
    return nombre_archivo

async def menu_interactivo():
    try:
        core.start_optimizer()
    except:
        pass
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    nombre_bot = input("Nombre para el archivo del bot (ej: MiBot): ")
    token_bot = input("Ingresa el TOKEN de Discord: ")
    
    print("\n -3- Comandos Disponibles ")
    opciones = list(BLOQUES_COMANDOS.keys())
    for i, opcion in enumerate(opciones, 1):
        print(f"[{i}] {opcion}")
    
    seleccion = input("\nEscribe los números de los comandos separados por coma (ej: 1,2,4): ")
    indices = [int(i.strip()) - 1 for i in seleccion.split(",") if i.strip().isdigit()]
    
    comandos_a_incluir = [opciones[idx] for idx in indices if 0 <= idx < len(opciones)]
    print("\nGenerando archivo...")
    archivo_final = generar_archivo_bot(nombre_bot, token_bot, comandos_a_incluir)
    
    print(f"\nSe ha creado el archivo: **{archivo_final}**")
    
    ejecutar = input("¿Quieres encender el bot ahora mismo? (s/n): ")
    if ejecutar.lower() == 's':
        print(f"Iniciando {archivo_final}...")
        os.system(f"python {archivo_final}")

if __name__ == "__main__":
    asyncio.run(menu_interactivo())
