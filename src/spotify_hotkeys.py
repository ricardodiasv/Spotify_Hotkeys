
# app.py
import os
import time
import threading
import keyboard
from flask import Flask, redirect, session, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI  = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")
SCOPES        = ["user-modify-playback-state", "user-read-playback-state"] 
STEP          = 5  

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "troque_por_uma_chave_segura")

oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=" ".join(SCOPES),
    cache_path=".cache",          
    show_dialog=False
)

sp: spotipy.Spotify | None = None

def ensure_active_device():
    global sp
    state = sp.current_playback()
    if state and state.get("device") and state["device"].get("is_active"):
        return state["device"]
    devices = sp.devices()      

    target = None
    for d in devices.get("devices", []):
        if d.get("type") == "computer":
            target = d; break
    target = target or (devices.get("devices") or [None])[0]
    if target and target.get("id"):
        sp.transfer_playback(target["id"], force_play=False)  
        time.sleep(0.2)
        state = sp.current_playback()
        return state["device"] if state else None
    return None

def set_volume(percent: int):
    dev = ensure_active_device()
    if not dev:
        print("Nenhum dispositivo ativo disponível.")
        return
    percent = max(0, min(100, percent))
    sp.volume(percent) 
    print(f"🔊 Volume Spotify: {percent}% (device: {dev.get('name')})")

def bump_volume(delta: int):
    state = sp.current_playback()
    current = 50
    if state and state.get("device"):
        current = state["device"].get("volume_percent", 50)
    set_volume(current + delta)

def register_hotkeys():
    while not sp:
        time.sleep(0.1)

    keyboard.add_hotkey("ctrl+alt+up",   lambda: bump_volume(+STEP))
    keyboard.add_hotkey("ctrl+alt+down", lambda: bump_volume(-STEP))
    keyboard.add_hotkey("ctrl+alt+0",    lambda: set_volume(0))
    keyboard.add_hotkey("ctrl+alt+9",    lambda: set_volume(100))

    print("Hotkeys ativos: Ctrl+Alt+↑/↓/0/9. Pressione ESC no console para encerrar.")
    keyboard.wait("esc")

@app.route("/")
def index():
    token_info = oauth.get_cached_token()
    if token_info:
        global sp
        sp = spotipy.Spotify(auth=token_info["access_token"])
        return "Autenticado. Utilize os atalhos."

    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Falha no login.", 400
    token_info = oauth.get_access_token(code, as_dict=True)
    if not token_info or "access_token" not in token_info:
        return "Não foi possível obter token.", 400

    global sp
    sp = spotipy.Spotify(auth=token_info["access_token"])
    session["spotify_auth"] = True
    return redirect("/")

if __name__ == "__main__":
    t = threading.Thread(target=register_hotkeys, daemon=True)
    t.start()
    app.run(host="127.0.0.1", port=8888, debug=False)
