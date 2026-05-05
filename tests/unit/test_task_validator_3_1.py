import pytest

ALLOWED = {
        'NEW': ['ASSIGNED', 'CANCELLED'],
        'ASSIGNED': ['IN_PROGRESS', 'CANCELLED'],
        'IN_PROGRESS': ['DONE', 'CANCELLED'],
        'DONE': [],
        'CANCELLED': [],
}

class Task:
    def __init__(self, id, title, priority, due_date, creator_id):
        self.id = id
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.creator_id = creator_id
        self.assignee_id = None
        self.status = 'NEW'

class TaskService:
    def __init__(self, repo, notifier):
        self.repo = repo
        self.notifier = notifier

    def create_task(self, title, priority, due_date, creator_id):
        if not title:
            raise ValueError('Invalid title')

        task = Task(None, title, priority, due_date, creator_id)
        return self.repo.save(task)
    
    def assign_task(self, task_id, assignee_id):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError('Task not found')
        self.notifier.notify(task)  
        task.assignee_id = assignee_id
        return task
    def get_tasks_by_assignee(self, assignee_id):
        return self.repo.get_by_assignee(assignee_id)
    

    def change_status(self, task_id, new_status):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError('Task not found')
        allowed = ALLOWED.get(task.status, [])
        if new_status not in allowed:
            raise ValueError('Invalid transition')
        task.status = new_status
        self.notifier.notify(task)
        return task
    
TRANSITIONS = [
    # from, to, allowed

    # NEW
    ('NEW', 'NEW', False),
    ('NEW', 'ASSIGNED', True),
    ('NEW', 'IN_PROGRESS', False),
    ('NEW', 'DONE', False),
    ('NEW', 'CANCELLED', True),

    # ASSIGNED
    ('ASSIGNED', 'NEW', False),
    ('ASSIGNED', 'ASSIGNED', False),
    ('ASSIGNED', 'IN_PROGRESS', True),
    ('ASSIGNED', 'DONE', False),
    ('ASSIGNED', 'CANCELLED', True),

    # IN_PROGRESS
    ('IN_PROGRESS', 'NEW', False),
    ('IN_PROGRESS', 'ASSIGNED', False),
    ('IN_PROGRESS', 'IN_PROGRESS', False),
    ('IN_PROGRESS', 'DONE', True),
    ('IN_PROGRESS', 'CANCELLED', True),

    # DONE
    ('DONE', 'NEW', False),
    ('DONE', 'ASSIGNED', False),
    ('DONE', 'IN_PROGRESS', False),
    ('DONE', 'DONE', False),
    ('DONE', 'CANCELLED', False),

    # CANCELLED
    ('CANCELLED', 'NEW', False),
    ('CANCELLED', 'ASSIGNED', False),
    ('CANCELLED', 'IN_PROGRESS', False),
    ('CANCELLED', 'DONE', False),
    ('CANCELLED', 'CANCELLED', False),
]

@pytest.mark.parametrize("from_status,to_status,allowed", TRANSITIONS)
def test_status_transitions(mocker, from_status, to_status, allowed):

    task = mocker.Mock()
    task.status = from_status

    repo = mocker.Mock()
    repo.get_by_id.return_value = task

    service = TaskService(repo, notifier=mocker.Mock())

    if allowed:
        result = service.change_status(1, to_status)
        assert result.status == to_status
    else:
        with pytest.raises(ValueError):
            service.change_status(1, to_status)