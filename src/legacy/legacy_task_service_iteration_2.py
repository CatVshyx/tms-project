import datetime
import smtplib
from enum import Enum
from email.mime.text import MIMEText


LOG_FILE = 'log.txt'


class TaskStatus(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2


class TaskRepository:
    def __init__(self):
        self._tasks = []
        self._users = {}

    def add_task(self, task: dict):
        self._tasks.append(task)

    def get_by_id(self, task_id: int):
        for task in self._tasks:
            if task['id'] == task_id:
                return task
        return None

    def next_id(self):
        return len(self._tasks) + 1


# ----------- helpers -----------

def _validate_title(title: str):
    if title is None or title == '' or len(title) == 0:
        raise ValueError('no title')

    if len(title) > 100:
        raise ValueError('title too long')


def _log_action(message: str):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.datetime.now()}: {message}\n")


def _send_email(user_email: str, title: str):
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


# ----------- use cases -----------

def create_task(repo: TaskRepository, title: str, user_email: str, priority=None):
    _validate_title(title)

    if priority is None:
        priority = 3

    task = {
        'id': repo.next_id(),
        'title': title,
        'status': TaskStatus.TODO.value,
        'priority': priority,
        'user': user_email,
        'created': str(datetime.datetime.now())
    }

    repo.add_task(task)

    _log_action(f"created task {title}")
    _send_email(user_email, title)

    return task


def assign_task(repo: TaskRepository, task_id: int, user_email: str):
    task = repo.get_by_id(task_id)
    if not task:
        return None

    task['user'] = user_email
    task['status'] = TaskStatus.IN_PROGRESS.value

    _log_action("assigned")

    return task


def complete_task(repo: TaskRepository, task_id: int):
    task = repo.get_by_id(task_id)
    if not task:
        return None

    if task['status'] != TaskStatus.IN_PROGRESS.value:
        return False

    task['status'] = TaskStatus.DONE.value

    # placeholder for PDF generation
    # ...

    _log_action("completed")

    return task


# ----------- dispatcher -----------

def process_task(repo: TaskRepository, title, user_email, action, priority=None):
    if action == 1:
        return create_task(repo, title, user_email, priority)

    elif action == 2:
        return assign_task(repo, title, user_email)

    elif action == 3:
        return complete_task(repo, title)

    return None