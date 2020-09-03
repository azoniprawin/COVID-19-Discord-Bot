# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord.ext import tasks
import requests

TOKEN = ""
client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
	file = open("stats_logs.txt", "a")
	file.write("Bot is ready.")
	file.close()

@client.command()
async def country(ctx, *, country_name):
	try:
		country_name = country_name.lower().replace(" ", "-")
		headers = {"Content-Type": "application/json"}
		url = "https://api.covid19api.com/summary"
		message_string = ""
		request_object = requests.get(url, headers=headers)
		if(str(request_object.status_code).startswith("2")):
			json_data = request_object.json()
			for country_data in json_data["Countries"]:
				if(country_data["Country"].lower() == country_name or country_data["Slug"].lower() == country_name):
					message_string = f"**{country_data['Country']}**\nTotal Confirmed: {country_data['TotalConfirmed']}\nTotal Deaths: {country_data['TotalDeaths']}\nTotal Recovered: {country_data['TotalRecovered']}"
					break
			if(message_string == ""):
				message_string = "No data"
		else:
			message_string = "No data"
		embed = discord.Embed(title="COVID-19", description=message_string, color=(0xF48D1))
		await ctx.send(embed=embed)
	except Exception as error:
		file = open("stats_logs.txt", "a")
		file.write("Error:" + str(error) + ".\n")
		file.close()

client.run(TOKEN)