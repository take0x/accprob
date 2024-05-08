# accprob

`accprob` is a command line tool for [AtCoder Problems](https://kenkoooo.com/atcoder/). This tool is inspired by [atcoder-cli](https://github.com/Tatamo/atcoder-cli).

## Installation

Before installing accprob, you need to install [pipx](https://pipx.pypa.io/) referring to [this page](https://pipx.pypa.io/stable/installation/).<br>
Then, you can install accprob by running the following command.

```bash
$ pipx install git+https://github.com/take0x/accprob.git
```

## Usage

To create a new contest project directory:
```bash
$ accprob download <AtCoder Problem URL>
```
or
```bash
$ accprob d <AtCoder Problem URL>
```

To test the solution:
```bash
$ accprob test <Problem Index> OR <Problem ID>
```
or
```bash
$ accprob t <Problem Index> OR <Problem ID>
```

Use `--help` option to see more details.

## Example
```bash
$ accprob d https://kenkoooo.com/atcoder/#/contest/show/0ee3bd11-2b7f-414c-bb91-7baf0c48a6ac
```
### No.2 is typical90_v
```bash
$ accprob t 2
Test /path/to/典型90問 難易度順/02-typical90_v? ([Y]/n):  
```
### ambiguous problem key
```bash
$ accprob t typical90_ 
ValueError: Ambiguous problem key
00-typical90_d
...
...
89-typical90_cl
Error: Ambiguous problem key. Please specify more.
```
### specify more
default command is `python main.py`.
```
/path/to/<Contest Name>/
    <Problem ID>/in/sample-1.in, /in/sample-2.in, ...
    <Problem ID>/out/sample-1.out, /out/sample-2.out, ...
    <Problem ID>/main.py
```
default: always run `python main.py` command at `/path/to/<Contest Name>/<Problem ID>/` directory.


```bash
$ accprob t typical90_e
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y (or Y or Enter)
typical90_e : sample-1.in -> sample-1.out -> JudgeResult.AC
typical90_e : sample-2.in -> sample-2.out -> JudgeResult.AC
typical90_e : sample-3.in -> sample-3.out -> JudgeResult.AC
typical90_e : sample-4.in -> sample-4.out -> JudgeResult.AC
typical90_e : sample-5.in -> sample-5.out -> JudgeResult.TLE
```
### bind commands
if you want to use pypy3 or other commands, you can use `--bind-commands` option.
```bash
$ accprob t typical90_e --bind-commands "pypy3 main.py"
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y
typical90_e : sample-1.in -> sample-1.out -> JudgeResult.AC
typical90_e : sample-2.in -> sample-2.out -> JudgeResult.AC
typical90_e : sample-3.in -> sample-3.out -> JudgeResult.AC
typical90_e : sample-4.in -> sample-4.out -> JudgeResult.AC
typical90_e : sample-5.in -> sample-5.out -> JudgeResult.AC
```

## Contributing
If you are interested in contributing to this project, please read [CONTRIBUTING.md](CONTRIBUTING.md).
