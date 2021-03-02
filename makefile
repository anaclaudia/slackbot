decrypt:
	@sops -d -i .env

encrypt:
	@sops -e -i .env
