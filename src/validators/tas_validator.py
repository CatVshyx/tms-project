class TaskValidator:
    def is_title_valid(self, title) -> bool:
        if title is None:
            return False

        title = title.strip()

        if len(title) == 0:
            return False

        if len(title) > 100:
            return False

        return True