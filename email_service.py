import imaplib
import email
from email.header import decode_header
import os
import schedule
import time
from file_management import move_old_file
from config import Config


# Função para processar anexos de e-mails com assunto "teste de integracao"
def process_email_attachments():
    try:
        # Conectar ao servidor IMAP
        mail = imaplib.IMAP4_SSL(Config.IMAP_SERVER)
        mail.login(Config.EMAIL, Config.PASSWORD)

        # Selecionar a caixa de entrada
        mail.select("inbox")

        # Procurar e-mails não lidos
        status, messages = mail.search(None, 'UNSEEN')

        # Processar cada e-mail não lido
        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]

                    # Decodificar o assunto, se necessário
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    # Verificar se o assunto é "teste de integracao"
                    if subject.lower() == "teste de integracao":
                        print(f"E-mail com assunto '{subject}' encontrado.")

                        # Processar os anexos
                        for part in msg.walk():
                            if part.get_content_maintype() == "multipart":
                                continue
                            if part.get("Content-Disposition") is None:
                                continue

                            filename = part.get_filename()

                            # Verificar se o arquivo anexado é "R007.xlsx"
                            if filename and filename == "R007.xlsx":
                                filepath = os.path.join(Config.DOWNLOAD_FOLDER, filename)

                                # Mover arquivo anterior para o backup
                                move_old_file(Config.DOWNLOAD_FOLDER, Config.BACKUP_FOLDER)

                                # Salvar o novo arquivo "R007.xlsx"
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))

                                print(f"Anexo '{filename}' salvo com sucesso em {Config.DOWNLOAD_FOLDER}.")

        mail.logout()

    except Exception as e:
        print(f"Erro ao processar e-mails: {str(e)}")


# Função para verificar e-mails com faturas (assunto "nova fatura") e salvar "invoice.pdf"
def check_invoices_email():
    try:
        # Conectar ao servidor IMAP
        mail = imaplib.IMAP4_SSL(Config.IMAP_SERVER)
        mail.login(Config.EMAIL, Config.PASSWORD)

        # Selecionar a caixa de entrada
        mail.select("inbox")

        # Procurar e-mails não lidos
        status, messages = mail.search(None, 'UNSEEN')

        # Processar cada e-mail não lido
        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]

                    # Decodificar o assunto, se necessário
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    # Verificar se o assunto é "nova fatura"
                    if subject.lower() == "nova fatura":
                        print(f"E-mail com assunto '{subject}' encontrado.")

                        # Processar os anexos
                        for part in msg.walk():
                            if part.get_content_maintype() == "multipart":
                                continue
                            if part.get("Content-Disposition") is None:
                                continue

                            filename = part.get_filename()

                            # Verificar se o arquivo anexado é "invoice.pdf"
                            if filename and filename == "invoice.pdf":
                                filepath = os.path.join(Config.DOWNLOAD_FOLDER, filename)

                                # Mover arquivo anterior para o backup
                                move_old_file(Config.DOWNLOAD_FOLDER, Config.BACKUP_FOLDER)

                                # Salvar o novo arquivo "invoice.pdf"
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))

                                print(f"Anexo '{filename}' salvo com sucesso em {Config.DOWNLOAD_FOLDER}.")

        mail.logout()

    except Exception as e:
        print(f"Erro ao processar e-mails de faturas: {str(e)}")


# Função para agendar e rodar os serviços de e-mails
def schedule_email_services():
    # Alterar o intervalo de processamento para 1 minuto para facilitar o teste
    schedule.every(1).minutes.do(process_email_attachments)  # A cada 1 minuto

    # Se você quiser testar as faturas também, pode manter ou alterar o intervalo aqui:
    schedule.every(1).minutes.do(check_invoices_email)  # A cada 1 minuto para testar

    # Loop para rodar as tarefas agendadas
    while True:
        schedule.run_pending()
        time.sleep(1)
