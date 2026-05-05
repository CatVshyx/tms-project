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



def test_get_tasks_by_assignee(mocker):
    repo = mocker.Mock()
    repo.get_by_assignee.return_value = [1, 2]

    service = TaskService(repo, notifier=mocker.Mock())

    result = service.get_tasks_by_assignee(10)

    assert result == [1, 2]

def test_get_tasks_by_assignee_empty(mocker):
    repo = mocker.Mock()
    repo.get_by_assignee.return_value = []
    service = TaskService(repo, notifier=mocker.Mock())

    result = service.get_tasks_by_assignee(10)

    assert result == []

def test_assign_task_sets_assignee(mocker):
    task = Task(1, 'Deploy', 'MEDIUM', '2026-06-01', creator_id=5)
    repo = mocker.Mock()
    repo.get_by_id.return_value = task
    notifier = mocker.Mock()

    service = TaskService(repo, notifier)
    result = service.assign_task(task_id=1, assignee_id=99)

    assert result.assignee_id == 99