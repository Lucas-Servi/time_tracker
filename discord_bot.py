import discord
from discord.ext import commands
import time
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='!')

# A dictionary to store the start times for each user in a voice channel
start_times = {}

# A dictionary to store the total time spent by each user in the last week
weekly_times = {}

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the member joined or left a voice channel
    if before.channel is None and after.channel is not None:
        # The member joined a voice channel, so store the start time
        start_times[member.id] = time.time()
    elif before.channel is not None and after.channel is None:
        # The member left a voice channel, so calculate the total time spent in the channel
        total_time = time.time() - start_times[member.id]
        # Add the total time to the user's weekly time
        if member.id not in weekly_times:
            weekly_times[member.id] = total_time
        else:
            weekly_times[member.id] += total_time

@bot.command()
async def stats(ctx):
    # Get the start time of the last week
    start_time = datetime.now() - timedelta(days=7)
    # Create a dictionary to store the total time spent by each user in the last week
    times = {}
    for member_id, total_time in weekly_times.items():
        # Check if the user spent any time in the voice channel in the last week
        if member_id in start_times and start_times[member_id] >= start_time.timestamp():
            times[member_id] = total_time
    # Sort the users by their total time spent in the voice channel
    sorted_users = sorted(times.items(), key=lambda x: x[1], reverse=True)
    # Print the results in the chat
    message = "Weekly Stats:\n"
    for member_id, total_time in sorted_users:
        member = ctx.guild.get_member(member_id)
        message += f"{member.display_name}: {total_time:.2f} seconds\n"
    await ctx.send(message)

bot.run('MTA3ODQ1MzEyNTMwNTg2ODQyOQ.GtBjdX.YkH0M_pzfuR9sdjPZRqMaM3mUkhwOTrNegQYKY')

