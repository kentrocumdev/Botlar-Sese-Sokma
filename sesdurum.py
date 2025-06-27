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

def run_client_process(token, channel_id, status_str, activity_type_str, activity_name, stream_url=None):
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
        "competing": discord.ActivityType.competing,
        "streaming": discord.ActivityType.streaming
    }

    status = status_map.get(status_str, discord.Status.online)

    if activity_type_str == "none":
        activity_type = None
        activity_name = None
    else:
        activity_type = activity_map.get(activity_type_str, discord.ActivityType.playing)

    class CustomVoiceClient(discord.Client):
        async def on_ready(self):
            print(f"{self.user} olarak giriş yapıldı.")
            if activity_type and activity_name:
                if activity_type == discord.ActivityType.streaming:
                    await self.change_presence(
                        status=status,
                        activity=discord.Streaming(name=activity_name, url=stream_url or "https://twitch.tv/username")
                    )
                else:
                    await self.change_presence(
                        status=status,
                        activity=discord.Activity(type=activity_type, name=activity_name)
                    )
                print(f"Durum ayarlandı: {status}, {activity_type.name} {activity_name}")
            else:
                await self.change_presence(status=status, activities=[])
                print("Aktivite ayarlanmadı.")

            channel = self.get_channel(int(channel_id))
            if channel and isinstance(channel, discord.VoiceChannel):
                await channel.connect()
                print(f"{self.user} ses kanalına katıldı: {channel.name}")
            else:
                print("Ses kanalı bulunamadı veya yanlış ID.")

        async def start_client(self):
            try:
                await self.start(token)
            except Exception as e:
                print(f"{token[:10]}... hatalı olabilir: {e}")

    client = CustomVoiceClient(intents=intents)
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
        "0": "none",
        "1": "playing",
        "2": "listening",
        "3": "watching",
        "4": "competing",
        "5": "streaming"
    }
    print(Fore.RED + """
🎮 Aktivite Türü:
0 - Aktivite Yok
1 - Playing
2 - Listening
3 - Watching
4 - Competing
5 - Twitch Yayını
""" + Style.RESET_ALL)
    activity_choice = input("Seçim (0-5): ").strip()
    activity_type_str = activity_options.get(activity_choice, "playing")

    activity_name = None
    stream_url = None

    if activity_type_str != "none":
        activity_name = input(Fore.RED + "📝 Aktivite mesajı: " + Style.RESET_ALL)
        if activity_type_str == "streaming":
            stream_url = input(Fore.RED + "📺 Twitch yayın linki: " + Style.RESET_ALL)

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
            args=(token, channel_id, status_str, activity_type_str, activity_name, stream_url)
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
    multiprocessing.set_start_method("spawn")
    main()
