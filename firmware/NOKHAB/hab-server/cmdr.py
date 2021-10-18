import string, sys
from typing import Dict, List, Tuple, final

PROMPT = '(Cmdr) '

class Cmd:

    def __init__(self, command: str) -> None:
        self._command = command

    def get_name(self) -> str:
        return self._command

    def _get_methods(self) -> List:
        return {method.strip('do_'): method for method in dir(self)
                if callable(getattr(self, method)) and method.startswith('do_')}

    @final
    def do_help(self, arg=None) -> None:
        """ this is help doc """ 
        if arg:
            try:
                doc = getattr(self, self._get_methods()[arg]).__doc__
                if doc:
                    print(doc)
            except KeyError as e:
                print(f"Command {self.get_name()} has no subcommand '{arg}'")
            except AttributeError as e:
                pass
        else:
            print(f"Command {self.get_name()} has the following subcommands:")
            for name, method in self._get_methods().items():
                try:
                    doc = getattr(self, method).__doc__
                    if doc:
                        print(f"{name:<15}: {doc}")
                except AttributeError as e:
                    pass

    @final
    def execute(self, arg=None) -> None:
        if not arg:
            return self.do()
        else:
            args = None
            tokens = arg.split()
            subcmd = tokens[0]
            if len(tokens) > 1:
                args = ' '.join(tokens[1:])

            if subcmd == '-':
                return self.do(args)
            else:
                func = getattr(self, self._get_methods()[subcmd])
                return func(args)

    def do(self, arg=None) -> None:
        self.do_help(arg)

class Cmdr:
    prompt = PROMPT

    def __init__(self, stdin=None, stdout=None) -> None:
        self._commands: Dict[str, Cmd] = dict()
        
        if stdin is not None:
            self.stdin = stdin
        else:
            self.stdin = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout
    
    @final
    def cmdloop(self, intro=None):
        self.preloop()
        stop = None
        while not stop:
            self.stdout.write(self.prompt)
            self.stdout.flush()
            line = self.stdin.readline()
            if not len(line):
                line = 'EOF'
            else:
                line = line.rstrip('\r\n')
            
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def precmd(self, line: str):
        return line

    def postcmd(self, stop, line: str):
        return stop

    def preloop(self):
        pass

    def postloop(self):
        pass

    def _parseline(self, line: str) -> Tuple[str, str, str]:
        cmd, arg = None, None
        line = line.strip()
        
        tokens = line.split()
        if len(tokens) > 0:
            cmd = tokens[0]
        if len(tokens) > 1:
            arg = ' '.join(tokens[1:])

        return cmd, arg, line

    @final
    def onecmd(self, line: str):
        cmd, arg, line = self._parseline(line)
        if cmd:
            if cmd == 'help':
                self.do_help(arg)
            elif cmd == 'exit':
                self.do_exit(arg)
            else:
                try:
                    self._commands[cmd].execute(arg)
                except KeyError:
                    self.stdout.write(f"Command {cmd} not found")
                    self.stdout.flush()

    @final
    def register(self, cmd: Cmd) -> None:
        self._commands[cmd.get_name()] = cmd
    
    @final
    def unregister(self, cmd: Cmd) -> None:
        self._commands.pop(cmd.get_name())

    @final
    def unregister(self, cmd: str) -> None:
        self._commands.pop(cmd)

    def do_help(self, arg=None) -> None:
        self.stdout.write("Registered commands:\n")
        for cmd in self._commands.keys():
            self.stdout.write(f"{cmd}\n")
        self.stdout.flush()

    def do_exit(self, arg=None) -> None:
        pass
