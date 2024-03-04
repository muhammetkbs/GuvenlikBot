from Robot.Edevat._pyrogram.BUTON_OLUSTURUCU import buton_olustur
from Robot.Edevat.zenginLog import log_yolla
from pyrogram import Client, filters
from pyrogram.types import Message
from Robot import DUGMELER, GROUP_ID_PDF
from datetime import datetime
from datetime import timedelta


@Client.on_message(filters.regex(r'^📕 Pdf$') & filters.private)
async def join_group_buton(client: Client, message: Message):
    # < Başlangıç
    await log_yolla(client, message)

    ilk_mesaj = await message.reply("⌛️ `Pending..`",
                                    quote=True,
                                    disable_web_page_preview=True
                                    )
    # ------------------------------------------------------------- Başlangıç >
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=1)
    davet_linki = await client.create_chat_invite_link(GROUP_ID_PDF, member_limit=1, expire_date=future_time)
    mesaj = f"""Merhaba **{message.from_user.first_name}**,

[Pdf | Güvenlik Bot]({davet_linki.invite_link})

❗️Bu link kısa süre içinde geçersiz olacaktır.
"""

    await ilk_mesaj.delete()

    await message.reply(mesaj, quote=True, reply_markup=DUGMELER)
