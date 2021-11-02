from scheduling_package.task import Task
import plotly.figure_factory as ff


class IScheduleMultiples:
    """this class will analize the schedule for multiple
        choices for tasks, and the minimum machines needed"""
    def __init__(self, tasks_dict) -> None:
        super().__init__()
        self.tasks_dict = tasks_dict

    def comp_max_tasks(self, tasks_name_to_exclude=None):
        """compute the schedule of the maximum tasks
           O( n^2 )

            Returns:
                  list of compatible tasks
        """
        if tasks_name_to_exclude is None:
            tasks_name_to_exclude = []

        tasks_list = [t for tasks in self.tasks_dict.values()
                            for t in tasks if t.name not in tasks_name_to_exclude]

        if len(tasks_list) == 0:
            return None

        sorted_tasks_by_end = sorted(tasks_list, key=lambda t: t.end)
        max_compatible_tasks = [sorted_tasks_by_end[0]]

        # mark the name of the person to avoid taking him again later
        taken_tasks = [max_compatible_tasks[-1].name]

        for task in sorted_tasks_by_end:
            if task.start >= max_compatible_tasks[-1].end \
                    and task.name not in taken_tasks:
                max_compatible_tasks.append(task)
                taken_tasks.append(task.name)

        return max_compatible_tasks

    def comp_min_resources(self):
        """calculates the minimum number of machines needed
            O( n^3 )

            Returns:
                number of machines
        """
        resources = 0
        tasks_to_exclude = []
        while True:
            compatible_tasks = self.comp_max_tasks(tasks_name_to_exclude=tasks_to_exclude)
            if compatible_tasks is None:
                break
            tasks_to_exclude.extend([t.name for t in compatible_tasks])
            resources += 1

        return resources

    def show_opt_schedule(self, tasks=None):
        """plot the optimat solution or the tasks that are given"""
        if tasks is None:
            tasks = self.comp_max_tasks()
        df = []
        for t in tasks:
            df.append(dict(Task=t.name,
                           Start=f'2020-01-01 {t.start}:00:00',
                           Finish=f'2020-01-01 {t.end}:00:00'))
        fig = ff.create_gantt(df)
        fig.show()

    def show_schedule_multiple_shower(self):
        """plot the full schedule contining all the persons in multiple showers"""
        allready_ploted = []
        for _ in range(self.comp_min_resources()):
            tasks = self.comp_max_tasks(tasks_name_to_exclude=allready_ploted)
            allready_ploted.extend([t.name for t in tasks])
            self.show_opt_schedule(tasks=tasks)


if __name__ == '__main__':
    tasks = {
        'Leela': [Task("Leela", 8, 10), Task("Leela", 17, 19)],
        'Fry': [Task("Fry", 9, 10), Task('Fry', 20, 22)],
        'Bender': [Task('Bender', 18, 19)],
        'Hermes': [Task('Hermes', 12, 13), Task("Hermes", 15, 17)],
        'Amy': [Task('Amy', 10, 16)],
        'Zoidberg': [Task('Zoidberg', 16, 17)],
        'Nibbler': [Task('Nibbler', 19, 21)]
    }

    scheduler = IScheduleMultiples(tasks)
    print(scheduler.comp_min_resources())
    # scheduler.show_opt_schedule()
    scheduler.show_schedule_multiple_shower()