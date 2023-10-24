from json import decoder
from typing import List, Dict, Any

default_indent: str = "    "

def indent(amount: int, value: str = default_indent) -> str:
    return value * amount

def varify(name: str, type: str, indent_amount: int = 0) -> str:
    return indent(indent_amount) + F"var {name}: {type}\n"

def structify(struct_name: str, obj: Dict[str, Any], indent_amount: int = 0) -> str:
    objects: Dict[str, Dict[str, Any]] = {}
    literals: Dict[str, str] = {}
    for key, value in obj.items():
        if type(value) is dict:
            objects[key] = value
            literals[key] = key.capitalize()
        elif type(value) is list and all(type(elem) is str for elem in value):
            literals[key] = "[String]"
        elif type(value) is list and all(type(elem) is int for elem in value):
            literals[key] = "[Int]"
        elif type(value) is list and all(type(elem) is float for elem in value):
            literals[key] = "[Double]"
        elif type(value) is str:
            literals[key] = "String"
        elif type(value) is int:
            literals[key] = "Int"
        elif type(value) is float:
            literals[key] = "Double"
        else:
            raise Exception(f"failed: { type(value) }")
    vars: List[str] = [varify(key, value, indent_amount+1) for key, value in literals.items()]
    structs: List[str] = [structify(key.capitalize(), value, indent_amount+1) for key, value in objects.items()]
    struct_init: str = indent(indent_amount) + "struct " + str(struct_name) + ": Codable {\n"
    struct_end: str = indent(indent_amount) + "}\n\n"
    return struct_init + "".join(structs + vars) + struct_end


with open("input.json") as f:
    dec: decoder.JSONDecoder = decoder.JSONDecoder()
    json_file: dict = dec.decode(f.read())

print(structify("Response", json_file))