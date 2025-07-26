#!/usr/bin/python3
import os
import time
import json
import requests
from requests.exceptions import RequestException
from rich.console import Console
from rich.panel import Panel
from rich import print as printf

COOKIES, SUKSES, GAGAL, XRP = {"KEY": None}, [], [], {"KEY": "0.000000"}

def BANNER():
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(Panel(r"""[bold red]●[bold yellow] ●[bold green] ●[/]
[bold red]    ______                      __                 
   / ____/___ ___  __________  / /____  ____ ______
  / /_  / __ `/ / / / ___/ _ \/ __/ _ \/ __ `/ ___/
 / __/ / /_/ / /_/ / /__/  __/ /_/  __/ /_/ / /    
[bold white]/_/    \__,_/\__,_/\___/\___/\__/\___/\__,_/_/     
        [bold white on red]Free XRP Tokens - Coded by Rozhak""", style="bold bright_black", width=56))

class CLAIM:
    def EXECUTION(self):
        with requests.Session() as r:
            r.headers.update({
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://faucetearner.org/dashboard.php',
                'Host': 'faucetearner.org',
            })
            try:
                r.get('https://faucetearner.org/faucet.php', cookies={'Cookie': COOKIES['KEY']})
                response2 = r.post('https://faucetearner.org/api.php?act=faucet', data={}, cookies={'Cookie': COOKIES['KEY']})
            except Exception as e:
                printf(f"[bold red]Request error: {e}")
                return

            txt = response2.text.lower()
            if 'congratulations' in txt:
                try:
                    earned = response2.text.split(' XRP')[0].split('0.')[1]
                except Exception:
                    earned = "000000"
                XRP["KEY"] = f"0.{earned}"
                printf(Panel(f"[italic green]Received {XRP['KEY']} XRP!", title="[bold bright_black]>>> Sukses <<<", style="bold bright_black", width=56))
                SUKSES.append(response2.text)
            elif 'already claimed' in txt:
                printf(Panel("[bold yellow]You already claimed! Waiting...", title="[bold bright_black]>>> Info <<<", style="bold bright_black", width=56))
                GAGAL.append(response2.text)
            else:
                printf(Panel(response2.text, title="[bold bright_black]>>> Gagal <<<", style="bold bright_black", width=56))

    def CHECK_LOGIN(self):
        BANNER()
        cookie = os.environ.get("FAUCET_COOKIE")
        if cookie:
            COOKIES["KEY"] = cookie
        else:
            printf(Panel("[bold red]Environment variable FAUCET_COOKIE belum diatur!", style="bold bright_black", width=56))
            exit(1)

    def XRP(self):
        self.CHECK_LOGIN()
        printf("[bold bright_black]Menjalankan farming 24 jam...\n")
        while True:
            try:
                self.EXECUTION()
                time.sleep(65)
            except RequestException:
                printf("[bold red]Connection error. Retry in 10 detik...", end='\r')
                time.sleep(10)
            except KeyboardInterrupt:
                printf("\n[bold red]Stopped by user.")
                break

if __name__ == "__main__":
    CLAIM().XRP()
