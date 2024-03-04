from pyfiglet import Figlet
import os
import sys
import platform
import requests
import datetime
import pytz
from rich.console import Console
from notifypy import Notify
from pathlib import Path
from shutil import copyfileobj
from requests.exceptions import ConnectionError


class TabarnaBase():
    def __repr__(self) -> str:
        return f"{__class__.__name__} Sınıfı -- Tabarna CLI projeleri için kodlanmıştır."

    konsol: Console = Console(log_path=False, highlight=False)

    try:
        kullanici_adi = os.getlogin()
    except OSError:
        import pwd
        kullanici_adi = pwd.getpwuid(os.geteuid())[0]

    bilgisayar_adi = platform.node()
    oturum = kullanici_adi + "@" + bilgisayar_adi

    isletim_sistemi = platform.system()
    bellenim_surumu = platform.release()
    cihaz = isletim_sistemi + " | " + bellenim_surumu

    tarih = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y")
    saat = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%H:%M")
    zaman = tarih + " | " + saat

    try:
        global_ip = requests.get('http://ip-api.com/json').json()['query']
    except ConnectionError:
        global_ip = requests.get('https://api.ipify.org').text
    except Exception as hata:
        global_ip = type(hata).__name__

    ust_bilgi = f"[bright_red]{cihaz}[/]\n"
    ust_bilgi += f"[chartreuse1]{zaman}[/]\n\n"

    ust_bilgi += f"[turquoise2]{oturum}[/]\n"
    ust_bilgi += f"[yellow2]{global_ip}[/]\n"

    def __init__(self, baslik: str, aciklama: str, banner: str, genislik: int = 70, girinti: int = 0, stil: str = "stop", bildirim: bool = False) -> None:
        "Varsayılan Olarak; konsolu temizler, logoyu ve üst bilgiyi yazdırır.."

        self.genislik = genislik
        self.pencere_basligi = baslik
        self.bildirim_metni = aciklama
        self.logo = Figlet(font=stil).renderText(f"{' ' * girinti}{banner}")

        self.temizle

        if bildirim:
            self.bildirim()

        self.konsol.print(self.logo,      width=genislik, style="pale_green1")
        self.konsol.print(self.ust_bilgi, width=genislik, justify="center")

    def logo_yazdir(self, renk: str = "turquoise2") -> None:
        "Konsolu Temizler ve İstenilen Renkte Logoyu Yazdırır.."

        self.temizle
        self.konsol.print(self.logo, width=self.genislik, style=renk)

    def bilgi_yazdir(self):
        "Üst Bilgiyi Yazdırır.."

        self.konsol.print(
            self.ust_bilgi, width=self.genislik, justify="center")

    def log_salla(self, sol: str, orta: str, sag: str) -> None:
        "Sol orta ve sağ şeklinde ekranda hizalanmış tek satır log verir.."

        sol = f"{sol[:13]}[bright_blue]~[/]" if len(sol) > 14 else sol
        orta = f"{orta[:19]}[bright_blue]~[/]" if len(orta) > 20 else orta
        sag = f"{sag[:14]}[bright_blue]~[/]" if len(sag) > 15 else sag
        bicimlendir = '[bold red]{:14}[/] [green]||[/] [yellow]{:20}[/] {:>2}[green]||[/] [magenta]{:^16}[/]'.format(
            sol, orta, "", sag)
        self.konsol.log(bicimlendir)

    def hata_salla(self, hata: Exception) -> None:
        "Yakalanan Exception'ı ekranda gösterir.."

        bicimlendir = f'\t  [bold yellow2]{type(hata).__name__}[/] [bold magenta]||[/] [bold grey74]{hata}[/]'

        self.konsol.print(f"{bicimlendir}",
                          width=self.genislik, justify="center")

    @property
    def temizle(self) -> None:
        if self.isletim_sistemi == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @property
    def win_baslik(self) -> None:
        if self.isletim_sistemi == "Windows":
            try:
                import ctypes
            except ModuleNotFoundError:
                os.system('pip install ctypes')
                self.temizle
                import ctypes

            ctypes.windll.kernel32.SetConsoleTitleW(f"{self.pencere_basligi}")

    def bildirim(self, baslik=None, icerik=None, gorsel=None) -> None:
        if platform.machine() == "aarch64" or self.kullanici_adi == "gitpod" or self.bellenim_surumu.split('-')[-1] == 'aws':
            return

        dizin = os.getcwd()
        konum = dizin.split(
            "\\") if self.isletim_sistemi == "Windows" else dizin.split("/")
        dosya_adi = f"~/../{konum[-2]}/{konum[-1]}/{sys.argv[0]}"

        ayrac = "/" if self.isletim_sistemi != "Windows" else "\\"

        kutuphane_dizin = Path(__file__).parent.resolve()

        _bildirim = Notify()
        _bildirim._notification_audio = f"{kutuphane_dizin}{ayrac}bildirim.wav"
        _bildirim._notification_application_name = dosya_adi

        if gorsel:
            if not gorsel.startswith("http"):
                _bildirim._notification_icon = f"{dizin}{ayrac}{gorsel}"
            else:
                foto_istek = requests.get(gorsel, stream=True)
                foto_istek.raw.decode_content = True
                with open(f"{kutuphane_dizin}{ayrac}gorsel.png", "wb") as dosya:
                    copyfileobj(foto_istek.raw, dosya)
                _bildirim._notification_icon = f"{kutuphane_dizin}{ayrac}gorsel.png"

        _bildirim.title = baslik or self.pencere_basligi
        _bildirim.message = icerik or self.bildirim_metni
        _bildirim.send(block=False)
