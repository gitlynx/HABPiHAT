#!/usr/bin/env python
import typing
import pdb


class CommandMenu(object):
    """
        Base Class to process commands
    """
    def __init__(self, menuname: str):
        """
            Class Constructor
        """
        self.name = menuname
        self.commands = {}

    def action(self, cmdline) -> typing.Tuple[bool, str]:
        """
            action
                Searches if command (first element of input string) is in list of sub commands
                if found: Call associated function with remainder of input string
        """
        command_remainder = cmdline.split(None, 1)
        if len(command_remainder) < 1:
            return "No command line given"

        command = command_remainder[0]
        if len(command_remainder) < 2:
            remainder = ""
        else:
            remainder = command_remainder[1]
        if command in self.commands.keys():
            if self.commands[command] is not None:
                ret = self.commands[command](remainder)
            else:
                return "No action linked to command"
        else:
            return "Command not found"

    def identity(self):
        return self.name, self.action

    def add(self, command: tuple) -> bool:
        """
            'add'
            Add the command given as a tuple to the command menu
            tuple element 1: string with command name
            tuple element 2: function object. Function with 1 parameter (remainder of command line)

        """
        if not isinstance(command, tuple):
            return False
        if len(command) is not 2:
            return False
        self.commands[command[0]] = command[1]
        return True

    def remove(self, command: str) -> bool:
        if command in self.commands:
            del self.commands[command]
            return True
        else:
            return False

    def listSubCommand(self):
        for t in self.commands.items():
            print("Command: {}; implemented: {}".format(t[0], t[1] is not None))


class Command(object):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def identity(self):
        return self.name, self.action


class cmd1(Command):
    def __init__(self, cmdname):
        Command.__init__(self, cmdname, self.action)
        print("--- cmd1 ---")

    def action(self, remainder):
        print("--- cmd1 action ---")


class sub1(Command):
    def __init__(self, cmdname):
        Command.__init__(self, cmdname, self.action)
        print("--- sub1 ---")

    def action(self, remainder):
        print("--- {} ---", remainder)


def fn1(remainder):
    print("++++ **** ++++")

if __name__ == "__main__":
    c1 = cmd1("modem")
    c2 = cmd1("cmd1")

    s1 = sub1("sub1")
    s2 = sub1("sub2")

    rootmenu = CommandMenu("root")
    rootmenu.add(c1.identity())
    rootmenu.add(c2.identity())

    submenu = CommandMenu("sub")
    submenu.add(s1.identity())
    submenu.add(s2.identity())
    submenu.add(("fn1", fn1))

    rootmenu.add(submenu.identity())

    print("-- 1 ----------------------------------------------")
    rootmenu.listSubCommand()
    print("-- 2 ----------------------------------------------")
    rootmenu.action("cmd1 param1 param2")
    print("-- 3 ----------------------------------------------")
    rootmenu.action("sub sub1")
    print("-- 4 ----------------------------------------------")
    rootmenu.action("sub fn1")
    print("-- 5 ----------------------------------------------")
    pdb.set_trace()
    submenu.remove("fn1")
    rootmenu.action("sub fn1")
