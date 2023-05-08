from invoke import task
#   Tasks:
#
# poetry run invoke <task>
# poetry run invoke --list
#
# use kebab-case when running
# invokes from CLI.
@task
def foo(ctx):
    print("bar")

# Runs the program.
@task
def start(ctx):
    ctx.run("python3 src/main.py", pty=True)

# Run tests in src folder.
@task
def test(ctx):
    ctx.run("pytest src", pty=True)

# Check for test coverage. Runs pytest only in 
# src folder.
@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

# Generates the coverage report. 'coverage'-task
# is given as a parameter to this task to
# make it a dependancy. Now 'coverage'-task
# is always run before this task.
@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage report -m", pty=True)
    ctx.run("coverage html", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)
    