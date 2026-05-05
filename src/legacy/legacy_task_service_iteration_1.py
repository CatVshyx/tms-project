import datetime
import json
import os
import smtplib
from enum import Enum
from email.mime.text import MIMEText

TASKS = []
USERS = {}
LOG_FILE = 'log.txt'


class TaskStatus(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2


def process_task(title, user_email, action, priority=None):
    """Process task"""

    if action == 1:
        if title is None or title == '' or len(title) == 0:
            print('error: no title')
            return None

        if len(title) > 100:
            print('error: title too long')
            return None

        if priority is None:
            priority = 3

        task = {
            'id': len(TASKS) + 1,
            'title': title,
            'status': TaskStatus.TODO.value,
            'priority': priority,
            'user': user_email,
            'created': str(datetime.datetime.now())
        }

        TASKS.append(task)

        # logging (fixed resource leak)
        with open(LOG_FILE, 'a') as f:
            f.write(f"{datetime.datetime.now()}: created task {title}\n")

        # email sending
        try:
            msg = MIMEText('New task: ' + title)
            msg['Subject'] = 'Task created'
            msg['From'] = 'noreply@tms.com'
            msg['To'] = user_email

            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()

        except (smtplib.SMTPException, OSError) as e:
            print(f"email error: {e}")

        return task

    elif action == 2:
        for task in TASKS:
            if task['id'] == title:  # тут title фактически id (оставлено как есть на этой итерации)
                task['user'] = user_email
                task['status'] = TaskStatus.IN_PROGRESS.value

                with open(LOG_FILE, 'a') as f:
                    f.write(f"{datetime.datetime.now()}: assigned\n")

                return task

        return None

    elif action == 3:
        for task in TASKS:
            if task['id'] == title:
                if task['status'] != TaskStatus.IN_PROGRESS.value:
                    return False

                task['status'] = TaskStatus.DONE.value

                # placeholder for PDF generation (unchanged)
                # ...

                with open(LOG_FILE, 'a') as f:
                    f.write(f"{datetime.datetime.now()}: completed\n")

                return task

        return None