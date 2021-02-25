from simple_term_menu import TerminalMenu
from colorama import Fore, Back, Style
global task_file
import os

sts_done = "Done"
sts_in_progress = "In Progress"
sts_next = "Up Next"

list_of_status = [sts_done,sts_in_progress,sts_next]
list_of_tasks = list()

def check_if_task_file_exists():
    try:
        task_file = open('tasks.txt','r')
        task_file.close()

    except FileNotFoundError:
        task_file = open("tasks.txt", "w")

def create_new_task_from_input():
    description_input = input("What's your plan for this task? ")



    new_task = task(description_input,get_status_by_user_input())

    global task_file
    task_file = open('tasks.txt','a')
    task_file.writelines(f'{new_task.status} | {new_task.description} \n')
    task_file.close()

    main_menu()

def get_status_by_user_input():
    status_choice = TerminalMenu(list_of_status).show()
    status_input = list_of_status[status_choice]
    return status_input

def create_task_from_list(description,status):
    global new_task
    new_task = task(description,status)

class task():
    def __init__(self,description,status):
        self.description = description
        self.status = status

def load_tasks_from_file():
    global list_of_tasks
    list_of_tasks = list()

    task_file = open('tasks.txt','r')
    global tasks_from_file
    tasks_from_file = task_file.readlines()
    task_file.close()

    for _ in tasks_from_file:
        try:
            status = _.split(sep=" | ")[0]
            description = _.split(sep=" | ")[1]

            create_task_from_list(description, status)
            list_of_tasks.append(new_task)

        except IndexError:
            pass

def show_tasks():
    os.system('clear')
    load_tasks_from_file()

    for _ in list_of_tasks:

        if _.status == sts_done:
            color = Back.GREEN

        elif _.status == sts_next:
            color = Back.MAGENTA

        elif _.status == sts_in_progress:
            color = Back.YELLOW

        else:
            color = Back.BLACK

        print(color,str(_.status).ljust(11),Style.RESET_ALL,_.description.replace("\n",""))

    TerminalMenu(["Ok."]).show()
    os.system("clear")
    main_menu()

def save_task_list_to_file():
    task_file = open('tasks.txt','w')
    for _ in list_of_tasks:
        task_file.writelines(f'{_.status} | {_.description} \n')
    task_file.close()

def edit_tasks():
    load_tasks_from_file()
    task_descriptions = list()

    for _ in list_of_tasks:
        task_descriptions.append(_.description.strip())

    index_of_edited_task = TerminalMenu(task_descriptions).show()

    edit_menu = TerminalMenu(['New Task','Change Description','Change Status','Delete Task']).show()

    def delete_task():
        list_of_tasks.pop(index_of_edited_task)
        save_task_list_to_file()

    def change_description():
        user_input = input('Please enter your new description: \n')
        list_of_tasks[index_of_edited_task].description = user_input
        save_task_list_to_file()

    def change_status():
        list_of_tasks[index_of_edited_task].status = get_status_by_user_input()

    if edit_menu == 0:
        create_new_task_from_input()

    elif edit_menu == 1:
        change_description()

    elif edit_menu == 2:
        change_status()

    elif edit_menu == 3:
        delete_task()

    save_task_list_to_file()
    main_menu()



def main_menu():
    os.system('clear')
    choice = TerminalMenu(['My Tasks','Edit Tasks','Exit']).show()

    if choice == 0:
        show_tasks()


    elif choice == 1:
        edit_tasks()

    elif choice == 2:
        exit()

    return choice

check_if_task_file_exists()
main_menu()

