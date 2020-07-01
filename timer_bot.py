import asyncio
import datetime
import os

from discord_timer import DiscordTimer
import discord

client = discord.Client()

TOKEN = os.getenv('DISCORD_TOKEN', '')


def manage_play_error(error):
    if error is not None:
        print(error)
    else:
        print("Sound played correctly.")


async def play_sound(channel, sound="b15.mp3"):
    # create StreamPlayer
    vc = await channel.connect()
    sound = discord.FFmpegPCMAudio(sound)
    vc.play(sound, after=manage_play_error)
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


async def change_channel_name(channel, channel_name, activity, remaining_time_str):
    finished = remaining_time_str == "00:00"
    if finished:
        activity = ""
        remaining_time_str = ""
    if channel is not None:
        new_channel_name = "{channel_name} {activity} {remaining_time}".format(
            channel_name=channel_name,
            activity=activity,
            remaining_time=remaining_time_str
        )
        print(datetime.datetime.now(), " change channel name to: ", new_channel_name)
        await channel.edit(name=new_channel_name)
        print(datetime.datetime.now(), " channel name changed")


def parse_time_from_message(message):
    message_parts = message.split()
    time = message_parts[-1]
    return time


def format_timer_remaining_string(timer):
    remaining_string = timer.get_remaining_time_string().split(":")
    return "{}:{}".format(remaining_string[0], remaining_string[1])


async def update_working_channel(timer):
    remaining_time_str = format_timer_remaining_string(timer)
    channel_name = "Oficina"
    activity = "\U0001F9D0"
    guild = timer.get_guild()
    channel = get_channel_by_name(guild, channel_name, "voice")
    await change_channel_name(channel, channel_name, activity, remaining_time_str)


async def update_resting_channel(timer):
    remaining_time_str = format_timer_remaining_string(timer)
    channel_name = "Oficina"
    activity = "\U0001F5E8"
    guild = timer.get_guild()
    channel = get_channel_by_name(guild, channel_name, "voice")
    await change_channel_name(channel, channel_name, activity, remaining_time_str)


def get_channel_by_name(guild, channel_name, type):
    """

    :param guild:
    :param channel_name: string with channel name
    :param type: "voice" or "text"
    :return:
    """
    channel = discord.utils.find(lambda c: channel_name in c.name and c.type.name == type, guild.channels)
    return channel


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$Empezamos a trabajar!'):
        end_time = parse_time_from_message(message.content)
        timer = DiscordTimer(end_time, update_working_channel, message.guild)
        await message.channel.send('OK! Cada 5 minutos  voy a actualizar el nombre del canal de Oficina'
                                   ' para que sepan cuanto falta.')
        await timer.run()
        await message.channel.send('Listo!')
        await play_sound(get_channel_by_name(message.guild, "Oficina", "voice"))

    if message.content.startswith('$Empieza el descanso!'):
        end_time = parse_time_from_message(message.content)
        timer = DiscordTimer(end_time, update_resting_channel, message.guild)
        await message.channel.send('OK!')
        await timer.run()
        await message.channel.send('Terminó el descanso!')
        await play_sound(get_channel_by_name(message.guild, "Oficina", "voice"))

    if message.content.startswith('$campana'):
        await message.channel.send('OK!')
        channel_name = "Oficina"
        channel = get_channel_by_name(message.guild, channel_name, "voice")
        await play_sound(channel)


client.run(TOKEN)
