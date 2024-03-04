from pyrogram import Client, __version__
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid
from pyrogram.types import ReplyKeyboardMarkup
import os
import sys
from dotenv import load_dotenv
from Lib._TabarnaBase import TabarnaBase

taban = TabarnaBase(
    baslik="Güvenlik Sistemi",
    aciklama="gRobot Başlatıldı..",
    banner="gRobot",
    girinti=3
)

konsol = taban.konsol


def hata(yazi: str) -> None:
    konsol.print(yazi, style="bold red")


def bilgi(yazi: str) -> None:
    konsol.print(yazi, style="blue")


def basarili(yazi: str) -> None:
    konsol.print(yazi, style="bold green", width=70, justify="center")


def onemli(yazi: str) -> None:
    konsol.print(yazi, style="bold cyan")


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    hata("""En az python 3.6 sürümüne sahip olmanız gerekir.
            Birden fazla özellik buna bağlıdır. Bot kapatılıyor.""")
    quit(1)

# Heroku Geçmek için aws
if (taban.bellenim_surumu.split('-')[-1] != 'aws') and (not os.path.exists("ayar.env")):
    hata("\n\tLütfen ayar.env dosyanızı oluşturun..\n")
    quit(1)

load_dotenv("ayar.env")

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
AYAR_KONTROL = os.environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if AYAR_KONTROL:
    hata("\n\tLütfen ayar.env dosyanızı düzenlediğinize emin olun veya\n\tilk hashtag'de belirtilen satırı kaldırın..\n")
    quit(1)

API_ID = str(os.environ.get("API_ID", str))
API_HASH = str(os.environ.get("API_HASH", str))
BOT_TOKEN = str(os.environ.get("BOT_TOKEN", str))
LOG_ID = str(os.environ.get("LOG_ID", str))
SESSION_ADI = str(os.environ.get("SESSION_ADI", str))
GROUP_ID_PDF = int(os.environ.get("GROUP_ID_PDF", int))
GROUP_ID_EPUB = int(os.environ.get("GROUP_ID_EPUB", int))
GROUP_ID_CHAT = int(os.environ.get("GROUP_ID_CHAT", int))



BUTONLAR = {
    "pdf": "📕 Pdf",
    "epub": "📗 Epub",
     "chat": "💬 Sohbet - İstek",

}

DUGMELER = ReplyKeyboardMarkup([
    [
       BUTONLAR["chat"],
    ],
    [
        BUTONLAR["pdf"],
        BUTONLAR["epub"]
    ]
],
    resize_keyboard=True)


try:
    oRobot = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        name=':memory:',
        bot_token=BOT_TOKEN,
        plugins=dict(root="Robot/Eklentiler")
    )
except ValueError:
    hata("\n\tLütfen ayar.env dosyanızı DÜZGÜNCE! oluşturun..\n")
    quit(1)

DESTEK_KOMUT = {}

tum_eklentiler = [
    f"📂 {dosya.replace('.py','')}"
    for dosya in os.listdir("./Robot/Eklentiler/")
    if dosya.endswith(".py") and not dosya.startswith("_")
]


def baslangic() -> None:
    try:
        oRobot.start()
    except ApiIdInvalid:
        hata('\n\tayar.env dosyasındaki API Bilgileri Geçersiz..\n')
        quit(1)
    except AccessTokenInvalid:
        hata('\n\tBot Token Geçersiz..\n')
        quit(1)

    surum = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}"
    konsol.print(
        f"[gold1]@{SESSION_ADI}[/] [yellow]:bird:[/] [bold red]Python: [/][i]{surum}[/]", width=70, justify="center")
    basarili(
        f"{SESSION_ADI} [magenta]v[/] [blue]{__version__}[/] [red]Pyrogram[/] tabanında [magenta]{len(tum_eklentiler)} eklentiyle[/] çalışıyor...\n")

    oRobot.stop()
