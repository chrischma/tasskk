from simple_term_menu import TerminalMenu
global task_file

list_of_tasks = list()

def check_if_task_file_exists():
    try:
        task_file = open('tasks.txt','r')
        print("Task-file found.")
        task_file.close()

    except FileNotFoundError:
        task_file = open("tasks.txt", "w")

def create_new_task_from_input():
    description_input = input("What's your plan for this task?")
    status_input = input("Set status...")
    new_task = task(description_input,status_input)
    #print(new_task)

    global task_file
    task_file = open('tasks.txt','a')
    task_file.writelines(f'\n{new_task.description} | {new_task.status}')
    task_file.close()

    main_menu()

def create_task_from_list(description,status):
    global new_task
    new_task = task(description,status)
    #print(new_task)

class task():
    def __init__(self,description,status):
        self.description = description
        self.status = status

def load_tasks_from_file():

    task_file = open('tasks.txt','r')
    global tasks_from_file
    tasks_from_file = task_file.readlines()
    task_file.close()

    for _ in tasks_from_file:
        try:
            description = _.split(sep=" | ")[0]
            status = _.split(sep=" | ")[1]

            create_task_from_list(description, status)
            list_of_tasks.append(new_task)

        except IndexError:
            pass


def show_tasks():
    load_tasks_from_file()

    for _ in list_of_tasks:
        print(_.description,_.status)

    print(len(list_of_tasks),'tasks found.')


def main_menu():
    main_mn = TerminalMenu(['New Task','Show Tasks','Exit'])

    choice = main_mn.show()

    if choice == 0:
        create_new_task_from_input()

    elif choice == 1:
        show_tasks()

    elif choice == 2:
        exit()

    return choice

check_if_task_file_exists()
main_menu()






