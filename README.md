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

for example
```bash
$ accprob t typical90_e
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y (or Y or Enter)
typical90_e : sample-1.in -> (0.04 [s]) -> sample-1.out | Result: JudgeResult.AC
typical90_e : sample-2.in -> (0.02 [s]) -> sample-2.out | Result: JudgeResult.AC
typical90_e : sample-3.in -> (0.03 [s]) -> sample-3.out | Result: JudgeResult.RE
typical90_e : sample-4.in -> (0.03 [s]) -> sample-4.out | Result: JudgeResult.RE
typical90_e : sample-5.in -> (0.02 [s]) -> sample-5.out | Result: JudgeResult.RE
```
or
```bash
$ accprob t 75
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y (or Y or Enter)
typical90_e : sample-1.in -> (0.04 [s]) -> sample-1.out | Result: JudgeResult.AC
typical90_e : sample-2.in -> (0.02 [s]) -> sample-2.out | Result: JudgeResult.AC
typical90_e : sample-3.in -> (0.03 [s]) -> sample-3.out | Result: JudgeResult.RE
typical90_e : sample-4.in -> (0.03 [s]) -> sample-4.out | Result: JudgeResult.RE
typical90_e : sample-5.in -> (0.02 [s]) -> sample-5.out | Result: JudgeResult.RE
```

### show detail
```bash
$ accprob t 75 --show-detail
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y
================================================================ 

Result: JudgeResult.AC
Time: 0.03508258300007583[s]
Return code: 0

In:
3 7 3
1 4 9

Your Out:
3

Expected:
3


================================================================ 

Result: JudgeResult.AC
Time: 0.02223887500008459[s]
Return code: 0

In:
5 2 3
1 4 9

Your Out:
81

Expected:
81


================================================================ 

Result: JudgeResult.RE
Time: 0.020535999999992782[s]
Return code: 127

In:
10000 27 7
1 3 4 6 7 8 9

Your Out:

Expected:
989112238


================================================================ 

Result: JudgeResult.RE
Time: 0.017910125000071275[s]
Return code: 127

In:
1000000000000000000 29 6
1 2 4 5 7 9

Your Out:

Expected:
853993813


================================================================ 

Result: JudgeResult.RE
Time: 0.01573075000010249[s]
Return code: 127

In:
1000000000000000000 957 7
1 2 3 5 6 7 9

Your Out:

Expected:
205384995
```

OK. The result is RE. You can see the detail of the test.

### bind commands
then, you fixed the bug and want to test it again.
```bash
$ accprob t typical90_e
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y
typical90_e : sample-1.in -> (0.04 [s]) -> sample-1.out | Result: JudgeResult.AC
typical90_e : sample-2.in -> (0.02 [s]) -> sample-2.out | Result: JudgeResult.AC
typical90_e : sample-3.in -> (0.03 [s]) -> sample-3.out | Result: JudgeResult.AC
typical90_e : sample-4.in -> (0.03 [s]) -> sample-4.out | Result: JudgeResult.AC
typical90_e : sample-5.in -> (9.46 [s]) -> sample-5.out | Result: JudgeResult.TLE
```
the result is TLE. python is so slow.
if you want to use pypy3 or other commands, you can use `--bind-commands` option.

```bash
$ accprob t typical90_e --bind-commands "pypy3 main.py"
Test /path/to/典型90問 難易度順/75-typical90_e? ([Y]/n): y
typical90_e : sample-1.in -> (0.04 [s]) -> sample-1.out | Result: JudgeResult.AC
typical90_e : sample-2.in -> (0.02 [s]) -> sample-2.out | Result: JudgeResult.AC
typical90_e : sample-3.in -> (0.02 [s]) -> sample-3.out | Result: JudgeResult.AC
typical90_e : sample-4.in -> (0.02 [s]) -> sample-4.out | Result: JudgeResult.AC
typical90_e : sample-5.in -> (0.22 [s]) -> sample-5.out | Result: JudgeResult.AC
```

OK. It's fast.

## Contributing
If you are interested in contributing to this project, please read [CONTRIBUTING.md](CONTRIBUTING.md).
