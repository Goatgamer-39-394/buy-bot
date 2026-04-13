import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ROLE_ID = 1490306567126515722

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class BuyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.product = None
        self.payment = None

    @discord.ui.select(
        placeholder="Select Product",
        options=[
            discord.SelectOption(label="Minecraft", value="Minecraft", emoji="⛏️"),
            discord.SelectOption(label="Crunchyroll", value="Crunchyroll", emoji="🍥"),
            discord.SelectOption(label="Steam", value="Steam", emoji="🎮"),
        ]
    )
    async def product_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.product = select.values[0]
        await interaction.response.send_message(f"Product: {self.product}", ephemeral=True)

    @discord.ui.select(
        placeholder="Select Payment",
        options=[
            discord.SelectOption(label="Crypto", value="Crypto", emoji="🪙"),
            discord.SelectOption(label="PayPal", value="PayPal", emoji="💰"),
        ]
    )
    async def payment_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.payment = select.values[0]
        await interaction.response.send_message(f"Payment: {self.payment}", ephemeral=True)

    @discord.ui.button(label="Confirm Purchase", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.product or not self.payment:
            return await interaction.response.send_message(
                "Please select product and payment first.",
                ephemeral=True
            )

        await interaction.response.send_message(
            content=(
                f"✅ **ORDER CONFIRMED**\n"
                f"<@&{ROLE_ID}>\n"
                f"Customer: {interaction.user.mention}\n"
                f"Product: {self.product}\n"
                f"Payment: {self.payment}"
            )
        )


@bot.command()
async def buy(ctx):
    embed = discord.Embed(
        title="🛒 Store",
        description="Select product + payment then confirm order",
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=BuyView())


bot.run(TOKEN)