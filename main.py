import json
from subprocess import Popen, PIPE
import sys
from threading import Thread


def buildTunnel(command):
    coreProcess = Popen(command, stdout=PIPE, stdin=PIPE)
    fileEditor = open('history' + '.txt', "w+")
    Thread(target=myMessage, args=[coreProcess, fileEditor]).start()
    Thread(target=hisMessage, args=[coreProcess, fileEditor]).start()


def myMessage(coreProcess, fileEditor):
    while True:
        message = input()
        message = json.dumps(message) + '\n'
        coreProcess.stdin.write(bytes(message, 'utf8'))
        coreProcess.stdin.flush()
        fileEditor.write('1: ' + message + '\n')
        fileEditor.flush()
        if message == 'bye':
            fileEditor.close()
            coreProcess.terminate()
            sys.exit()


def hisMessage(coreProcess, fileEditor):
    while True:
        output = coreProcess.stdout.readline().decode()
        message = json.loads(output)
        print('2: ' + message)
        fileEditor.write('2: ' + message + '\n')
        fileEditor.flush()
        if output == '':
            fileEditor.close()
            coreProcess.terminate()
            sys.exit()


if __name__ == "__main__":
    print(' type "server" to choose server\n type "client" to choose client\n type "bye" to exit')
    cmd = {'server': ['netcat', '-l', '-p', '1234'], 'client': ['netcat', 'localhost', '1234']}
    side = input()
    buildTunnel(cmd[side])
