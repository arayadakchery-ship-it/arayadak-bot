# arayadak-bot
Telegram Store Bot for Arayadak Auto Parts

## Stack
- Python 3.12
- python-telegram-bot 21.6
- SQLite (arayadak.db)

## Run locally
```bash
pip install -r requirements.txt
python bot.py
```

## Ubuntu VPS Deployment

### 1. Install dependencies
```bash
sudo apt update && sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

### 2. Copy project files
```bash
sudo mkdir -p /opt/arayadak-bot
sudo cp -r . /opt/arayadak-bot/
```

### 3. Configure the systemd service
Edit `arayadak.service` and set your real values:
```
Environment="BOT_TOKEN=YOUR_ACTUAL_TOKEN"
Environment="WHATSAPP=989131634786"
```

Then install and start the service:
```bash
sudo cp arayadak.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable arayadak
sudo systemctl start arayadak
```

### 4. Check status / logs
```bash
sudo systemctl status arayadak
sudo journalctl -u arayadak -f
```

## Environment Variables
| Variable   | Default (config.py)              | Description           |
|------------|----------------------------------|-----------------------|
| BOT_TOKEN  | hardcoded fallback               | Telegram bot token    |
| WHATSAPP   | 989131634786                     | WhatsApp contact      |
| PHONE      | 09131634786                      | Phone contact         |
| ADMIN_ID   | 0                                | Telegram admin user ID|
