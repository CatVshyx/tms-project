from __future__ import annotations

import datetime
import smtplib
from dataclasses import dataclass
from enum import Enum
from email.mime.text import MIMEText
from typing import List, Optional


LOG_FILE = 'log.txt'


class TaskStatus(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2


@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus
    priority: int
    user_email: str
    created: datetime.datetime


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def next_id(self) -> int:
        return len(self._tasks) + 1


def _validate_title(title: str) -> None:
    """Validate task title.

    :param title: Title of the task
    :raises ValueError: If title is empty or too long
    """
    if not title:
        raise ValueError('no title')

    if len(title) > 100:
        raise ValueError('title too long')


def _log_action(message: str) -> None:
    """Write log message to file.

    :param message: Message to log
    """
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.datetime.now()}: {message}\n")


def _send_email(user_email: str, title: str) -> None:
    """Send notification email about task creation.

    :param user_email: Recipient email
    :param title: Task title
    :raises smtplib.SMTPException: If sending fails
    """
    try:
        msg = MIMEText('New task: ' + title)
        msg['Subject'] = 'Task created'
        msg['From'] = 'noreply@tms.com'
        msg['To'] = user_email

        with smtplib.SMTP('localhost') as smtp:
            smtp.send_message(msg)

    except (smtplib.SMTPException, OSError) as e:
        print(f"email error: {e}")


def create_task(
    repo: TaskRepository,
    title: str,
    user_email: str,
    priority: Optional[int] = None
) -> Task:
    """Create a new task and store it in repository.

    :param repo: Task repository
    :param title: Task title
    :param user_email: Owner email
    :param priority: Optional priority value
    :raises ValueError: If title is invalid
    :return: Created task
    """
    _validate_title(title)

    if priority is None:
        priority = 3

    task = Task(
        id=repo.next_id(),
        title=title,
        status=TaskStatus.TODO,
        priority=priority,
        user_email=user_email,
        created=datetime.datetime.now()
    )

    repo.add_task(task)

    _log_action(f"created task {title}")
    _send_email(user_email, title)

    return task


def assign_task(
    repo: TaskRepository,
    task_id: int,
    user_email: str
) -> Optional[Task]:
    """Assign a task to a user.

    :param repo: Task repository
    :param task_id: Task identifier
    :param user_email: New user email
    :return: Updated task or None if not found
    """
    task = repo.get_by_id(task_id)
    if task is None:
        return None

    task.user_email = user_email
    task.status = TaskStatus.IN_PROGRESS

    _log_action("assigned")

    return task


def complete_task(
    repo: TaskRepository,
    task_id: int
) -> Optional[Task]:
    """Mark task as completed.

    :param repo: Task repository
    :param task_id: Task identifier
    :return: Updated task, None if not found, or False-like logic avoided
    """
    task = repo.get_by_id(task_id)
    if task is None:
        return None

    if task.status != TaskStatus.IN_PROGRESS:
        return None
    task.status = TaskStatus.DONE
    _log_action("completed")
    return task


def process_task(
    repo: TaskRepository,
    value: int | str,
    user_email: str,
    action: int,
    priority: Optional[int] = None
) -> Optional[Task]:
    """Dispatch task operation based on action.

    :param repo: Task repository
    :param value: Title (for create) or task_id (for others)
    :param user_email: User email
    :param action: Action code (1=create, 2=assign, 3=complete)
    :param priority: Optional priority
    :return: Resulting task or None
    """
    if action == 1:
        return create_task(repo, str(value), user_email, priority)

    if action == 2:
        return assign_task(repo, int(value), user_email)

    if action == 3:
        return complete_task(repo, int(value))

    return None
