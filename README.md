# spotify_hotkeys

Atalhos globais (Windows) para controlar **o volume do Spotify** e **navegar entre músicas (próxima/anterior)**, mesmo com **outro aplicativo em foco**.

O projeto combina **Python + Flask + Spotipy (OAuth da Spotify Web API)** com a biblioteca **keyboard** para capturar hotkeys globais e enviar comandos de **volume e playback** para o **dispositivo ativo** via API.

> **Requisitos:** Spotify **Premium**, app criado no **Spotify Developer Dashboard** e Redirect URI configurada como **`http://127.0.0.1:8888/callback`**.

---

## Funcionalidades

* Hotkeys **globais** no Windows (funcionam com qualquer app em foco)
* Controle de **volume absoluto** (0–100%) e **incremental** (±STEP)
* **Próxima música** e **música anterior** via atalhos
* Detecção automática do **dispositivo ativo** (PC preferencial)
* Transferência automática de playback quando necessário
* Autenticação via **OAuth** com cache de token (Spotipy)
* **Logs** no console para debug (volume, device ativo, etc.)

---

## Tecnologias

* Python 3.10+
* Flask
* Spotipy (Spotify Web API)
* keyboard (hotkeys globais no Windows)

---

## Estrutura do projeto

```text
spotify_hotkeys/
├─ .venv/                   # ambiente virtual (não versionar)
├─ src/
│  └─ spotify_hotkeys.py    # Flask + OAuth + hotkeys
├─ requirements.txt
├─ .env                     # (opcional) credenciais locais
├─ .gitignore
└─ README.md
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/spotify_hotkeys.git
cd spotify_hotkeys

# Crie o ambiente virtual (Windows)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt
```

---

## Configuração

### Spotify Developer Dashboard

* Adicione a Redirect URI: **`http://127.0.0.1:8888/callback`**
* Ative o **Development Mode** e adicione seu usuário como *tester*
* Copie o **Client ID** e **Client Secret**

### Variáveis de ambiente (PowerShell)

```powershell
$env:SPOTIPY_CLIENT_ID="SEU_CLIENT_ID"
$env:SPOTIPY_CLIENT_SECRET="SEU_CLIENT_SECRET"
$env:SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
$env:FLASK_SECRET_KEY="uma_chave_segura"
```

---

## Execução

```bash
python .\src\spotify_hotkeys.py
```

* Abra `http://127.0.0.1:8888/` no navegador
* Faça login no Spotify e autorize os escopos solicitados
* Após autenticar, os hotkeys serão ativados automaticamente

---

## Hotkeys disponíveis

### Volume

* `Ctrl + Alt + ↑` → aumentar volume (+5%)
* `Ctrl + Alt + ↓` → diminuir volume (−5%)
* `Ctrl + Alt + 0` → volume 0% (mute)
* `Ctrl + Alt + 9` → volume 100%

### Playback

* `Ctrl + Alt + →` → próxima música
* `Ctrl + Alt + ←` → música anterior

> O valor do passo pode ser alterado na constante:

```python
STEP = 5
```

---

## Funcionamento geral

1. O **Flask** inicia o fluxo de autenticação OAuth do Spotify.
2. Após o login, o token é armazenado em cache local.
3. Uma **thread separada** registra os hotkeys globais.
4. Cada atalho envia comandos de **volume ou navegação de faixa** para a API do Spotify.

---

## Troubleshooting

* **Atalhos não funcionam**

  * Execute o terminal como **Administrador**
  * Confirme que o login OAuth foi concluído

* **Nenhum dispositivo ativo**

  * Abra o Spotify Desktop e inicie uma música

* **Erro de redirect ou client_id**

  * Verifique se a Redirect URI é idêntica à configurada no Dashboard

---

## Segurança

* Nunca versione `.env` ou credenciais
* Em caso de vazamento, gere um novo **Client Secret** no Dashboard

---

## Licença

MIT — veja o arquivo `LICENSE`.
