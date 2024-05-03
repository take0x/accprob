import os
import json
import sys
import subprocess

def main():
    with open('../contest-info.json', 'r') as f:
        info = json.load(f)

    problem_num = int(os.getcwd().split('/')[-1])
    url = info[str(problem_num)]['url']

    file = sys.argv[1]

    command = ["oj", "s", url, file]
    subprocess.run(
        command,
        # stdout=subprocess.DEVNULL,
        check=True,
    )



if __name__ == '__main__':
    main()
