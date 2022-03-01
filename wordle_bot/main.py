import discord
import os

client = discord.Client()


class GameEnv:
	def __init__(self):
		self.game_board = [[':regional_indicator_g: :regional_indicator_u: :regional_indicator_e: :regional_indicator_s: :regional_indicator_s: : :regional_indicator_h: :regional_indicator_i: :regional_indicator_n: :regional_indicator_t: :regional_indicator_s:'.split(' ')],
		[':black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: : :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square:' for _ in range(6)]]

board = GameEnv()
@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$board'):
		for line in board.game_board:
			text = ''
			for char in line:
				text += char
			await message.channel.send(text)

client.run('NzMxMzU1ODk0NTYxODk4NTI3.Xwk2QQ.sSoWtXIUX_GIBLsh4yHz7QI3Pv4')