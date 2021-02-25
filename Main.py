from simple_term_menu import TerminalMenu
from colorama import Fore, Back, Style
global task_file
import os
import time

def load_status_list_from_file():
    global status_file

    try:
        status_file = open('status.txt', 'r')
    except FileNotFoundError:
        status_file = open('status.txt','w')
        status_file.writelines('Done\nIn Progress\nUp Next')
        status_file = open('status.txt', 'r')

    global list_of_status
    list_of_status = status_file.read().splitlines()

    status_file.close()

class status():
    def __init__(self,name,color):
        self.name = name
        self.color = color

def create_status():
    name_input = input('Name for new status \n')
    new_status = status(name_input,'Custom Color')
    load_status_list_from_file()
    list_of_status.append(str(new_status.name+' | '+new_status.color))

    status_file = open('status.txt','w')

    for _ in list_of_status:
        status_file.writelines(_)
        status_file.writelines('\n')

    status_file.close()

    load_status_list_from_file()

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
    os.system('clear')
    print('Please set a status for your task: ')
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

    print('Your tasks: ')

    for _ in list_of_tasks:

        if _.status == 'Done':
            color = Back.GREEN

        elif _.status == 'In Progress':
            color = Back.MAGENTA

        elif _.status == 'Up Next':
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
        print('Task deleted.')
        time.sleep(1)
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
    show_tasks()
    main_menu()

def main_menu():
    os.system('clear')
    choice = TerminalMenu(['My Tasks','New Task','Edit Tasks','Edit Status','Exit']).show()

    if choice == 0:
        show_tasks()

    elif choice == 1:
        create_new_task_from_input()

    elif choice == 2:
        edit_tasks()

    elif choice == 3:
        os.system('open status.txt')

    elif choice == 4:
        exit()

    return choice

check_if_task_file_exists()
load_status_list_from_file()
show_tasks()
main_menu()

