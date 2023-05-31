import re, os, time, logging
from pyrogram.errors import FloodWait, RPCError

logging.basicConfig(level=logging.INFO, filename='error.log')
LOG = logging.getLogger("Bot by @YUITOAKASH")
LOG.setLevel(level=logging.INFO)

id_pattern = re.compile(r'^.\d+$')

class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_NAME = os.environ.get("BOT_NAME", "")
    TOKEN_TIMEOUT = int(os.environ.get("TOKEN_TIMEOUT", 600))
    # database config
    DB_NAME = os.environ.get("DB_NAME","pyro-botz")
    DB_URL = os.environ.get("DB_URL","")
    # other configs
    BOT_UPTIME = time.time()
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]
    FORCE_SUB = os.environ.get("FORCE_SUB", "")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", None))
    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    Text = os.environ.get("Text", "")
    Text1 = os.environ.get("Text1", "")
    Text2 = os.environ.get("Text2", "")
    Text3 = os.environ.get("Text3", '''\         / 
 \       /
  \     /
   \   /
    \ /
     X
    / \\
   /   \\
  /     \\
 /       \\
/         \'''
)

    LOGGER = LOG
    shorteners_list = []

    def __init__(self):
        if os.path.exists('shorteners.txt'):
            with open('shorteners.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    temp = line.strip().split()
                    if len(temp) == 2:
                        self.shorteners_list.append({'domain': temp[0], 'api_key': temp[1]})

LOG.info('Config loaded successfully')


class Txt(object):

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""
