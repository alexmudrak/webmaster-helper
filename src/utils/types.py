from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mail.models import MailSettings


@dataclass
class MailMessage:
    mail_settings: "MailSettings"
    mail_box: str
    mail_id: str
    replay_to: str | None
    author_mail: str
    author_name: str
    subject: str
    body: str
    receive_date: datetime
