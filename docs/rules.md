- General rules
  1. (GitHub `fetch`) You must `fetch` (and `pull`) every time before making changes and/or uploading to the repo.
  2. (GitHub `commit` message) You should write a meaningful (and short) commit message. Description is helpful if you are making lots of changes.
  3. (GitHub files' conflict) You must announce everyone if you cannot push because of files' conflict.
  4. (Citation) Any copied content (code or text) must has a citation at the start or the end of the file containing that content.

- Coding rules
  1. (Code conventions) Every single Python line in this project should follows [PEP 8](https://www.python.org/dev/peps/pep-0008/).
  2. (Comment conventions) You must comment for every object and every method, please follow [PEP 257](https://www.python.org/dev/peps/pep-0257/).
  3. (OOP) You must use Object Oriented Programming, and try to avoid writing too much code in the main program without putting them in an object.
  4. (Absolute import) If you want to use an object from another file, you should use [absolute import](https://www.geeksforgeeks.org/absolute-and-relative-imports-in-python/). For example, `from AI_intro_project.Coordinate_and_Move import Coordinate`.
  5. (Tests) There are some automated tests (in Actions tab) after your push. My tests will check for code conventions, and test your classes in every file. If any of the test fails, you must rewrite or undo (or `revert` if you know it) until all the tests are passed. (If the tests are wrong, please tell me). If there is a file that the tests show too many warnings (>10) about your code conventions, you must adjust it to reduce the convention warnings.
  6. (No Jupyter) Avoid using Jupyter notebook to code, but there will be some for reporting.
- Writing rules
  1. (Structure) A report must has a hierarchical structure, using Markdown in text cells of the notebook ([Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)).
  2. (Mathematical formulae) You can format a mathematical formula using LaTeX between `$ ... $` in text cells ([an example](https://github.com/htnminh/AI-intro-project/blob/fc835b8cf00a72818d5662f27fde46979cc71470/publication/hello_world_example.PNG), [LaTeX formula Cheat Sheet](http://tug.ctan.org/info/undergradmath/undergradmath.pdf))
