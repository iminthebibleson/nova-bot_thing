import asyncio
import random
import requests
import discord
import datetime
from discord.ext import bridge, commands
import time
from datetime import date
import calendar
import time; time.time()
import calendar, time; calendar.timegm(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S'))
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = discord.Bot(intents=intents)
bot = bridge.Bot(command_prefix=".", intents=intents)
today = datetime.datetime.now(datetime.timezone.utc)
date = date.today()
def probably(chance):
    return random.random() < chance

@bot.slash_command(name="contact", description="Shows contact info", help="Shows contact info")
async def contact(ctx):
    embed = discord.Embed(description="For any inquiries/issues, please contact @RoyceClub1 on x.com, richclubtm on discord, and royceclub32@gmail.com. Please give us up to 4 business days to get to your inquiries.\n\nYou may also contact ChangeNOW at: support@changenow.io for any queries related to conversions")

    await ctx.respond(embed=embed)


@bot.slash_command(name="exchange")
async def exchange(ctx):
    profile_photo_url = ctx.author.display_avatar.url
    embed = discord.Embed(title="Exchange",description="Sure, what currencies would that be?",colour=0x800080)
    embed.set_thumbnail(url=profile_photo_url)
    embed.set_footer(text="Nova Bot")
    await ctx.respond(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        currencies_message = await bot.wait_for('message', check=check, timeout=30)
        currencies = currencies_message.content.split()
        
        if len(currencies) != 3:
            embed = discord.Embed(title="Exchange",description="Invalid input. Please provide input currency, output currency, and output wallet.",colour=0x800080)
            embed.set_thumbnail(url=profile_photo_url)
            embed.set_footer(text="Nova Bot")

            await ctx.respond(embed=embed)
            return
        
        input_currency, output_currency, output_wallet = currencies

        embed = discord.Embed(title="Exchange",description="Enter Amount:",colour=0x800080)
        embed.set_thumbnail(url=profile_photo_url)
        embed.set_footer(text="Nova Bot")
        await ctx.respond(embed=embed)
        amount_message = await bot.wait_for('message', check=check, timeout=30)
        amount = int(amount_message.content)

        embed = discord.Embed(title="Exchange",description="Enter Address:",colour=0x800080)
        embed.set_thumbnail(url=profile_photo_url)
        embed.set_footer(text="Nova Bot")
        await ctx.respond(embed=embed)
        in_wallet_message = await bot.wait_for('message', check=check, timeout=30)
        in_wallet = in_wallet_message.content

        valid_currencies = ['SOL', 'ADA', 'XMR', 'XRP', 'LTC', 'BTC', 'ETH', 'BNB', 'TRX', 'MATIC']
        
        if input_currency not in valid_currencies or output_currency not in valid_currencies:
            embed = discord.Embed(title="Exchange",description="Invalid currency, please try again.",colour=0x800080)
            embed.set_thumbnail(url=profile_photo_url)
            embed.set_footer(text="Nova Bot")
            await ctx.respond(embed=embed)
            return

        # Replace 'YOUR_API_KEY' with your ChangeNOW API key
        url = f'https://changenow.io/api/v2/exchange?output_currency={output_currency}&output_wallet={in_wallet}&input_amount={amount}&input_currency={input_currency}&key=03db3c586bd0f30d8e0a4f7f13affe922f30adbcd6ec18dd6c23e3058a636049'

        response = requests.get(url)
        
        if response.status_code == 200:
            embed = discord.Embed(title="Exchange",description=('Exchange successful!\nResponse: {response.json()}'),colour=0x800080)
            embed.set_thumbnail(url=profile_photo_url)
            embed.set_footer(text="Nova Bot")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Exchange",description=(f'Exchange failed. Status code: {response.status_code}'),colour=0x800080)
            embed.set_thumbnail(url=profile_photo_url)
            embed.set_footer(text="Nova Bot")
            await ctx.respond(embed=embed)

    except asyncio.TimeoutError:
        embed = discord.Embed(title="Exchange",description=('Exchange request timed out.'),colour=0x800080)
        embed.set_thumbnail(url=profile_photo_url)
        embed.set_footer(text="Nova Bot")
        await ctx.respond(embed=embed)


@bot.slash_command(name="get_currencies", description="lists all the currency", help="lists all the currency")
async def get_currencies(ctx):
    try:
        response = requests.get('https://api.changenow.io/v1/currencies?active=true')
        
        profile_photo_url = ctx.author.display_avatar.url

        if response.status_code == 200:
            data = response.json()
            currencies = [entry['name'] for entry in data]

            per_page = 10
            pages = [currencies[i:i + per_page] for i in range(0, len(currencies), per_page)]

            current_page = 0

            embed = discord.Embed(
                title="Currency List",
                description="List of active currencies from the ChangeNOW API",
                color=discord.Color.green()
            )

            for i, currency in enumerate(pages[current_page]):
                embed.add_field(name=f"**{currency}**", value="", inline=False)
                embed.set_thumbnail(url=profile_photo_url)

            await ctx.respond("Loading...", delete_after=3)
            message = await ctx.send(embed=embed)

            if len(pages) > 1:
                await message.add_reaction('⬅️')
                await message.add_reaction('➡️')

                def check(reaction, user):
                    return user == ctx.author and reaction.message == message and str(reaction.emoji) in ['⬅️', '➡️']

                while True:
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

                        if str(reaction.emoji) == '➡️' and current_page < len(pages) - 1:
                            current_page += 1
                        elif str(reaction.emoji) == '⬅️' and current_page > 0:
                            current_page -= 1

                        embed.clear_fields()

                        for i, currency in enumerate(pages[current_page]):
                            embed.add_field(name=f"**{currency}**", value="", inline=False)
                            embed.set_thumbnail(url=profile_photo_url)

                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    
                    except asyncio.TimeoutError:
                        await message.clear_reactions()
                        break
        else:
            await ctx.respond(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        await ctx.respond(f'An error occurred: {e}')


async def simple_text_paginator(ctx, pages):
    current_page = 0

    embed = discord.Embed(
        title="Text Paginator",
        description=pages[current_page],
        color=discord.Color.blue()
    )

    await ctx.respond("loading...", delete_after=3)
    message = await ctx.send(embed=embed)

    if len(pages) > 1:
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction, user):
            return user == ctx.author and reaction.message == message and str(reaction.emoji) in ['⬅️', '➡️']

        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '➡️' and current_page < len(pages) - 1:
                    current_page += 1
                elif str(reaction.emoji) == '⬅️' and current_page > 0:
                    current_page -= 1

                embed.description = pages[current_page]

                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

@bot.slash_command(name="tos", description="shows the terms of service", help="shows the terms of service")
async def tos(ctx):
    # Example list of pages (replace with your content)
    pages = [
        "**Terms Of Service** | **Page 1/4**\n\n> *1. This Terms of Service (TOS) governs the use of the \"Bot,\" an open-source software that assists users in processing crypto cross-chain transactions using ChangeNow (referred to as \"ChangeNow\" throughout this document).\n> The use of the Bot is free of charge, with a nominal fee applied in the form of trading fees. The Bot owner is not responsible for handling or resolving any complaints relating to fund locks. ChangeNow's ToS also apply.*\n\n> *2. Disclosures and Limitations of Liability\n> The Bot is provided on an \"as is\" basis. The Bot owner, any developers associated with the Bot, and any endorsers or sponsors are not responsible for any losses, damages, or liabilities. This includes, but is not limited to, damages caused by misappropriation, misuse, misrepresentation, and fraudulent activities by the user.*\n\n> *3. The user hereby agrees that the risk of financial loss associated with using the Bot rests entirely with the user. The user also agrees to hold harmless the Bot owner, the developers, and any endorsers or sponsors associated with the Bot. Finally, the user agrees to immediately report any fraudulent activities to the appropriate authorities, including but not limited to ChangeNow and any relevant regulatory or government entity.*\n\n> *4. In case of disputes, these Terms of Service shall be governed and interpreted in accordance with the laws of the United States. Any dispute arising out of or relating to these Terms of Service shall be finally resolved by binding arbitration through an arbitrator to be mutually agreed upon. In the event the parties are unable to agree upon an arbitrator, then either party may apply to a federal court of appropriate jurisdiction for relief. Any award of damages or other relief shall not exceed $50,000 per incident or occurrence, and shall be payable in United States dollars.*\n\n> *5. The Bot owner is not making any representation or warranty regarding the content, accuracy, or results achieved with this Bot. This includes any implied warranties of merchantability, fitness for a particular purpose, or non-infringement. The user agrees that the use of this Bot is at their own risk, and waives any liability claims arising out of or related to the use of this Bot. Please review the ChangeNow ToS for further information.*",
        "**Terms Of Service** | **Page 2/4**\n\n> *6. These Terms of Service are the entire agreement between the parties, and supersede all previous agreements or understanding with respect to the subject matter of these Terms of Service. Any additional terms proposed by the user shall not apply and shall be deemed non-binding.*\n\n> *7. These Terms of Service shall not be modified or amended except in writing and with the mutual consent of the Bot owner and the user.\n> No waiver by either party of a breach of any provision of these Terms of Service shall operate as a waiver of any other right or provision. No prior waiver by the Bot owner shall limit its right to enforce these Terms of Service to the full extent permitted by law.*\n\n> *8. The Bot owner reserves the right to modify or change these Terms of Service at any time, without notice. Upon publishing the modified Terms of Service, the Bot owner shall notify the user in Writing. Once the user receives such notification, they are expected to review and either accept or reject the terms within a reasonable time period. Continued use of the Bot following notice of any modification shall be deemed acceptance of such modified Terms of Service.*\n\n> *9. In the event the Bot owner discontinues the Bot or makes fundamental changes to the Bot, the user agrees to terminate their use of the Bot, including removing the Bot software and any associated files from their computer or servers. Failure to immediately terminate the Bot will be considered acceptance by the user of the discontinuation or alteration of the Bot. These Terms of Service shall be binding on the parties and their respective heirs, assigns, legal representatives, and any subsequent owners of the user's or Bot owner's business.*\n\n> *10. The Bot owner is not liable for any damages, including but not limited to special or consequential damages, incurred by the user or their business due to the discontinuation or alteration of the Bot. Such damages are the sole responsibility of the user. The Bot owner is also not responsible for losses in data or any other losses incurred by the user as a result of the discontinuation or alteration of the Bot.*",
        "**Terms Of Service** | **Page 3/4**\n\n> *11. The provisions and obligations of this TOS shall survive the expiration, termination, or cancellation of the user's use of the Bot. Upon cancellation of the user's use, the user shall delete all instances of the Bot from their computer and servers and immediately delete all saved data and information related to their use of the Bot.*\n\n> *12. In the event of a tie, or any ambiguity or conflict between these Terms of Service and the ChangeNow ToS, these Terms of Service shall apply.*\n\n> *13. These Terms of Service represent the final and exclusive understanding and agreement between the User and the Bot owner, with respect to the subject matter. Any modification or amendment to this agreement shall not be effective unless signed by the Bot owner or provided in Writing by the Bot owner. Any previous agreements or understandings with the Bot owner regarding the subject matter do not modify or supersede these Terms of Service.*\n\n> *14. Unless otherwise specified in these Terms of Service, each of the terms and obligations within this document shall be severable: if a court, arbitrator, judge or other form of dispute resolution rules that one or more of these terms is unenforceable or otherwise unenforceable against the user, those terms are to be treated as nonexistent and the rest of these terms are allowed to take full effect. Unless otherwise specified, all references to \"you\" and \"your\" shall refer to the specific user or users listed on the Agreement. All references to \"we\" or \"us\" refer to the Bot owner.*\n\n> *15. Any and all legal disputes, complaints and disagreements between you and the Bot owner concerning or relating to the subject matter, use, or non-use of this Discord Bot, and the interpretation, enforceability, or application of these Terms of Service shall be resolved exclusively through binding arbitration in accordance with the Federal Arbitration Act, without resort to any other remedy.*",
        "**Terms Of Service** | **Page 4/4**\n\n> *16. You agree that any claims, disputes, and allegations you may have against the Bot owner must be submitted to binding arbitration in accordance with these Terms of Service for resolution. You also agree that you will not participate in any group action regarding the subject matter of this agreement, including in any class action suit or any other form of group proceeding.*\n\n> *17. You and the Bot owner agree to use good faith efforts and reasonable diligence regarding any disputes or claims that are submitted to arbitration.*"
    ]

    await simple_text_paginator(ctx, pages)


@bot.bridge_command(name="currency_info", description="shows info about the currency", help="shows info about the currency")
async def currency_info(ctx, *, currency_name):
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/markets', params={'vs_currency': 'usd', 'ids': currency_name})
        
        if response.status_code == 200 and response.json():
            data = response.json()[0]  # We assume the first result is the closest match
            
            name = data['name']
            symbol = data['symbol']
            image_url = data['image']
            description = data.get('description', 'No description available.')
            current_price = data.get('current_price', 0)
            market_cap = data.get('market_cap', 0)
            total_volume = data.get('total_volume', 0)

            embed = discord.Embed(
                title=f"{name} ({symbol})",
                description=description,
                color=discord.Color.purple()
            )
            
            embed.set_thumbnail(url=image_url)

            embed.add_field(name="Current Price (USD)", value=f"${current_price:.2f}", inline=False)
            embed.add_field(name="Market Cap (USD)", value=f"${market_cap:.2f}", inline=False)
            embed.add_field(name="Total 24h Volume (USD)", value=f"${total_volume:.2f}", inline=False)

            await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"Failed to fetch data for '{currency_name}'. Make sure the currency name is valid.")
    except Exception as e:
        await ctx.respond(f'An error occurred: {e}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass


@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Deploying Nova Members And Suffering")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"i hope it works now | signed in as {bot.user} | bot ID: {bot.user.id}")
    bot.run("imagine")
