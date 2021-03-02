decrypt:
	@sops -d -i .env

encrypt:
	@sops -e -i .env

run-ngrok:
	@~/ngrok http 5000

run-flask: decrypt
	python3 bot.py
