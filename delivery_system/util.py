

def show_opt_schedule(tasks, cost_function_type):
    """plot the optimal solution for the shipment schedule in a Gantt Chart configuration.

    :param tasks: list of shipments
    :param cost_function_type: string representing the type of the cost function.
    :return: None
    """
    import random
    from datetime import datetime, timedelta
    import plotly.figure_factory as ff

    df = []
    start_time = 0
    start = datetime.now()
    colors = {}
    for i, shipment in enumerate(tasks):
        end = start + timedelta(hours=shipment.distance)
        df.append(dict(Task=f"{shipment.client_name} - {shipment.type}",
                       Start=start.strftime("%Y-%m-%d %H:%M:%S"),
                       Finish=end.strftime("%Y-%m-%d %H:%M:%S"),
                       Resource=f"f({cost_function_type}) = {round(shipment.cost_value, 2)}",
                       title="name"))
        start = end
        colors[f"f({cost_function_type}) = {round(shipment.cost_value, 2)}"] = (random.random(),
                                                                                random.random(),
                                                                                random.random())
    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, colors=colors)
    fig.show()


def title_print(str):
    stars = '*' * (len(str) + 4 )
    print(f"\n{stars}\n* {str.title()} *\n{stars}")


if __name__ == '__main__':
    title_print("whats up man")