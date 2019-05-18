from flask import Flask, session, redirect, url_for, escape, request, render_template, Markup
import static.probe_one

app = Flask(__name__)


@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/remindozaur')
def remindozaur():
    return render_template('remindozaur.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route("/submit_form", methods=['GET', 'POST'])
def submit_form():
    idd = static.probe_one.find_list()
    new_task_dict = request.form
    print(new_task_dict)
    if 'money' in new_task_dict:
        money = new_task_dict['money']
    else:
        money = '0'
    task = static.probe_one.task_creation_web(new_task_dict['title'], new_task_dict['notes'],
                                              new_task_dict['date'], money)
    print(task)
    static.probe_one.add_task(static.probe_one.myAddTask(task), idd)
    return redirect("/my_tasks")


@app.route("/my_tasks", methods=['GET', 'POST'])
def my_tasks():
    idd = static.probe_one.find_list()
    all_tasks = static.probe_one.find_all_tasks(idd)
    for task in all_tasks:
        task[1] = Markup(task[1].replace("\n", "<br>"))
    print(all_tasks)

    # return redirect("/")
    return render_template('my_tasks.html', all_tasks=all_tasks)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
