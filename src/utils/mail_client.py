import email
import imaplib
import re
import smtplib
from datetime import datetime
from email.header import decode_header
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dateutil import parser

from api.project.models import Project
from mail.models import Mail, MailSettings
from utils.logger_handler import get_logger
from utils.types import MailMessage

logger = get_logger(__name__)


class MailClient:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        imap_ssl: bool,
        imap_server: str,
        imap_port: int,
        imap_username: str,
        imap_password: str,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.imap_ssl = imap_ssl
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.imap_username = imap_username
        self.imap_password = imap_password

    def _create_email_message(
        self,
        subject: str,
        to_email: str,
        body: str,
        reply_mail: Mail | None = None,
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.smtp_username
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        if reply_mail:
            msg["In-Reply-To"] = reply_mail.mail_id.replace("<", "").replace(
                ">", ""
            )
        return msg

    def _send_email_message(self, msg: MIMEMultipart) -> None:
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.smtp_username, msg["To"], msg.as_string())
            server.quit()
            logger.info(f"Email sent successfully - {self.smtp_username}")
        except Exception as e:
            logger.error(f"Email send failed: {str(e)} - {self.smtp_username}")

    def _date_to_mail_str(self, date: datetime) -> str:
        since_date = date.strftime("%d-%b-%Y")
        return f"SINCE {since_date}"

    def _date_handler(self, date_header: str | None) -> datetime:
        date_obj = datetime.now()

        if date_header:
            date_bytes, encoding = decode_header(date_header)[0]
            if encoding:
                date_str = date_bytes.decode(encoding)
            else:
                date_str = date_bytes

            date_pattern = re.compile(r"(.+?) \((.*?)\)")
            match = date_pattern.match(date_str)

            if match:
                date_bytes, _ = match.groups()

            date_bytes = date_bytes.replace("UT", "").strip()

            try:
                date_obj = parser.parse(date_bytes)
            except ValueError:
                raise ValueError(f"Unable to parse date: {date_str}")
        return date_obj

    def _decode_header(self, element: str) -> str:
        decoded_name, encoding = decode_header(element)[0]
        if encoding is not None:
            decoded_name = decoded_name.decode(encoding)
        return decoded_name

    def _from_handler(self, from_header: str) -> tuple[str, str]:
        decoded_name = self._decode_header(from_header)
        email_pattern = re.compile(r"<([^>]+)>")
        match = email_pattern.search(from_header)

        if match:
            from_email = match.group(1)
        else:
            from_email = from_header

        from_name = decoded_name.split(" <")[0].replace('"', "")
        return (from_name, from_email)

    def _body_handler(self, email_msg: Message) -> str:
        body = ""
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = email_msg.get_payload(decode=True).decode()
        return body

    def _parse_email_message(
        self, mail_settings: MailSettings, mail_box: str, email_data: bytes
    ) -> MailMessage:
        email_msg = email.message_from_bytes(email_data)
        subject = self._decode_header(email_msg["subject"])
        from_author, from_email = self._from_handler(email_msg["from"])
        date = self._date_handler(email_msg.get("date"))
        body = self._body_handler(email_msg)
        mail_id = email_msg.get("Message-Id", "")
        replay_to = email_msg.get("In-Reply-To")

        return MailMessage(
            mail_settings=mail_settings,
            mail_box=mail_box,
            mail_id=mail_id,
            replay_to=replay_to,
            author_mail=from_email,
            author_name=from_author,
            subject=subject,
            body=body,
            receive_date=date,
        )

    def _connect_to_mail_server(self) -> imaplib.IMAP4_SSL | imaplib.IMAP4:
        mail: imaplib.IMAP4_SSL | imaplib.IMAP4

        if self.imap_ssl:
            mail = imaplib.IMAP4_SSL(host=self.imap_server)
        else:
            mail = imaplib.IMAP4(host=self.imap_server, port=self.imap_port)

        mail.login(self.imap_username, self.imap_password)
        return mail

    def _get_email_ids(
        self,
        mail: imaplib.IMAP4_SSL | imaplib.IMAP4,
        mail_box: str,
        start_date: datetime | None,
    ) -> list[str]:
        status, _ = mail.select(mail_box)
        find_date = "ALL"
        if start_date:
            find_date = self._date_to_mail_str(start_date)

        status, email_ids = mail.search(None, find_date)
        if not status == "OK":
            raise NotImplementedError("Need to handle search mails error")
        return email_ids[0].split()

    def _fetch_email(
        self, mail: imaplib.IMAP4_SSL | imaplib.IMAP4, email_id: str
    ) -> bytes | None:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if not status == "OK":
            raise NotImplementedError("Need to handle fetch mail error")
        if msg_data and isinstance(msg_data, list):
            if (
                msg_data[0]
                and isinstance(msg_data[0], tuple)
                and len(msg_data[0]) > 1
                and isinstance(msg_data[0][1], bytes)
            ):
                return msg_data[0][1]
        return None

    def get_emails(
        self,
        username: str,
        settings: MailSettings,
        start_date: datetime | None = None,
    ) -> list[MailMessage]:
        results: list[MailMessage] = []
        mail: imaplib.IMAP4_SSL | imaplib.IMAP4 = (
            self._connect_to_mail_server()
        )

        try:
            mail_boxes = (
                settings.mail_folders.split(",")
                if settings.mail_folders
                else ["inbox"]
            )

            for mail_box in mail_boxes:
                mail_box = mail_box.strip()
                email_ids = self._get_email_ids(mail, mail_box, start_date)

                for email_id in email_ids:
                    email_data = self._fetch_email(mail, email_id)
                    if email_data:
                        mail_message = self._parse_email_message(
                            settings, mail_box, email_data
                        )
                        Mail.objects.create_message(mail_message)

                        results.append(mail_message)

            mail.logout()
        except Exception as e:
            logger.error(f"Email retrieval failed: {str(e)}")
        return results

    def send_email(
        self,
        subject: str,
        to_email: str,
        body: str,
        mail_settings: MailSettings,
        project: Project,
        reply_mail: Mail | None = None,
    ) -> None:
        date = datetime.now()
        msg = self._create_email_message(subject, to_email, body, reply_mail)
        self._send_email_message(msg)

        mail_message = MailMessage(
            mail_settings=mail_settings,
            mail_box="Sent",
            mail_id=date.isoformat(),
            replay_to=to_email,
            author_mail=str(mail_settings.smtp_username),
            author_name=str(project.name),
            subject=subject,
            body=body,
            receive_date=date,
        )
        Mail.objects.create_message(mail_message)
