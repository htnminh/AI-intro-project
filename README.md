# (Name)
(Description)

<!-- ![preview](https://github.com/htnminh/python-template/blob/main/docs/preview.png)
-->

## (An Introduction)



## Announcements 
13/10/2021: 
- We will start to discuss about some topics to choose from (for the first time) in Thursday (14/10) at 3 PM in our Messenger group. Everyone should be prepared for some ideas. The discussion should take about an hour.
- We will have a second discussion to select the final topic in Saturday (16/10). I will announce later.


## Guide for Collaborators
This is a guide for everything, you MUST read it carefully.


### Guide to GitHub
You should follow the following steps to get yourself familiar with GitHub. Things might get seriously worse if you do something wrong, basically bacause we are coding together. You can see the GitHub's official guide [here](https://guides.github.com/activities/hello-world/) if you cannot do some steps.


- Step 1: I think it will be the best for you to use GitHub Desktop. Download it and do the following jobs.

You MUST understand, and know how to do the following things using GitHub to manage a project, BEFORE doing anything in this repository (feel free to skip this part if you already know how to use GitHub):

- Step 2: Create a repository of your own.
- On that repository...
  - When you start working on the project for the first time:
    - Step 3: `clone`: clone the repository to your local machine.
  - Create, delete, and adjust files (for the first time and later times):
    - Step 4: `fetch`: "sync" everything that you and others have done on the repository from cloud to your local machine, you must do this EVERY TIME you start coding.
    - Step 5: Create and write a Python `hello_world.py` file in that directory. I recommend using Visual Studio Code, but you can use any IDE/editor that you are familiar with.
    - Step 6: `commit`: "make a change" to what you have done in the repository, locally. (Each commit could have multiple files change). Please, write a meaningful commit message, in which you shortly describe all what you have done (e.g. create hello_world)
    - Step 7: `push`: "push all changes", i.e. "sync" your recent commit(s) from your local machine to cloud. (Each push could have multiple commits). The best practice is to split your work in an afternoon to multiple tasks, commit each task, and push it right after each commit. (If you cannot push because of files' conflict, do not try to push the conflict up, and let everyone knows about those files right away)
    - Step 8: Take a look at your repository on the web to see your pushed commits. 
  - By now, you have a hands-on experience with basic GitHub, let's practice!
    - Step 9: Repeat from step 4 to step 8, instead in step 5, you can try to create more files, delete some files, adjust some code, and it will work magically the same way you create the `hello_world.py` file.
   

### Introduction to directories in this project
The directory...
- `AI_intro_project`: all the files used to run the project.
- `tests`: scripts used to test Python files in `AI_intro_project`.
- `publication`: all `.md` and `.pdf` files for publication.
  - `formulae`: all images of formulae used in the parent directory `publication`.


### End-to-end rules to work in this project:
- General rules
  1. (GitHub `fetch`) You must `fetch` every time before coding.
  2. (GitHub `commit` message) You should write a meaningful (and short) commit message.
  3. (GitHub files' conflict) You must announce everyone if you cannot push because of files' conflict.
  4. (Citation) Any copied content (code or text) must has a citation at the end of the file containing that content.
  5. (What did you do?) You should add a card to the `Done` column in the [project](https://github.com/htnminh/AI-intro-project/projects/1) after you have finished something. This will be easier for scoring later on.
- Coding rules
  1. (Code conventions) Every single Python line in this project should follows [PEP 8](https://www.python.org/dev/peps/pep-0008/).
  2. (Comment conventions) You must comment for every object and every method, please follow [PEP 257](https://www.python.org/dev/peps/pep-0257/).
  3. (OOP) You must use Object Oriented Programming, and try to avoid writing too much code in the main program without putting them in an object.
  4. (Absolute import) Most of the time, if you want to use an object from another file, you should use [absolute import](https://www.geeksforgeeks.org/absolute-and-relative-imports-in-python/).
  5. (Tests) There are some automated tests (in Actions tab) after your push. My tests will check for code conventions, and test your classes in every file. If any of the test fails, you must rewrite or undo (or `revert` if you know it) until all the tests are passed. (If the tests are wrong, please tell me). If there is a file that the tests show too many warnings (>10) about your code conventions, you must adjust it to reduce the convention warnings.
  6. (No Jupyter) Avoid using Jupyter notebook to code, but there will be some for reporting.
- Writing rules
<!--
  1. (Markdown for publication) Any publication file must has a raw text `.md` file (in the `publication` directory) before converting to `.pdf` or so. If you are a writer, you must learn how to use Markdown, and this is a [guide](https://guides.github.com/features/mastering-markdown/). (Everything you see here is written by Markdown, it is beautiful, and easy).
  2. (Formulae in Markdown) In a Markdown file, if you want to insert a mathematical formula, you must upload an image of the formula to the `formulae` directory, copy the permalink to that image, then paste it in the Markdown code, so the image is displayed. (The code to insert the image is `![](https://...)`. I will use LaTeX to convert those formulae to `.pdf` file).
-->

### Start working
Start working only if you understand and accept to follow the rules above. It will take some time, I know. You will soon feel everything runs smoothly.
1. Clone this repository.
2. Open your command line, change the directory to the repository location (`AI-intro-project` by default). There are more than two ways of doing this:
  - If you want to use VSCode: open GitHub Desktop, choose Open in Visual Studio Code. In VSCode, create a terminal, and the directory is already there.
  - If you want to use Windows' command line: open it and `cd` there.
3. Run `pip install .`, this will install a package named `AIIntroProject`.
4. Take a look at [`hello_world.py`](https://github.com/htnminh/AI-intro-project/blob/main/AI_intro_project/hello_world.py) and [`test_hello_world.py`](https://github.com/htnminh/AI-intro-project/blob/main/tests/test_hello_world.py) to understand importation.
5. Start doing your things. Remember to follow the rules, since you are not working alone.

<!--
# Docs
- [LICENSE]()
- [Code of Conduct]()
- [Contributing]()
- [Issue templates]()
-->
