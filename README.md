# 🎧 spotify_hotkeys

Atalhos globais (Windows) para controlar **o volume do Spotify** e comandos básicos de player, mesmo com **outro aplicativo em foco**.

Combina **Python + Flask + Spotipy (OAuth da Spotify Web API)** com a biblioteca **keyboard** para capturar hotkeys no sistema e enviar comandos de volume/playback para o **dispositivo ativo** via API.

> **Requisitos:** Spotify **Premium**, app no **Spotify Developer Dashboard** e Redirect URI configurada como **`http://127.0.0.1:8888/callback`**.

---

## ✨ Funcionalidades

- Hotkeys **globais** no Windows (não dependem da janela ativa)
- Ajuste de **volume absoluto** (0–100%) e **incremental** (±STEP)
- (Opcional) **Play/Pause**, **Próxima**/**Anterior**
- Detecta e, se necessário, **transfere** o playback para o **computador**
- Fluxo de **OAuth** com cache e **refresh automático** de token (Spotipy)
- **Logs** no console para diagnóstico (device ativo, volume atual, etc.)

---

## 🧱 Tecnologias

- Python 3.10+
- Flask
- Spotipy (Spotify Web API)
- keyboard (hook global de teclado)

---

## 🗂️ Estrutura

```text
spotify_hotkeys/
├─ .venv/                   # ambiente virtual (não versionar)
├─ src/
│  └─ spotify_hotkeys.py    # app Flask + hotkeys globais
├─ requirements.txt
├─ .env                     # (opcional) credenciais e chaves locais
├─ .gitignore               # inclui: .venv/, .env
└─ README.md
```

---

## 🚀 Instalação

```bash
# 1) Clone o repositório
git clone https://github.com/seu-usuario/spotify_hotkeys.git
cd spotify_hotkeys

# 2) Crie e ative o ambiente virtual (Windows — PowerShell)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Instale as dependências
pip install -r requirements.txt
# ou
pip install flask spotipy keyboard python-dotenv
```

> **Dica:** mantenha as dependências em `requirements.txt` e **não** versione `.venv/`.

---

## 🔐 Configuração

### 1) Spotify Developer Dashboard
- **Redirect URIs**: adicione **exatamente** `http://127.0.0.1:8888/callback` (loopback IP literal). 
- **Development mode**: adicione seu usuário como **tester**.
- Copie **Client ID** e **Client Secret**.

### 2) Variáveis de ambiente (Windows — PowerShell)

```powershell
$env:SPOTIPY_CLIENT_ID     = "SEU_CLIENT_ID"
$env:SPOTIPY_CLIENT_SECRET = "SEU_CLIENT_SECRET"
$env:SPOTIPY_REDIRECT_URI  = "http://127.0.0.1:8888/callback"
$env:FLASK_SECRET_KEY      = "uma_chave_segura_qualquer"
```

> Alternativa: arquivo `.env` na raiz:
```env
SPOTIPY_CLIENT_ID=SEU_CLIENT_ID
SPOTIPY_CLIENT_SECRET=SEU_CLIENT_SECRET
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
FLASK_SECRET_KEY=minha_chave_segura
```

---

## ▶️ Execução

```bash
# com o venv ativo
python .\src\spotify_hotkeys.py
```

- Acesse `http://127.0.0.1:8888/` e conclua o **login** na sua conta Spotify.
- Autorize os **escopos**: `user-modify-playback-state` e `user-read-playback-state`.
- Ao voltar para `/`, o console exibirá:
  ```
  ✅ Hotkeys ativos: Ctrl+Alt+↑/↓/0/9...
  ```

---

## 🎹 Hotkeys padrão

- `Ctrl + Alt + ↑` → **+5%** volume
- `Ctrl + Alt + ↓` → **−5%** volume
- `Ctrl + Alt + 0` → **0%** (mute)
- `Ctrl + Alt + 9` → **100%**
- *(opcional)* `Ctrl + Alt + Espaço` → **Play/Pause**

> Ajuste o passo em `STEP = 5` ou adicione mapeamentos finos:
```python
keyboard.add_hotkey("ctrl+alt+shift+up",   lambda: bump_volume(+1))
keyboard.add_hotkey("ctrl+alt+shift+down", lambda: bump_volume(-1))
```

---

## 🧭 Como funciona

1. **Flask** inicia o fluxo de **OAuth** e obtém o **access token** da sua conta.
2. Um **thread** separado registra **hotkeys globais** via `keyboard`.
3. Cada hotkey:
   - **lê** o device ativo (ou **transfere** para o PC),
   - **ajusta** o volume pelo endpoint `PUT /v1/me/player/volume` (0–100%),
   - imprime **logs** no console.

---

## 🩺 Troubleshooting

- **Hotkeys não disparam**
  - Conclua o **login** abrindo `http://127.0.0.1:8888/`.
  - Rode o PowerShell como **Administrador**.
  - Troque as combinações por teclas menos concorridas (ex.: `ctrl+shift+alt+page up/down`).

- **"Nenhum dispositivo ativo disponível"**
  - Abra o **Spotify desktop** e **comece a tocar** algo.
  - A transferência de playback para o PC é automática, mas iniciar a reprodução ajuda.

- **Erros de OAuth (No client_id / Invalid redirect)**
  - Confira se as variáveis `SPOTIPY_CLIENT_ID/SECRET/REDIRECT_URI` estão definidas **no mesmo terminal**.
  - Verifique se a Redirect URI **cadastrada** no Dashboard é **idêntica** ao valor usado no código (host, porta, caminho).

---

## 🛡️ Segurança

- **Não** comite `CLIENT_SECRET` nem `.env`.
- Se o secret vazar, use **Rotate client secret** no Dashboard e atualize as variáveis.

---

## 🛣️ Roadmap

- [ ] Hotkeys configuráveis via `config.json`
- [ ] Integração com teclas multimídia
- [ ] UI web simples para controles
- [ ] Build com `pyinstaller` (executável)

---

## 🤝 Contribuição

PRs são bem-vindos. Abra issues com detalhes do ambiente, passos para reproduzir e logs do console.

---

## 📄 Licença

MIT — veja `LICENSE`.
