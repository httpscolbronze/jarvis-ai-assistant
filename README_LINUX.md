# JARVIS on Linux and Hyprland

## System dependencies

On Arch Linux:

```sh
sudo pacman -S --needed python python-pip portaudio qt5-wayland xdg-utils pipewire wireplumber
```

On Debian or Ubuntu:

```sh
sudo apt install python3 python3-venv python3-dev portaudio19-dev libportaudio2 libgl1 libxcb-xinerama0 libxcb-cursor0 xdg-utils
```

Create an environment and install the Python dependencies from the project directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Requirements.txt
```

Copy `.env.example` to `.env` and add your API keys. Start the app with:

```sh
python main.py
```

Speech input uses the default microphone and Google's online speech-recognition service, so it needs microphone access and an internet connection. If PyAudio cannot find an input device, check PipeWire/WirePlumber and the selected default source. Volume controls use `wpctl` when available and fall back to `pactl`. App launching uses installed executable names and `xdg-open` for web links.

If Qt cannot find a Wayland platform plugin, install the Qt 5 Wayland package for your distribution or run through XWayland with `QT_QPA_PLATFORM=xcb`.