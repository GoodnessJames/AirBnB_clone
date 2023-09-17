#!/usr/bin/python3
"""Defines the HBnB console."""
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import cmd
import re


def parse(arg):
    """Splits and returns a list of tokens depending on the format of arg"""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    sqr_brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if sqr_brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            tokens = split(arg[:sqr_brackets.span()[0]])
            token_list = [i.strip(",") for i in tokens]
            token_list.append(sqr_brackets.group())
            return token_list
    else:
        tokens = split(arg[:curly_braces.span()[0]])
        token_list = [i.strip(",") for i in tokens]
        token_list.append(curly_braces.group())
        return token_list


class HBNBCommand(cmd.Cmd):
    """Defines the AirBnB command-line interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default(self, arg):
        """Parse and execute commands provided.
        Maps recognized commands to corresponding methods within the class.
        If the command is not recognized, returns False.
        """
        commands = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arglist = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arglist[1])
            if match is not None:
                command = [arglist[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in commands.keys():
                    call = "{} {}".format(arglist[0], command[1])
                    return commands[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        arglist = parse(arg)
        if len(arglist) == 0:
            print("** class name missing **")
        elif arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arglist[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arglist = parse(arg)
        objdict = storage.all()
        if len(arglist) == 0:
            print("** class name missing **")
        elif arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arglist) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglist[0], arglist[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(arglist[0], arglist[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arglist = parse(arg)
        objdict = storage.all()
        if len(arglist) == 0:
            print("** class name missing **")
        elif arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arglist) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglist[0], arglist[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arglist[0], arglist[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arglist = parse(arg)
        if len(arglist) > 0 and arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objlist = []
            for obj in storage.all().values():
                if len(arglist) > 0 and arglist[0] == obj.__class__.__name__:
                    objlist.append(obj.__str__())
                elif len(arglist) == 0:
                    objlist.append(obj.__str__())
            print(objlist)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arglist = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arglist[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute name> <attribute value>
        Update a class instance of a given id by adding or updating a given
        attribute key/value pair."""
        arglist = parse(arg)
        objdict = storage.all()

        if len(arglist) == 0:
            print("** class name missing **")
            return False
        if arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arglist) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arglist[0], arglist[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arglist) == 2:
            print("** attribute name missing **")
            return False
        if len(arglist) == 3:
            try:
                type(eval(arglist[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arglist) == 4:
            obj = objdict["{}.{}".format(arglist[0], arglist[1])]
            if arglist[2] in obj.__class__.__dict__.keys():
                attr_type = type(obj.__class__.__dict__[arglist[2]])
                obj.__dict__[arglist[2]] = attr_type(arglist[3])
            else:
                obj.__dict__[arglist[2]] = arglist[3]
        elif type(eval(arglist[2])) == dict:
            obj = objdict["{}.{}".format(arglist[0], arglist[1])]
            for k, v in eval(arglist[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    attr_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = attr_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
