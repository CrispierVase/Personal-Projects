import subprocess
import sys
import pexpect

user = 'CrispierVase'
args = sys.argv[1:]
with open('./github_key', 'r') as file:
	key = file.read()
if not args:
	quit(0)
if len(args) < 2:
	quit(0)
subprocess.call(f'git add {args[0]}', shell=True)
subprocess.call(f'git commit -m \"{args[1]}\"', shell=True)
subprocess.call(f'git push', shell=True)
child = pexpect.popen_spawn.PopenSpawn('git push')
child.expect('Username for \'https://github.com\':')
child.sendline(user)
child.expect(f'Password for \'https://{user}@github.com\': ')
child.sendline(key)
print('Git Repo Updated')
