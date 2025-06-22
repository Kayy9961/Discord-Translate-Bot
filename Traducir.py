import discord
from discord import app_commands
from googletrans import Translator
import datetime

DISCORD_TOKEN = 'EL TOKEN DE TU BOT DE DISCORD'

LANGUAGES = {
    "🇺🇸 English": "en",
    "🇪🇸 Spanish": "es",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇮🇹 Italian": "it",
    "🇵🇹 Portuguese": "pt",
    "🇯🇵 Japanese": "ja",
    "🇰🇷 Korean": "ko",
    "🇨🇳 Chinese": "zh-CN",
    "🇮🇳 Hindi": "hi",
    "🇷🇺 Russian": "ru",
    "🇸🇦 Arabic": "ar"
}

LANG_FLAGS = {v: k.split()[0] for k, v in LANGUAGES.items()}
LANG_LABELS = {v: k.split()[1] for k, v in LANGUAGES.items()}

translator = Translator()

class TranslateBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Bot is online as {self.user}")

bot = TranslateBot()

@bot.tree.command(name="translate", description="Translate a message into another language.")
@app_commands.describe(
    text="Text to translate",
    language="Target language (choose from list)"
)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def translate(inter: discord.Interaction, text: str, language: str):
    await inter.response.defer(thinking=True)

    try:
        result = translator.translate(text, dest=language)
        detected_lang = result.src
        translated_text = result.text
        flag_src = LANG_FLAGS.get(detected_lang, "🌐")
        flag_tgt = LANG_FLAGS.get(language, "🌐")
        name_src = LANG_LABELS.get(detected_lang, detected_lang.upper())
        name_tgt = LANG_LABELS.get(language, language.upper())

        embed = discord.Embed(
            title=f"{flag_src} {name_src} ➡️ {name_tgt} {flag_tgt}",
            description=(
                f"📝 **Original:** {text}\n"
                f"📤 **Translation:** {translated_text}"
            ),
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Translated on {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        await inter.followup.send(embed=embed)

    except Exception as e:
        await inter.followup.send(f"❌ Translation failed: {e}", ephemeral=True)

@translate.autocomplete("language")
async def autocomplete_langs(inter: discord.Interaction, current: str):
    matches = []
    for name, code in LANGUAGES.items():
        if current.lower() in name.lower() or current.lower() in code.lower():
            matches.append(app_commands.Choice(name=name, value=code))
    return matches[:25]

bot.run(DISCORD_TOKEN)
