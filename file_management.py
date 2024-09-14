import os
import shutil

# Função para mover arquivos antigos para a pasta de backup
def move_old_file(download_folder, backup_folder):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Lista os arquivos no diretório de download
    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)

        # Mover o arquivo para o diretório de backup
        if os.path.isfile(file_path):
            shutil.move(file_path, os.path.join(backup_folder, filename))

# Função para listar arquivos em um diretório específico
def list_files(directory):
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return []

# Função para obter o caminho completo de um arquivo
def get_file_path(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        return file_path
    return None
