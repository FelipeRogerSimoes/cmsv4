import os

class Config:
    BASE_DIR = '/home/cmsssv3/cmsv4'

    # Diretórios para downloads e backups
    DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads/current')
    BACKUP_FOLDER = os.path.join(BASE_DIR, 'downloads/backup')

    # Diretórios de log
    LOG_FOLDER = os.path.join(BASE_DIR, 'logs/current')  # Pasta onde os logs diários serão salvos
    OLD_LOG_FOLDER = os.path.join(BASE_DIR, 'logs/old')  # Pasta onde os logs antigos serão movidos

    # Caminho do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}"

    # Configurações de e-mail
    EMAIL = "informativo@acelera360.app"
    PASSWORD = "Fukumatemple2443-"
    IMAP_SERVER = "smtp0001.neo.space"

    # Outras configurações
    SQLALCHEMY_TRACK_MODIFICATIONS = False
