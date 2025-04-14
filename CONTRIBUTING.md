<!-- CONTRIBUTING.md is based on the provided in the Red Queen Repo: https://github.com/Qiskit/red-queen/blob/a9f396b16c88cea9c9987cd379526c0624e22323/CONTRIBUTING.md -->

# Contributing

First read the overall project contributing guidelines. These are all
included in the ReadMe file of this repo:

<https://github.com/innovateorange/DiscordBot/blob/ec161ab7b4d38fab5db17f62c353e9d673e6fbde/README.md>

## Contributing to Discord Bot Project

## Style and lint

Discord Bot Project uses two tools to verify code formatting and lint checking. The
first tool is [black](https://github.com/psf/black) which is a code formatting
tool that will automatically update the code formatting to a consistent style.
The second tool is [ruff](https://github.com/astral-sh/ruff) which is a code linter
which does a deeper analysis of the Python code to find both style issues and
potential bugs and other common issues in Python.

You can check that your local modifications conform to the style rules
by running `nox` which will run `black` and `ruff` to check the local
code formatting and lint. You will need to have [nox](https://github.com/wntrblm/nox)
installed to run this command. You can do this with `pip install -U nox`.

If black returns a code formatting error, you can run `nox -s format` to
automatically update the code formatting to conform to the style. However,
if `ruff` returns any error, you will have to resolve these issues by manually updating your code.

When you want to contribute to the Discord Bot Project, you will need to create a new branch where you will be staging your changes.

### Creating a new branch

You can do this by running the git checkout command:

```bash
git checkout -b <new_branch_name>
```

> [!TIP]
> Note that this command creates a branch base on the branch that you are currently in, so please make sure that you are on the main branch when you are making a new branch.
>
> You can see which branch you are on by using the git branch command:
>
> ```bash
> git branch
> ```

Once you are ready to push your code to the branch that you created, you have to stage the changes.

### Staging your changes

First you need to add all your changes (deltas) to a git. [You can think of this as putting all of your work into an unmarked folder]

```bash
git add -A # This adds all of the files/edits that you have made 
```

After you add your changes to git, you need to sign it with a message [You can think of this as signing the folder with your name so we know whose work is in the folder]:

```bash
git commit -am "<Title of Change>\n <Rationale behind change>" # This command signs your changes
```

> [!TIP] You can think of your commit message as an email where you explain to your team the reasoning behind your changes. You don't need to explain you changes, your deltas are visable for any reviewers. The thought behind your changes should be clearly outlined in your commit.

After you sign your changes, you need to push your changes to your branch's upstream:

For first-time commits to branch:

```bash
git push -u # This command creates an upstream version of your local branch 
```

>[!NOTE]
> The -u flag is important to track the initial tracking history of the branch itself. You're basically telling git: "Hey, from now on, whenever I'm on this branch, I want to link it to this branch on GitHub." Almost like saving contact information on your phone

For subsequent commits to branch:

```bash
git pull # Pulls changes from base repository 
git push # Pushes changes to upstream
```

### Creating a Pull Request Draft

Once you do that you can create a draft pull request on GitHub. You can do this by visting the Pull Request tab within the project repo. There should be a prompt that looks similar to this:

![image](images/pull_request_ex1.png)

Press the `Compare & pull request` button, then you will be given the option to create a pull request in this screen:

![image](images/pull_request_ex2.png)

Click the dropdown menu of the `Create pull request` button:

![image](images/pull_request_ex3.png)

And then create a draft pull request. Now you can see if your changes pass the [CI/CD](https://github.com/innovateorange/DiscordBot/actions) checks. From here you can work on your changes until it is ready for review.

Before you submit your code for review, please make sure that you have done the following:

- [ ] Ensure that your code passes all of the [CI/CD](https://github.com/innovateorange/DiscordBot/actions) checks
- [ ] You have added tests for any new features
- [ ] You have added documentation for any new features
- [ ] You have added a description of the changes you made in the pull request

> [!NOTE]
> If your pull request is missing any of the above, it will be converted back to a draft and will not be reviewed until the above conditions are met. This is to ensure we are following best practices for industry-ready code.

Once you have ensured that you have done all of the above, you can convert your draft to a pull request for review. You can do this by pressing the `Ready for review` button:

![image](images/pull_request_ex5.png)

Once you do that you are ready for code review!

### Code Review

Congrats you have made it to the part where you interact with people! Code review is an opportunity for other people to review your changes and offer you feedback. It's important to make sure that you keep an open minded in this process. Receiving feedback can be hard to begin with, but with respectful communication it will help you gains the skills of a mature software engineer.

### CI/CD Jobs

[CI/CD](https://github.com/resources/articles/devops/ci-cd) means Continuous Integration and Continuous Deployment and is a stands as our way of implementing defensive programming in our devolpement workflow.

> [!NOTE]
> This document will be updated based on the needs of the team
>
>-[Caleb](@Lementknight)

> [!NOTE]
> Code review is a two way street. You should be open to receiving feedback, but you should also be open to giving feedback. If you see something that you think could be improved, please offer your feedback in a respectful manner.
