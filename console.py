#!/usr/bin/python3
"""This module contains the entry point of the command interpreter."""import shleximport shlex
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    # Other methods...

    def do_create(self, arg):
        """Create a new instance of a class and save it to the JSON file."""
        args = shlex.split(arg)  # Splitting the input command

        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]

        # Validate class name
        if class_name not in globals():
            print("** class doesn't exist **")
            return

        # Get the class object from globals
        new_instance = globals()[class_name]()

        # Iterate over additional arguments (params)
        for param in args[1:]:
            if "=" not in param:
                continue  # Skip invalid param
            key, value = param.split("=", 1)

            # Handle strings: remove quotes, handle escapes and replace underscores with spaces
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace("_", " ").replace('\\"', '"')

            # Handle integers
            elif value.isdigit():
                value = int(value)

            # Handle floats
            else:
                try:
                    value = float(value)
                except ValueError:
                    continue  # Skip invalid float

            # Set the attribute on the instance
            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

# Other methods...

if __name__ == '__main__':
    HBNBCommand().cmdloop()


