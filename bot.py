import os
import random
import discord
import feedparser
import json
from datetime import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

# ================= LOAD ENV =================

load_dotenv()

TOKEN = os.getenv("TOKEN")
SERVER_BRAND_NAME = "Arcade NeXus"

if not TOKEN:
    raise RuntimeError("TOKEN not found in environment variables")

# ================= BOT CONFIG =================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= FILE STORAGE =================

BALANCE_FILE = "balances.json"
POSTED_FILE = "posted_links.json"

def load_json(file):
    if not os.path.exists(file):
        return {}

    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

balances = load_json(BALANCE_FILE)
posted_links = load_json(POSTED_FILE)

# ================= NEWS CONFIG =================

NEWS_CHANNEL_ID = 1473057009652858880
CHECK_INTERVAL_MINUTES = 15

RSS_FEEDS = {
    "GameSpot": "https://www.gamespot.com/feeds/news/",
    "IGN": "https://feeds.ign.com/ign/games-all",
    "Steam": "https://store.steampowered.com/feeds/news.xml",
    "PC Gamer": "https://www.pcgamer.com/rss/"

}

IMPORTANT_KEYWORDS = [
    "announced","official","revealed","confirmed",
    "release","launch","update","dlc","expansion"
]

IGNORE_KEYWORDS = [
    "review","preview","guide","walkthrough"
]

def is_important_news(title, summary=""):
    content = (title + summary).lower()

    if any(x in content for x in IGNORE_KEYWORDS):
        return False

    return any(x in content for x in IMPORTANT_KEYWORDS)

# ================= NEWS SYSTEM =================

