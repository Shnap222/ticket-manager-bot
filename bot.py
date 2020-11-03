import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', help_command=None, intents=intents)
roles = [] # the roles that can see the ban appeals
emoji = "🎫" #default ticket emoji
close_ticket = "🔒" #default close ticket emoji
final_close = "✅"#default final close ticket emoji
reopen = "⛔"##default reopen ticket emoji
transcript = "🔖"#default save ticket emoji
ticket_msg = None #saved the setup message
tickets_category = None #saves the category of the setup msg
categoryT = None # the category where the transcripts go to

transcript_rdy = False # boolean if added a category for transcripts


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with Ban appeals'))
    print('BOT ACTIVATED')


@client.command()
async def help(ctx):#shows all the commands that can be used within this bot
    help_message = discord.Embed(
        colour=discord.Color.gold(),
        description="The bot's prefix is   . "

    )
    help_message.set_author(name="Commands")
    help_message.add_field(name="```.add [role/roles]```",
                           value="Adds the role/roles that you mentioned to the roles with the ability to see Ban Appeals.\n Aliases: role_add , addRole\n Disclaimer: Added roles will only see ban appeals that are added **after** they got added, they wont see any ban appeals that were made before the role was added.",
                           inline=False)
    help_message.add_field(name="```.remove [role/roles]```",
                           value=" Removes the the role/roles you mentioned from the role list.\n Aliases: role_remove , removeRoll",
                           inline=False)
    help_message.add_field(name="```.show_list```",
                           value="Description: Shows you all the roles that are able to see the Ban Appeals.\n Aliases: showL , roleList",
                           inline=False)
    help_message.add_field(name="```.setEmoji [emoji]```",
                           value="Description: Changes the emoji that is being used in the bot msg for opening ban appeals.\nAliases: none \nDisclaimer: If you change the message's emoji, you need to make a new msg using .setup",
                           inline=False)
    help_message.add_field(name="```.setup```",
                           value="Description: Sets up the bot for tickets and sending the message.\nAliases: none\nDisclaimer: Make a new category with a new channel for the message to be in. The ban appeals will be created on the same category as the message.",
                           inline=False)
    help_message.add_field(name="```.saved_category [name of category]```",
                           value="Description: Specifies the place for the saved ban appeals to go. If there is no specefied place for the transcripts to go, it will make a category channel names 'saved ban appeals'.\nAliases: transcriptS , saveT\nDisclaimer: If there are more than 1 category with the same name and you specify that category the bot will go to the higher category with that name.",
                           inline=False)
    help_message.add_field(
        name="----------------------------------------------\nDeveloper : Shnap \nDiscord: Shnap#5581",
        value="**If there are any problems or want to make a custom bot, contact me.**")

    await ctx.send(embed=help_message)


def role_check(role):
    for i in roles:
        if role == i:
            return True
    return False


@client.command(aliases=['role_add', 'addRole'])
async def add(ctx):#adds the roles that were mentioned to the roles list
    if not ctx.message.author.guild_permissions.administrator:
        ctx.message.author.send(embed=unable_msg)
        return
    await ctx.message.delete()
    mentioned_roles = ctx.message.role_mentions
    for role in mentioned_roles:
        if not role_check(role):
            roles.append(role)
    await ctx.send("The roles have been added", delete_after=2)


@client.command(aliases=['transcriptS', 'saveT'])
async def saved_category(ctx, *, category): # gets the name of the category and remembers it as the place to save the transcripts 
    global transcript_rdy
    if not ctx.message.author.guild_permissions.administrator:
        ctx.message.author.send(embed=unable_msg)
        return
    global categoryT
    categoryT = category.lower()
    transcript_rdy = True
    await ctx.message.delete()
    await ctx.send("Saved tickets category has been updated", delete_after=2)


@client.command()
async def setEmoji(ctx, *, emojiUse): #gets an emoji and changes the ticket emoji
    global emoji
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.author.send(embed=unable_msg)
        return
    emoji = emojiUse
    await ctx.message.delete()
    await ctx.send("The emoji is now " + emoji, delete_after=2)


@client.command(aliases=['role_remove', 'removeRole'])
async def remove(ctx, *, all): #removes the role/ roles that were mentioned, can also type all to delete all roles
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.author.send(embed=unable_msg)
        return
    await ctx.message.delete()
    if all == "all":
        while roles.__len__() > 0:
            print(roles)
            roles.pop()
        await ctx.send("All the roles have been removed from the list", delete_after=2)
        return
    removed_roles = False

    for role in ctx.message.role_mentions:
        for roleL in roles:
            if role == roleL:
                roles.remove(role)
                removed_roles = True
                await ctx.send(role.name + " has been removed from the list", delete_after=2)
        if not removed_roles:
            await ctx.send("No roles have been deleted", delete_after=2)


@client.command(aliases=['showL', "roleList"])
async def show_list(ctx): #sends an embed with all the roles that can see the ban appeals
    temp_roles = []
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.author.send(embed=unable_msg)
        return
    await ctx.message.delete()
    for i in roles:
        temp_roles.append(i.name)

    if temp_roles.__len__() == 0:
        emb_roles = discord.Embed(
            title='Roles that are able to see tickets:',
            description="There are no roles that were added to the list yet",
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=emb_roles)
        return
    emb_roles = discord.Embed(
        title='Roles that are able to see tickets:',
        description="{}".format("\n".join(temp_roles)),
        colour=discord.Colour.blue()
    )
    await ctx.send(embed=emb_roles)
    return


