import os
import asyncio
import multiprocessing
import discord
from colorama import init, Fore, Style

init()

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_and_clear():
    input("Devam etmek için Enter'a basın...")
    clear_cmd()

def banner():
    print(Fore.RED + """

            TOOL CODER BY KENTRO

DİKKAT! BU TOOL BOTLARI SES KANALINA SOKAR VE DURUM AYARLAR

""" + Style.RESET_ALL)
    wait_and_clear()

def menu():
    print(Fore.RED + "\nLütfen bir hizmet seçin:")
    print("1. Ses Kanalına Katıl ve Durum/Aktivite Ayarla")
    print("2. Çıkış" + Style.RESET_ALL)

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.presences = True
intents.members = True

class VoiceJoinClient(discord.Client):
    def __init__(self, token, channel_id, status=None, activity_type=None, activity_name=None):
        super().__init__(intents=intents)
        self.token = token
        self.channel_id = int(channel_id)
        self.status = status
        self.activity_type = activity_type
        self.activity_name = activity_name

    async def on_ready(self):
        print(f"{self.user} olarak giriş yapıldı.")

        if self.status and self.activity_type and self.activity_name:
            await self.change_presence(
                status=self.status,
                activity=discord.Activity(type=self.activity_type, name=self.activity_name)
            )
            print(f"Durum ayarlandı: {self.status}, {self.activity_type.name} {self.activity_name}")

        channel = self.get_channel(self.channel_id)
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f"{self.user} ses kanalına katıldı: {channel.name}")
        else:
            print("Ses kanalı bulunamadı veya yanlış ID.")

    async def start_client(self):
        try:
            await self.start(self.token)
        except Exception as e:
            print(f"{self.token[:10]}... hatalı olabilir: {e}")

def run_client_process(token, channel_id, status_str, activity_type_str, activity_name):
    import discord

    status_map = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
        "invisible": discord.Status.invisible
    }
    activity_map = {
        "playing": discord.ActivityType.playing,
        "listening": discord.ActivityType.listening,
        "watching": discord.ActivityType.watching,
        "competing": discord.ActivityType.competing
    }

    status = status_map.get(status_str, discord.Status.online)
    activity_type = activity_map.get(activity_type_str, discord.ActivityType.playing)

    client = VoiceJoinClient(token, channel_id, status, activity_type, activity_name)
    asyncio.run(client.start_client())

async def voice_joiner():
    token_count = int(input(Fore.RED + "Kaç token ile bağlanılsın? " + Style.RESET_ALL))
    channel_id = input(Fore.RED + "Ses Kanalı ID'si: " + Style.RESET_ALL)

    status_options = {
        "1": "online",
        "2": "idle",
        "3": "dnd",
        "4": "invisible"
    }
    print(Fore.RED + """
📶 Durum Seç:
1 - Çevrim İçi
2 - Boşta
3 - Rahatsız Etmeyin
4 - Görünmez
""" + Style.RESET_ALL)
    status_choice = input("Seçim (1-4): ").strip()
    status_str = status_options.get(status_choice, "online")

    activity_options = {
        "1": "playing",
        "2": "listening",
        "3": "watching",
        "4": "competing"
    }
    print(Fore.RED + """
🎮 Aktivite Türü:
1 - Playing
2 - Listening
3 - Watching
4 - Competing
""" + Style.RESET_ALL)
    activity_choice = input("Seçim (1-4): ").strip()
    activity_type_str = activity_options.get(activity_choice, "playing")

    activity_name = input(Fore.RED + "📝 Aktivite mesajı: " + Style.RESET_ALL)

    print(Fore.RED + "\nTokenleri nasıl almak istersin?" + Style.RESET_ALL)
    print("1. token.txt dosyasından al")
    print("2. Elle gir")
    choice = input(Fore.RED + "Seçimin (1/2): " + Style.RESET_ALL).strip()

    tokens = []
    if choice == "1":
        if os.path.exists("token.txt"):
            with open("token.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if len(lines) < token_count:
                print(Fore.RED + f"Yeterli token yok! {len(lines)} token bulundu, {token_count} gerekli." + Style.RESET_ALL)
                wait_and_clear()
                return
            tokens = lines[:token_count]
        else:
            print(Fore.RED + "token.txt dosyası bulunamadı!" + Style.RESET_ALL)
            wait_and_clear()
            return
    elif choice == "2":
        for i in range(token_count):
            token = input(Fore.RED + f"{i+1}. tokeni girin: " + Style.RESET_ALL).strip()
            tokens.append(token)
    else:
        print(Fore.RED + "Geçersiz seçim!" + Style.RESET_ALL)
        wait_and_clear()
        return

    processes = []
    for token in tokens:
        p = multiprocessing.Process(
            target=run_client_process,
            args=(token, channel_id, status_str, activity_type_str, activity_name)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

def main():
    clear_cmd()
    banner()
    while True:
        clear_cmd()
        menu()
        choice = input(Fore.RED + "Seçiminiz: " + Style.RESET_ALL).strip()
        clear_cmd()
        if choice == "1":
            print(Fore.RED + "İşlem başlatılıyor..." + Style.RESET_ALL)
            try:
                asyncio.run(voice_joiner())
            except Exception as e:
                print(Fore.RED + f"Hata oluştu: {e}" + Style.RESET_ALL)
            wait_and_clear()
        elif choice == "2":
            print(Fore.RED + "Çıkış yapılıyor..." + Style.RESET_ALL)
            wait_and_clear()
            break
        else:
            print(Fore.RED + "Geçersiz seçim, tekrar deneyin." + Style.RESET_ALL)
            wait_and_clear()

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Windows uyumluluğu için
    main()
