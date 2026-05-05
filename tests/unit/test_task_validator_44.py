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
        task.status = new_status
        return task
    

def test_change_status_updates_status(mocker):
    task = Task(1, 'Deploy', 'HIGH', '2026-06-01', creator_id=5)
    repo = mocker.Mock()
    repo.get_by_id.return_value = task

    service = TaskService(repo, notifier=mocker.Mock())
    result = service.change_status(1, 'DONE')

    assert result.status == 'DONE'

def test_change_status_returns_task(mocker):
    task = Task(1, 'Deploy', 'HIGH', '2026-06-01', creator_id=5)
    repo = mocker.Mock()
    repo.get_by_id.return_value = task

    service = TaskService(repo, notifier=mocker.Mock())
    result = service.change_status(1, 'IN_PROGRESS')

    assert result is task

def test_change_status_fetches_correct_task_id(mocker):
    task = Task(7, 'Review', 'LOW', '2026-06-01', creator_id=2)
    repo = mocker.Mock()
    repo.get_by_id.return_value = task

    service = TaskService(repo, notifier=mocker.Mock())
    service.change_status(7, 'DONE')

    repo.get_by_id.assert_called_once_with(7)