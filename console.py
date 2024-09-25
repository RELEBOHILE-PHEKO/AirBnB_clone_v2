#!/usr/bin/python3
"""This module contains the entry point of the command interpreter."""import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Command interpreter"""
    prompt = "(hbnb) "

    # Map of valid classes
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }

    def do_create(self, arg):
        """Creates a new instance of a class, with dynamic parameters"""
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

        # Parsing key=value arguments
        for param in args[1:]:
            if "=" not in param:
                continue

            key, value = param.split("=", 1)

            # Processing value
            if value.startswith('"') and value.endswith('"'):
                # String type: Remove surrounding quotes, replace underscores with spaces
                value = value[1:-1].replace("_", " ")
                value = value.replace('\\"', '"')  # Handle escaped quotes inside strings
            elif '.' in value:
                # Float type
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                # Integer type
                try:
                    value = int(value)
                except ValueError:
                    continue

            # Dynamically set attributes for the new instance
            if hasattr(new_instance, key):
                setattr(new_instance, key, value)

        # Save the instance and print the ID
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) < 2:
            print("** class name or instance ID missing **")
            return

        class_name, instance_id = args[0], args[1]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        all_objs = storage.all()
        obj = all_objs.get(key)

        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all instances, or all instances of a specific class"""
        args = shlex.split(arg)
        all_objs = storage.all()

        if len(args) == 0:
            # Print all objects
            print([str(obj) for obj in all_objs.values()])
        elif args[0] in HBNBCommand.classes:
            # Print objects of a specific class
            print([str(obj) for key, obj in all_objs.items() if key.startswith(args[0])])
        else:
            print("** class doesn't exist **")

# To be integrated with your existing command loop and storage system.

