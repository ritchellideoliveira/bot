import asyncio
import json
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_FILE = "role_id.json"

def save_role_id(role_id):
    with open(ROLE_FILE, "w", encoding="utf-8") as f:
        json.dump({"role_id": role_id}, f, indent=4)

def get_role_id():
    if not os.path.exists(ROLE_FILE):
        return None
    try:
        with open(ROLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("role_id")
    except Exception:
        return None

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    await bot.tree.sync()

@bot.event
async def on_member_update(before, after):
    print("ANTES:", before.premium_since)
    print("DEPOIS:", after.premium_since)
    print("MEMBRO:", after.name)

    role_id = get_role_id()
    if role_id is None:
        return

    role = after.guild.get_role(role_id)
    if role is None:
        return

    if before.premium_since is None and after.premium_since is not None:
        if role not in after.roles:
            await after.add_roles(role)
        canal = after.guild.system_channel
        if canal:
            await canal.send(f"{after.mention} começou a boostar e ganhou {role.mention}")

    if before.premium_since is not None and after.premium_since is None:
        if role in after.roles:
            await after.remove_roles(role)
        canal = after.guild.system_channel
        if canal:
            await canal.send(f"{after.mention} parou de boostar e perdeu {role.mention}")

@bot.tree.command(name="configurar", description="Configura o cargo de Double Booster")
@app_commands.default_permissions(administrator=True)
async def configurar(interaction: discord.Interaction):
    await interaction.response.send_message("Configurando...", ephemeral=True)

    guild = interaction.guild
    if guild is None:
        await interaction.edit_original_response(content="Esse comando só funciona em um servidor.")
        return

    role = discord.utils.get(guild.roles, name="Double Booster")
    if role is None:
        role = await guild.create_role(name="Double Booster")
    save_role_id(role.id)

    canal = discord.utils.get(guild.text_channels, name="notificações-boosts")
    if canal is None:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        canal = await guild.create_text_channel(
            name="notificações-boosts",
            overwrites=overwrites
        )

    await guild.edit(system_channel=canal)

    await interaction.edit_original_response(
        content=f"✅ Configuração concluída.\nCargo: {role.mention}\nCanal: {canal.mention}"
    )

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Crie um arquivo .env com DISCORD_TOKEN=SEU_TOKEN")
    async with bot:
        await bot.start(token)

asyncio.run(main())
