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

class HBNBCommand(cmd.Cmd):
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
