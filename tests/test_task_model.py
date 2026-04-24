def test_task_status_transition_valid():
    from src.models.task import Task, TaskStatus

    t = Task(title="Test")
    t.change_status(TaskStatus.IN_PROGRESS)
    assert t.status == TaskStatus.IN_PROGRESS
