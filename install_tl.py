import pexpect
from glob import glob
import os
import sys


def command(pattern, send, **kwargs):
    child.expect(pattern, **kwargs)
    print(child.before.decode())
    print(child.after.decode())
    child.sendline(send)

if __name__ == '__main__':
    install_script = glob('install-tl-*/install-tl')

    child = pexpect.spawn(install_script)

    try:
        command('Import settings from previous TeX Live installation', 'n', timeout=10)
    except pexpect.TIMEOUT:
        print('No previous installation found')

    try:
        command('Enter command:', 'C', timeout=10)
        command('Enter letter', '-acfghkyIKLMSW',  timeout=10)
        command('Enter letter', 'R',  timeout=10)
        command('Enter command:', 'I', timeout=10)
    except pexpect.TIMEOUT:
        print('Something went wrong')
        sys.exit(1)

    try:
        while not child.terminated:
            print(child.readline().decode().strip())
    except pexpect.EOF:
        print('Installation seems to be finished')

    if 'Welcome' not in child.read():
        print('Installation did not terminate successfull')
        sys.exit(1)
