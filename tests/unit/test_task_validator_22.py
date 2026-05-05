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


def test_assign_task_happy(mocker):
    task = mocker.Mock()
    repo = mocker.Mock()
    repo.get_by_id.return_value = task
    notifier = mocker.Mock()

    service = TaskService(repo, notifier)
    result = service.assign_task(1, 20)
    assert task.assignee_id == 20
    assert result == task

def test_assign_task_not_found(mocker):
    repo = mocker.Mock()
    repo.get_by_id.return_value = None
    service = TaskService(repo, notifier=mocker.Mock())
    try:
        service.assign_task(1, 20)
        assert False
    except ValueError:
        assert True

def test_assign_task_sends_notification(mocker):
    task = mocker.Mock()
    repo = mocker.Mock()
    repo.get_by_id.return_value = task

    notifier = mocker.Mock()

    service = TaskService(repo, notifier)
    service.assign_task(1, 20)

    notifier.notify.assert_called_once()