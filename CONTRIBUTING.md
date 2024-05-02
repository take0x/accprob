# Contributing to accprob

The accprob project welcomes contributions from everyone.

## Setting up the development environment

We use [Rye](https://rye-up.com/) to manage dependencies so you need to [install it](https://rye-up.com/guide/installation/) first.

After installing Rye, you can install the dependencies by running the following command:

```bash
$ rye sync
```

Then you can run scripts by activating the virtual environment:

```bash
# If you are using Unix-like OS
$ . .venv/bin/activate

# If you are using Windows
$ .venv\Scripts\activate

# Now you can run accprob
$ accprob
```

## Modifying/Adding code

If you want to add dependencies, you can add them by running the following command:

```bash
$ rye add package1 package2 ... && rye sync
```

## Linting and Formatting

We highly recommend using VSCode because we have included the settings for linting and formatting in the `.vscode` directory.

If you don't want to use VSCode, you need to run the following commands before committing your changes:

To lint:
```bash
$ rye run ruff check && rye run mypy .
```

To format:
```bash
$ rye run ruff check --select I --fix && rye run ruff format
```