async def fetch_and_post_news(force=False):

    channel = bot.get_channel(NEWS_CHANNEL_ID)
    if not channel:
        return

    color_map = {
        "GameSpot": 0x9b59b6,
        "IGN": 0x9b59b6,
        "Steam": 0x9b59b6,
        "PC Gamer": 0x9b59b6
    }

    global posted_links

    for source, url in RSS_FEEDS.items():

        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:

            link = entry.get("link")
            title = entry.get("title", "")
            summary_text = entry.get("summary", "")

            if not link or link in posted_links:
                continue

            if not force and not is_important_news(title, summary_text):
                continue

            # HTML CLEANER
            clean_summary = summary_text
            clean_summary = clean_summary.replace("<p>", "")
            clean_summary = clean_summary.replace("</p>", "")
            clean_summary = clean_summary.replace("<br />", "")
            clean_summary = clean_summary[:300]

            embed = discord.Embed(
                title=title,
                url=link,
                description=clean_summary if clean_summary else "Click below to read more.",
                color=color_map.get(source, 0x9b59b6),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Source", value=source, inline=True)
            embed.add_field(
                name="Read full article",
                value=f"[Open article]({link})",
                inline=False
            )

            embed.set_footer(text="Arcade NeXus • Gaming News")

            await channel.send(embed=embed)

            posted_links.append(link)
            save_json(POSTED_FILE, posted_links)

# ================= LOOP =================

@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def news_loop():
    await fetch_and_post_news()

@news_loop.before_loop
async def before_news():
    await bot.wait_until_ready()

# ================= ROAST SYSTEM =================

roast_openers = [  "Bro",
  "My guy",
  "Buddy",
  "Chief",
  "Legend",
  "Big man",
  "G",
  "Champ",
  "Soldier",
  "Boss",
  "High roller",
  "Sweaty grinder",
  "Random from free mode",
  "Diamond Casino regular",
  "Low level tryhard",
  "AFK heist member",
  "Oppressor Mk2 enthusiast",
  "KD warrior",
  "Clip farmer",
  "Casual tourist"]

roast_middles = [
    "took an L so big",
  "just lost so hard",
  "donated so many chips",
  "got cooked so badly",
  "fumbled the bag so hard",
  "threw so violently",
  "missed so spectacularly",
  "crashed and burned so hard",
  "sold the whole lobby so hard",
  "speedran poverty so fast",
  "fed the casino so generously",
  "malfunctioned so badly",
  "desynced from reality so hard",
  "got RNG-slapped so brutally",
  "whiffed so hard even NPCs noticed",
  "played themselves so perfectly",
  "failed so cleanly",
  "tank-ragdolled so aggressively",
  "lag-spiked their own wallet",
  "got drop-kicked by the slot machine"
]

roast_endings = [
     "even Lester is speechless.",
  "Rockstar is clipping this for a comedy trailer.",
  "the Diamond Casino added you to the VIP donor wall.",
  "Maze Bank sent you a thank you card.",
  "NPCs are laughing in free mode.",
  "the slot machine is asking for a restraining order.",
  "Pavel cancelled your heist invites.",
  "even Lamar went quiet for a second.",
  "Los Santos economy stabilized off your losses.",
  "the CCTV footage got marked as training material.",
  "security renamed your table to Charity Corner.",
  "Rockstar used your spin as a before screenshot.",
  "your wallet filed for emergency protection.",
  "the dealer wrote Skill Issue in the report.",
  "your luck got griefed by a level 5 with a pistol.",
  "even an AFK player would have done better.",
  "the casino unlocked a secret achievement called Free Money.",
  "the janitor is sweeping up pieces of your ego.",
  "this loss is now pinned in the staff chat.",
  "the house edge started feeling bad for you."
]

def random_roast():
    return f"{random.choice(roast_openers)} {random.choice(roast_middles)} that {random.choice(roast_endings)}"

# ================= SLOT CONFIG =================

slot_symbols = ["💰","🚗","🔫","💣","💎","🧨"]

win_messages = [
      "**JACKPOT!** 💰 Diamond Casino security is watching YOU.",
  "**BIG WIN!** Lester is shocked you pulled that off.",
  "**LUCK GOD!** RNG bowed down before you.",
  "**PAYDAY!** Cleaner than a silent Diamond Heist.",
  "**TOP TIER!** You robbed the casino without a mask.",
]

slot_win_gifs = [
<<<<<<< HEAD
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnhhZmR0OXpydzRkMndidWZqdXUzdXpkYWsycDVneTY4MGl0Y2FhaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GBtcj090cj3bBSwgJB/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHhiY2pkZjN0ajNla3MzbmM1YzYxNnl4Y3pzZGhnNWVlbmcxdHczMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/sQBkCTTrJRLSE/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm1kbzJtOTg4c3N2d3dwdXN5cnM3dHpmZ3Z3cWt5YW5wamZqaWtxayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jRTD0svQ2M9WD4PNhh/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm1kbzJtOTg4c3N2d3dwdXN5cnM3dHpmZ3Z3cWt5YW5wamZqaWtxayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Y3qaJQjDcbJPyK7kGk/giphy.gif   ",
=======
     "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmZhbDh3d3poMGRkaGl5M2oyNGQxMTY0cHBwYjRsa21jZzQ0dHVvMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Y3qaJQjDcbJPyK7kGk/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmZhbDh3d3poMGRkaGl5M2oyNGQxMTY0cHBwYjRsa21jZzQ0dHVvMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jRTD0svQ2M9WD4PNhh/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWU5cmc0NnY0MWsyMnhrc3dvOGtqZHE1eXF5bGozMGI1OHRzbTNiOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26h0pHNtHKjmDo4WQ/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmdoeXBhdWdycmNycHdqZHFwNGYyaGQ5NGw1NnczbWN3NXRsbTl1OCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PtdOBG0BD9Vvi/giphy.gif",
>>>>>>> f3377d37f5d09b1c2b96a514dc92a9ef96791468
]


slot_lose_gifs = [
<<<<<<< HEAD
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bjJqZmJzeDJjbHk0dmJmbTBkNmM3anRvN2cwcmZ2N3h4Y28waGMyZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/AhmSvx3o3tktpUxd4S/giphy.gif",
  "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjhpZHM3YmEwOHd4cDlpbmZhNDVta2pwemJlZ3BvdXg2NHFkbWlweiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/H7kDjHfuqukEZoWhut/giphy.gif",
  "https://media.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXk1NXZ6MnpuNjE5eXpycHZhaXV0NjRyZjMzZTkwN3pzNTl2N3Q3cCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/In0Lpu4FVivjISX9HT/giphy.gif",
]

shoot_lines = [
     "🚗💥 **{attacker} pulled up on {target} and emptied the whole clip.**",
  "🔫 **{attacker} did a drive-by on {target}. No respawn detected.**",
  "🚘💨 **{attacker} slid through the block and smoked {target}.**",
  "💥 **{attacker} turned {target} into a loading screen.**",
  "🔪 **{attacker} clapped {target} and drove off like nothing happened.**",
  "💀 **{attacker} shot {target} so hard their KD dropped IRL.**",
  "🤣 **{target} got folded like a GTA ragdoll.**",
  "🔫 **{attacker} deleted {target}'s save file.**",
  "☠️ **{target} just became a Wasted screen.**",
  "📉 **{attacker} reduced {target}'s ego by 97%.**"
]

shoot_gifs = [
   "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNnYXd2OWhmMHhnZWZiZXlobG1hcXIyeDZkZzJ3Mno4ODdpMzNqZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l54BsKNdH81mTPgS79/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNnYXd2OWhmMHhnZWZiZXlobG1hcXIyeDZkZzJ3Mno4ODdpMzNqZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/nLjgeYbEdGl2YTYos9/giphy.gif"
]

rankup_gifs = [
    "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
  "https://media.giphy.com/media/xT0GqeSlGSRQutF4Iw/giphy.gif"
]

fbi_gifs = [
     "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDJpcmo5enVvOXAxaWJmNnd1YnN1ODNycWxoemtkbGl1cnJwbDZwbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/80D1Pe1m0jfConCfhn/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dGYzZ3plNGh4aWwyaG1ubG5sZW5lNDI5ZjVscXFwbzBrNmEyYzdyMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26ufnOm2Wtx1eo8O4/giphy.gif"
]

wanted_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanJ0NDhma3VhNndqZmUzMXJwdDhjM2VxbnpraTR3b21iMDFqMmVpaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/oOsIItpM0ofRy4H06m/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanJ0NDhma3VhNndqZmUzMXJwdDhjM2VxbnpraTR3b21iMDFqMmVpaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/oOsIItpM0ofRy4H06m/giphy.gif"
]

