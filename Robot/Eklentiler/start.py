from Robot.Edevat._pyrogram.BUTON_OLUSTURUCU import buton_olustur
from Robot.Edevat.zenginLog import log_yolla
from pyrogram import Client, filters
from pyrogram.types import Message
from Robot import DUGMELER


@Client.on_message(filters.command(['start'], ['!', '.', '/']) & filters.private)
async def start_buton(client: Client, message: Message):
    # < Başlangıç
    await log_yolla(client, message)

    ilk_mesaj = await message.reply("⌛️ `Pending..`",
                                    quote=True,
                                    disable_web_page_preview=True
                                    )
   
    # ------------------------------------------------------------- Başlangıç >
    mesaj = f"""Merhaba **{message.from_user.first_name}**, ----------- Hoşgeldin!

**[Güvenlik Bot](Kanal linki)**'nin bir üyesi olarak, buradan tüm kanallarımıza güvenle erişebilirsin.

Butonlara basarak, kanallarımızın davet linklerine ulaşabilirsin.

"""

    await ilk_mesaj.delete()

    await message.reply(mesaj, quote=True, reply_markup=DUGMELER)
