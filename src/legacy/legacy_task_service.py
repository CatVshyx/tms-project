# legacy_task_service.py – Реальний legacy-код для аналізу
# Знайдіть і класифікуйте всі Code Smells!
import datetime, json, os, smtplib
from email.mime.text import MIMEText
TASKS = [] # Глобальний стан! Code Smell: Global State
USERS = {}
LOG_FILE = 'log.txt' # Hardcoded path


def process(t, u, act, p=None): # Незрозумілі назви! Code Smell: Cryptic Names
    """Process task""" # Порожня документація
    if act == 1:
        if t is None or t == '' or len(t) == 0: # Дублювання логіки
            print('error: no title') # print замість logging
            return None
        if len(t) > 100:
            print('error: title too long')
            return None
        if p is None:
            p = 3 # Magic Number: що означає 3?
        task = {'id': len(TASKS) + 1, 'title': t, # не UUID!
            'status': 0, # Magic Number: 0 = TODO?
            'priority': p, 'user': u,
            'created': str(datetime.datetime.now())}
        TASKS.append(task)
        # Логування з дублюванням
        f = open(LOG_FILE, 'a') # не закрито! Resource Leak
        f.write(str(datetime.datetime.now()) + ': created task ' + t +'\n')
        
        # Відправка email прямо тут (порушення SRP)
        try:
            msg = MIMEText('New task: ' + t)
            msg['Subject'] = 'Task created'
            msg['From'] = 'noreply@tms.com'
            msg['To'] = u
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()
        except:
            pass # Проковтування виняків! Bare except
        return task
    elif act == 2: # Magic Number: 2 = assign?
        for task in TASKS: # O(n) пошук щоразу
            if task['id'] == t: # t тут – вже id, не title! Перевантаження параметрів
                task['user'] = u
                task['status'] = 1 # Magic: 1 = IN_PROGRESS?
                f = open(LOG_FILE, 'a') # Знову незакритий файл
                f.write(str(datetime.datetime.now()) + ': assigned\n')
                return task
        return None
    elif act == 3: # Magic: 3 = complete?
        for task in TASKS:
            if task['id'] == t:
                if task['status'] != 1: # Magic: 1 = IN_PROGRESS
                    return False
            task['status'] = 2 # Magic: 2 = DONE?
            # 20+ рядків генерації PDF звіту прямо тут...
            # ... (уявіть ще 20 рядків)
            f = open(LOG_FILE, 'a')
            f.write(str(datetime.datetime.now()) + ': completed\n')
            return task
            # Немає else → повертає None без попередження