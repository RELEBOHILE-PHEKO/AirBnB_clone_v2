import shlex
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

        for param in args[1:]:
            if "=" not in param:
                continue

            key, value = param.split("=", 1)

            # Processing value
            if value.startswith('"') and value.endswith('"'):
                # Remove surrounding quotes and replace underscores with spaces
                value = value[1:-1].replace("_", " ")
                value = value.replace('\\"', '"')  # Escape quotes within the string
            elif '.' in value:
                # Float
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                # Integer
                try:
                    value = int(value)
                except ValueError:
                    continue

            # Setting attribute
            setattr(new_instance, key, value)

        # Save the instance
        new_instance.save()
        print(new_instance.id)

    def do_all(self, arg):
        """Prints all string representations of all instances"""
        args = arg.split()
        if len(args) == 0:
            obj_list = storage.all()
        elif args[0] in HBNBCommand.classes:
            obj_list = storage.all(HBNBCommand.classes[args[0]])
        else:
            print("** class doesn't exist **")
            return

        print([str(obj) for obj in obj_list.values()])

# To be integrated with your existing command loop and storage system.
