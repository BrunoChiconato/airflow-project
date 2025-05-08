def _handle_failed_dag_run(ctx):
    print(
        f"""DAG Run failes with the task {ctx["task_instance"].task_id}
        for the data interval between {ctx["prev_ds"]} and {ctx["next_ds"]}"""
    )


def _handle_empty_size(ctx):
    print(
        f"""There is no cocktail to process for the data interval between 
        {ctx["prev_ds"]} and {ctx["next_ds"]}"""
    )