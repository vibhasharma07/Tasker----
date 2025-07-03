class Task:
    def __init__(self, title, description, deadline, priority):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        return f"{self.title} - {self.description} (Due: {self.deadline}, Priority: {self.priority}) [{'✓' if self.completed else '✗'}]"
