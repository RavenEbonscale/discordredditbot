import discord,os,random,re
from discord.ext import commands
import praw
import time
from dotenv import load_dotenv

import concurrent.futures

#Raven made this one
import redditcommand

exts ={

}

load_dotenv('discord.env')
TOKEN = os.getenv('Discord_token')

bot = commands.Bot(command_prefix='!')

bot.remove_command('help')

reddit = praw.Reddit(
    client_id= os.getenv('client_id'),
    client_secret =os.getenv('client_secret'),
    user_agent =os.getenv('user_agent') )


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error,commands.CommandNotFound):
        print('error')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')
    severs = list(bot.guilds)
    for sever in severs:
        print(f'{bot.user} in connected to {sever}')


@bot.command(name='sub')
async def reddit_fun(ctx,sub):
    #This is how you limit the channel the bot will work on
    #if ctx.message.channel.name == 'nsfw-images':
    submissions = list(reddit.subreddit(sub).hot(limit = 100))
    #helper fucntion in redditcommand.py file
    urls = await redditcommand.geturls(submissions)
    #checks to make sure there is an actual url in the list or else there will be an endless loop
    if len(urls) != 0:
    #This will loop the bot through until it can find a imaage to send
        blewup = True
        while blewup == True:
            try:
                post = random.choice(urls)
                print(f'The Choice was {post}!')
                await ctx.message.channel.send(post)
                blewup =False
            except:
                 pass
        #else:
            #pass
        print(f'sent to {ctx.message.channel} ^.^')

    else:
       await ctx.send('Sorry this sub dosent have any links i can use')
    print(ctx.message.channel.name)


@bot.command(name='help')
async def help_message(ctx):
    #I'll update this later
    author = ctx.author
    await author.send('Use !sub (name-of-sub-here) to get a response\n Ex: !sub pics')


@bot.command(name='top')
async def top(ctx,sub,num= 10,category = None ):
    try:
        submissions = list(reddit.subreddit(sub).hot(limit = int(num)))
        #checks to make sure there is an actual url in the list or else there will be an endless loop
        urls = await redditcommand.geturls(submissions)
        if len(urls) != 0:
            for url in urls:
                try:
                    await ctx.message.channel.send(url)
                except:
                    pass
        else:
            await ctx.send('Sorry this sub dosent have any links i can use')
        print(f'sent to {ctx.message.channel} @ {ctx.message.guild} ^.^')
    except commands.CommandInvokeError as e:
        pass

bot.run(TOKEN)