@client.command()
async def setup(ctx):#creats the ticket opener message and deletes the last ticket opener if was one.
    global ticket_msg
    try:
        if ticket_msg is not None:
            await ticket_msg.delete()
    except:
        ticket_msg = None

    await ctx.message.delete()
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.author.send(embed=unable_msg)
        return
    global ticket_opener
    ticket_opener = discord.Embed(
        title='Ban Appeal',
        description='To create a ban appeal react with ' + emoji,
        colour=discord.Colour.blue()
    )
    ticket_opener.set_footer(text="Made by Shnap#5581")
    ticket_msg = await ctx.send(embed=ticket_opener)
    await ticket_msg.add_reaction(emoji)


@client.event
async def on_reaction_add(reaction, user):
    global transcript_rdy
    global tickets_category
    hasRole = False

    # opening ticket from the ticket 
    if reaction.message.id == ticket_msg.id and reaction.emoji == emoji and user.id != ticket_msg.author.id:
        tickets_category = reaction.message.channel.category
        if categoryT != tickets_category:
            for ch in tickets_category.channels:
                if ch.name.startswith(user.name.lower()):
                    await reaction.remove(user)
                    return
        channel_created = await tickets_category.create_text_channel(user.name + "' ban appeal")
        everyone_role = reaction.message.channel.guild.default_role
        await channel_created.set_permissions(everyone_role, send_messages=False, read_messages=False)
        await channel_created.set_permissions(user, read_messages=True, send_messages=True)
        for role in roles:
            await channel_created.set_permissions(role, read_messages=True, send_messages=True)
        await channel_created.send("Welcome " + user.mention + "!")
        temp_msg = await channel_created.send(embed=ticket_responder2)
        await temp_msg.add_reaction(close_ticket)
        await reaction.remove(user)
        return

    # closing ticket from the ticket response message
    if reaction.message.author.id == 769529065232924684 and (
            reaction.message.channel.category == tickets_category or reaction.message.channel.category.name.lower() == categoryT) and ticket_msg.channel != reaction.message.channel and user.id != reaction.message.author.id:

        for role in roles:
            for pRole in user.roles:
                if role == pRole:
                    hasRole = True
                    break
        if hasRole:
            if reaction.emoji == close_ticket:  # the close ticket emoji check
                await reaction.remove(user)
                temp_msg = await reaction.message.channel.send(embed=ticket_2step)
                await temp_msg.add_reaction(final_close)
                await temp_msg.add_reaction(reopen)
                await temp_msg.add_reaction(transcript)
                return
            elif reaction.emoji == final_close:  # the check mark emoji check
                await reaction.message.channel.delete()
                return
            elif reaction.emoji == reopen:  # the reopen
                await reaction.message.delete()
                return
            elif reaction.emoji == transcript:  # the transcript emoji check
                channel_holder = reaction.message.channel
                if not transcript_rdy:
                    await channel_holder.send(embed=unable_t)
                    await reaction.remove(user)
                    return
                for specific_category in channel_holder.guild.categories:
                    if categoryT == specific_category.name.lower():
                        await reaction.message.channel.edit(category=specific_category,
                                                            name="saved " + channel_holder.name)
                        for member in channel_holder.members:
                            hasRole = False
                            for role in roles:
                                for pRole in member.roles:
                                    if role == pRole:
                                        hasRole = True
                            if not hasRole:
                                await channel_holder.set_permissions(member, read_messages=False, send_messages=False)

                        for role in roles:
                            await channel_holder.set_permissions(role, read_messages=True, send_messages=False)

                        await reaction.remove(user)
                        return

                await channel_holder.send(embed=error_t)

        await reaction.remove(user)

#all the embeds that dont needs changes(like setup and showL) and are used in the code.
global ticket_responder
ticket_responder = discord.Embed(
    description='Fill out your appeal below.\n Staff will be with you shortly.\nTo close This ticket react with 🔒',
    colour=discord.Colour.blue(),
)
ticket_responder2 = discord.Embed(
    description="Please fill out the information below in a message: "
)
ticket_responder2.add_field(name="In Game Name:",
                            value="-",
                           inline=False)
ticket_responder2.add_field(name="\nWhy You Were Banned:",
                            value="-",
                            inline=False)
ticket_responder2.add_field(name="\nWhen Were You Banned:",
                           value="-",
                            inline=False)
ticket_responder2.add_field(name="\nWho Banned You:",
                            value="-",
                            inline=False)
ticket_responder2.add_field(name="\nWhy You Wish To Appeal",
                            value="-",
                            inline=False)
ticket_responder.set_footer(text="Made by Shnap#5581")

global ticket_2step
ticket_2step = discord.Embed(
    description="Are you sure you want to delete the Ban Appeal?\n React ✅ to close it.\n React ⛔ to Open it again.\n React 🔖 to save the ban appeal. "
)


global unable_msg
unable_msg = discord.Embed(
    description="Unable to use the command.\nReason: You dont have an administrator permission"
)

global unable_t
unable_t = discord.Embed(
    description="Unable to save the transcript.\nReason: There is no designated place created for the transcript to be saved"
)

global error_t
error_t = discord.Embed(
    description="Unable to save the transcript.\nReason: The category given doesn't exist anymore/ The name given was typed wrong"
)
client.run("The bot's token")