mugshot_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHlvOHBpcnJiYmw5anh0b3h6NWJod3V2eTh6eXZkMTgzczBuazlhNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9XjyfcSzWTgMWEscnD/giphy.gif",
  "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHlvOHBpcnJiYmw5anh0b3h6NWJod3V2eTh6eXZkMTgzczBuazlhNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MUwmTGqyX5Q0NPgAgC/giphy.gif"
]

# ================= EVENTS =================
=======
     "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGs4Yml1MTdpdWF5cW1vajV2YzZrOXpwaG1vNGU4YTRqcHB0bTMyeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/H7kDjHfuqukEZoWhut/giphy.gif",
  "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyNHY1cWFqNGpwYXgyN2c2cHZiaXp5cHdzZHFxdjg3OXlyYjduaWowZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yHxZK6nxVIEpSorHFJ/giphy.gif",
  "https://media.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif",
  "https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyeXo0M3luNmh3ZW1neWNzaWhmaXcycTVlNGR4YWdheG5taTN1MnR6ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AhmSvx3o3tktpUxd4S/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa29wd2tkNHlmZDBndXpyaXhlcW1nczU4MGg1cHp2NnFsZWN5NDVlOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/fw8XWwT5YuSJGBwddf/giphy.gif","https://media1.giphy.com/media/v1.Y2lkPTZjMDliOTUyaW9rajg1aGgzdHNjbGx5ZnlrMmM2OHJzdWxjbmt3eWd1eXY1ZW92NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eJ4j2VnYOZU8qJU3Py/giphy.gif", "https://media0.giphy.com/media/v1.Y2lkPTZjMDliOTUyYmE2d2l6YXpxem9hdTV6bWcyNGE4emw3eXlseWUydmd1bmgxY2dxcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5MtOIdkHhxPFu/giphy.gif"]

# ================= READY =================
>>>>>>> f3377d37f5d09b1c2b96a514dc92a9ef96791468

@bot.event
async def on_ready():

    await bot.tree.sync()

    await bot.change_presence(
        activity=discord.Game("NeXus Chaos | /help")
    )

    print(f"✅ Logged in as {bot.user}")

    if not news_loop.is_running():
        news_loop.start()

# ================= NEWS COMMAND =================

@bot.tree.command(name="news", description="Force check gaming news")
async def manual_news(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)

    await fetch_and_post_news(force=True)

    await interaction.followup.send(
        "News check complete.",
        ephemeral=True
    )

# ================= SLOT COMMAND =================

@bot.tree.command(name="slot")
async def slot(interaction: discord.Interaction):

    await interaction.response.defer()

    user_id = str(interaction.user.id)

    if user_id not in balances:
        balances[user_id] = 1000

    if balances[user_id] < 50:
        await interaction.followup.send("💸 You're broke.")
        return

    balances[user_id] -= 50

    e1 = random.choice(slot_symbols)
    e2 = random.choice(slot_symbols)
    e3 = random.choice(slot_symbols)

    is_win = random.random() < (1 / 200)

    if is_win:

        symbol = random.choice(slot_symbols)
        e1 = e2 = e3 = symbol

        balances[user_id] += 1000

        embed = discord.Embed(
            title="🎰 JACKPOT!",
            description=f"```\n| {e1} | {e2} | {e3} |\n```\n{random.choice(win_messages)}",
            color=0x9b59b6
        )

        embed.set_image(url=random.choice(slot_win_gifs))

    else:

        embed = discord.Embed(
            title="💀 LOSS",
            description=f"```\n| {e1} | {e2} | {e3} |\n```\n> {random_roast()}",
            color=0x9b59b6
        )

        embed.set_image(url=random.choice(slot_lose_gifs))

    embed.add_field(name="Balance", value=f"${balances[user_id]}")
    embed.set_footer(text=SERVER_BRAND_NAME)

    save_json(BALANCE_FILE, balances)

    await interaction.followup.send(embed=embed)

# ================= RANK =================

@bot.tree.command(name="rank")
async def rank(interaction: discord.Interaction):

    if not balances:
        await interaction.response.send_message("No players yet.")
        return

    sorted_users = sorted(balances.items(), key=lambda x: x[1], reverse=True)

    leaderboard = ""

    for i, (user_id, money) in enumerate(sorted_users[:10], start=1):
        user = await bot.fetch_user(int(user_id))
        leaderboard += f"**{i}. {user.name}** — ${money}\n"

    embed = discord.Embed(
        title="🏆 Leaderboard",
        description=leaderboard,
        color=0xffcc00
    )

    await interaction.response.send_message(embed=embed)

# ================= RUN =================

bot.run(TOKEN)