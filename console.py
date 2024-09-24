#!/usr/bin/python3
"""This module contains the entry point of the command interpreter."""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex

class HBNBCommand(cmd.Cmd):
<<<<<<< HEAD
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Executes before each command"""
        return cmd.Cmd.precmd(self, line)

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = shlex.split(arg)
        
        if len(args) == 0:
            print("** class name missing **")
            return
        
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Create an instance of the class
        new_instance = HBNBCommand.classes[class_name]()

        # Process the parameters
        for param in args[1:]:
            key, value = self.parse_parameter(param)
            if key and value:
                setattr(new_instance, key, value)

        # Save the new instance
        new_instance.save()
        print(new_instance.id)

    def parse_parameter(self, param):
        """Parse a single key=value parameter and return key, value"""
        # Check if param follows key=value format
        if '=' not in param:
            return None, None
        
        key, value = param.split('=', 1)

        # String: if it starts with a double quote, process as a string
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('_', ' ').replace('\\"', '"')

        # Float: if it contains a dot, convert to float
        elif '.' in value:
            try:
                value = float(value)
            except ValueError:
                return None, None

        # Integer: if it's numeric, convert to int
        elif value.isdigit():
            try:
                value = int(value)
            except ValueError:
                return None, None

        else:
            return None, None

        return key, value

    # Rest of the methods, e.g., do_show, do_destroy, etc., remain unchanged

=======
    """Command interpreter class"""

    prompt = '(hbnb) '
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        
        new_instance = HBNBCommand.__classes[args[0]]()
        
        for param in args[1:]:
            if '=' not in param:
                continue
            key, value = param.split('=', 1)
            
            # Process the value based on its type
            if value.startswith('"') and value.endswith('"'):
                # String value
                value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            elif '.' in value:
                # Float value
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                # Integer value
                try:
                    value = int(value)
                except ValueError:
                    continue
            
            # Set the attribute
            setattr(new_instance, key, value)
        
        new_instance.save()
        print(new_instance.id)

    # ... (other methods remain unchanged)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
>>>>>>> 3d1c62397da9cec2fcada370ef70024952bac69e
