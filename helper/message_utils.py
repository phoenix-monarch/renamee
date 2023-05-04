from config import Config

async def sendMessage(message, text, buttons=None):
    try:
        return await message.reply(text=text, quote=True, disable_web_page_preview=True,
                                   disable_notification=True, reply_markup=buttons)
    except FloodWait as f:
        Config.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(message, text, buttons)
    except RPCError as e:
        Config.error(f"{e.NAME}: {e.MESSAGE}")
    except Exception as e:
        Config.error(str(e))
