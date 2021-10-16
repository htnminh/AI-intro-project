# Capstone Project for Intro to AI course.

<!-- ![preview](https://github.com/htnminh/python-template/blob/main/docs/preview.png)
-->


## Announcements
16/10/2021:
  - Final reminder to do topic & description for the upcoming deadline at 17/10/2021 23h59.
  - After publishing, please also move the corresponding TO-DO in GitHub/Projects/AI_Capstone_Project/To_do to the column Done.


All older announcements can be found in ANNOUNCEMENTS.md


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
    - Step 4: `fetch` and `pull`: "sync" everything that you and others have done on the repository from cloud to your local machine, you must do this EVERY TIME you start coding.
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
- `publication`: all `.ipynb` and `.pdf` files for publication.


### End-to-end rules to work in this project
- General rules
  1. (GitHub `fetch`) You must `fetch` (and `pull`) every time before making changes and/or uploading to the repo.
  2. (GitHub `commit` message) You should write a meaningful (and short) commit message. Description is helpful if you are making lots of changes.
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
  1. (Jupyter) Write reports using Jupyter notebook, even if there is no code or mathematical formula.
  2. (Structure) A report must has a hierarchical structure, using Markdown in text cells of the notebook ([Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)).
  3. (Mathematical formulae) You can format a mathematical formula using LaTeX between `$ ... $` in text cells ([an example](https://github.com/htnminh/AI-intro-project/blob/fc835b8cf00a72818d5662f27fde46979cc71470/publication/hello_world_example.PNG), [LaTeX formula Cheat Sheet](http://tug.ctan.org/info/undergradmath/undergradmath.pdf))

### Guide to publication
1. Write contents using ONLY Markdown, (do not use HTML), in a Jupyter notebook.
2. Convert to LaTeX by running `jupyter notebook` in your local machine, then export the notebook as a TeX file.
![](https://github.com/htnminh/AI-intro-project/blob/c1b88055c082e37e3235a257c6762ef461b0b3dc/publication/Convert%20to%20TeX.PNG)
3. Upload the TeX file to <https://www.overleaf.com/project>, compile it, then download the compiled PDF file. Remember to choose XeLaTeX as a compiler if the document has Vietnamese characters.
![](https://github.com/htnminh/AI-intro-project/blob/fe8618597e60cc2ee088ec4ee46feb38f0b5e4af/publication/Compiler%20XeLaTeX.PNG)


<!--
### Start working
Start working only if you understand and accept to follow the rules above. It will take some time, I know. You will soon feel everything runs smoothly.
1. Clone this repository.
2. Open your command line, change the directory to the repository location (`AI-intro-project` by default). There are more than two ways of doing this:
  - If you want to use VSCode: open GitHub Desktop, choose Open in Visual Studio Code. In VSCode, create a terminal, and the directory is already there.
  - If you want to use Windows' command line: open it and `cd` there.
3. Run `pip install .`, this will install a package named `AIIntroProject`.
4. Take a look at [`hello_world.py`](https://github.com/htnminh/AI-intro-project/blob/main/AI_intro_project/hello_world.py) and [`test_hello_world.py`](https://github.com/htnminh/AI-intro-project/blob/main/tests/test_hello_world.py) to understand importation.
5. Start doing your things. Remember to follow the rules, since you are not working alone.
-->

<!--
# Docs
- [LICENSE]()
- [Code of Conduct]()
- [Contributing]()
- [Issue templates]()
-->
