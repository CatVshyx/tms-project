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


def test_create_task_happy_path(mocker):
    repo = mocker.Mock()
    repo.save.return_value = 'task_obj'
    service = TaskService(repo, notifier=mocker.Mock())
    result = service.create_task('title', 1, 'date', 10)
    assert result == 'task_obj'

def test_create_task_invalid_title(mocker):
    repo = mocker.Mock()
    service = TaskService(repo, notifier=mocker.Mock())

    try:
        service.create_task('', 1, 'date', 10)
        assert False
    except ValueError:
        assert True
def test_create_task_calls_repo_save(mocker):

    repo = mocker.Mock()
    service = TaskService(repo, notifier=mocker.Mock())

    service.create_task('title', 1, 'date', 10)

    repo.save.assert_called_once()
