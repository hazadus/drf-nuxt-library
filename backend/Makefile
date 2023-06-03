BACKUP_PATH = /Users/hazadus/webbackup
BACKUP_DATE = $(shell date +%Y_%m_%d_%H-%M)
FULL_PATH = $(BACKUP_PATH)/library-$(BACKUP_DATE)
REMOTE_USER = root
REMOTE_IP = 77.232.139.124
REMOTE_DIR = /root/drf-nuxt-library/

backup:
	rsync -arv --exclude=.venv --exclude=.git --exclude=__pycache__ --exclude=staticfiles $(REMOTE_USER)@$(REMOTE_IP):$(REMOTE_DIR) $(FULL_PATH)
upd:
	docker compose up -d --build
test:
	docker exec library-api coverage run --source='.' -m manage test
	docker exec library-api coverage html
