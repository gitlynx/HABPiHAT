"""
Simple framework to implement line-oriented command interpreter
"""
import sys
from typing import Dict, List, Tuple, final

PROMPT = '(Cmdr) '

class Cmd:
    """ Command base class """

    def __init__(self, command: str) -> None:
        self._command = command

    def get_name(self) -> str:
        """ Get command name """
        return self._command

    def _get_methods(self) -> List:
        return {method.strip('do_'): method for method in dir(self)
                if callable(getattr(self, method)) and method.startswith('do_')}

    @final
    def do_help(self, arg=None) -> None:
        ''' List available subcommands with "help" or detailed help with "help subcmd" '''
        if arg:
            try:
                doc = getattr(self, self._get_methods()[arg]).__doc__
                if doc:
                    print(doc)
            except KeyError as _:
                print(f"Command {self.get_name()} has no subcommand '{arg}'")
            except AttributeError as _:
                pass
        else:
            print(f"Command {self.get_name()} has the following subcommands:")
            for name, method in self._get_methods().items():
                try:
                    doc = getattr(self, method).__doc__
                    if doc:
                        print(f"{name:<15}: {doc}")
                except AttributeError as _:
                    pass

    @final
    def execute(self, arg=None) -> None:
        """ Template method to execute (sub)command """
        if not arg:
            return self.do()

        args = None
        tokens = arg.split()
        subcmd = tokens[0]
        if len(tokens) > 1:
            args = ' '.join(tokens[1:])

        if subcmd == '-':
            return self.do(args)

        func = getattr(self, self._get_methods()[subcmd])
        return func(args)

    def do(self, arg=None) -> None: # pylint: disable=invalid-name
        """ Base do method should be overridden in command subclasses """
        self.do_help(arg)

class Cmdr:
    """ Command base shell class """
    prompt = PROMPT

    def __init__(self, stdin=None, stdout=None) -> None:
        self._commands: Dict[str, Cmd] = {}

        if stdin is not None:
            self.stdin = stdin
        else:
            self.stdin = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout

    @final
    def cmdloop(self, intro=None): # pylint: disable=unused-argument
        """ Template method to show prompt, accept and parse input, and execute commands """
        self.preloop()
        stop = None
        while not stop:
            self.stdout.write(self.prompt)
            self.stdout.flush()
            line = self.stdin.readline()
            if len(line.strip()) == 0:
                line = 'EOF'
            else:
                line = line.rstrip('\r\n')

            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def precmd(self, line: str): # pylint: disable=no-self-use
        ''' Hook method executed once when the cmdloop() method is called '''
        return line

    def postcmd(self, stop, line: str): # pylint: disable=no-self-use, unused-argument
        ''' Hook method executed just after a command has finished '''
        return stop

    def preloop(self):
        '''
        Hook method executed just before the command line is interpreted,
        but after the input prompt is generated and issued.
        '''

    def postloop(self):
        '''
        Hook method executed once when the cmdloop() method is about
        to return
        '''

    @staticmethod
    def _parseline(line: str) -> Tuple[str, str, str]:
        '''
        Parse the line into a command name and a string containing
        the arguments. Returns a tuple containing (cmd, args, line).
        '''
        cmd, arg = None, None
        line = line.strip()

        tokens = line.split()
        if len(tokens) > 0:
            cmd = tokens[0]
        if len(tokens) > 1:
            arg = ' '.join(tokens[1:])

        return cmd, arg, line

    @final
    def onecmd(self, line: str): # pylint: disable=inconsistent-return-statements
        ''' Accept and parse line input '''
        cmd, arg, line = Cmdr._parseline(line)
        if cmd:
            if cmd == 'help':
                self.do_help(arg)
            elif cmd == 'exit':
                return self.do_exit(arg)
            else:
                try:
                    self._commands[cmd].execute(arg)
                except KeyError:
                    self.stdout.write(f"Command {cmd} not found")
                    self.stdout.flush()

    @final
    def register(self, cmd: Cmd) -> None:
        ''' Register a command to the command shell '''
        self._commands[cmd.get_name()] = cmd

    @final
    def unregister(self, cmd: Cmd) -> None:
        ''' Unregister a command from the command shell '''
        self._commands.pop(cmd.get_name())

    def do_help(self, arg=None) -> None: # pylint: disable=unused-argument
        """ List registered commands """
        self.stdout.write("Registered commands:\n")
        for cmd in self._commands:
            self.stdout.write(f"{cmd}\n")
        self.stdout.flush()

    def do_exit(self, arg=None) -> None: # pylint: disable=no-self-use, unused-argument
        ''' Exit the command shell '''
        return True
