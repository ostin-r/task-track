import sys
import json
import time
import os


def _write_data(data):
    with open('tasks.json', 'w') as f:
        json.dump(data, f)


def start_task(task_name):
    if not os.path.exists('tasks.json'):
        with open('tasks.json', 'w') as f:
            json.dump({}, f)
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    if task_name not in tasks:
        tasks[task_name] = {
            'name': task_name,
            'time_intervals': [{'start': time.time(), 'end': None}],
            'duration': 0
        }
    else:
        task = tasks[task_name]
        if task['time_intervals'][-1]['end'] is None:
            print(f'Task {task_name} has already been started.  Run \'track stop <task_name>\' to complete the task first.')
            return -1
        task['time_intervals'].append({
            'start': time.time(),
            'end': None
        })
    print(f'Task {task_name} has been successfully started')
    _write_data(tasks)


def stop_task(task_name):
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    if task_name not in tasks:
        print(f'Task {task_name} could not be found in the current task list, try \'track ls\' to see active tasks.')
        return -1
    task = tasks[task_name]
    last_interval = task['time_intervals'][-1]
    last_interval['end'] = time.time()
    duration = 0
    for interval in task['time_intervals']:
        duration += interval['end'] - interval['start']
    task['duration'] = duration
    _write_data(tasks)

    minutes_spent = task['duration'] / 60
    print(f'Task {task_name} successfully stopped. Session time: {minutes_spent} minutes.  \nTo see total time spent on tasks, view the report with \'track report\'')


def list_tasks(show_all=None):
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
    except:
        tasks = {}
    if len(tasks) == 0:
        print('No tasks have been started, run \'track start <task_name>\' to get started')
    else:
        print('Task Name -- Time Spent (min)')
    for name in tasks:
        if show_all:
            duration = tasks[name]['duration']
            minutes_spent = round(duration / 60)
            print(f'{name} -- {minutes_spent}')
        elif tasks[name]['time_intervals'][-1]['end'] is None:
            duration = tasks[name]['duration']
            minutes_spent = round(duration / 60)
            print(f'{name} -- {minutes_spent}')


if __name__ == '__main__':
    print(f'args = {sys.argv}')
    if sys.argv[1] == 'start':
        if len(sys.argv) == 3 and isinstance(sys.argv[1], str):
            start_task(sys.argv[2])
        else:
            print('Incorrect usage of \'start\' command. Try \'task start <unique_task_name>\'')
    elif sys.argv[1] == 'stop':
        if len(sys.argv) == 3 and isinstance(sys.argv[1], str):
            stop_task(sys.argv[2])
        else:
            print('Incorrect usage of \'stop\' command. Try \'task stop <unique_task_name>\'')
    elif sys.argv[1] == 'ls':
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            print('Incorrect usage of \'ls\' command.  Use \'track ls\' or \'track ls -a\'')
    else:
        print('unkown arguments given')

