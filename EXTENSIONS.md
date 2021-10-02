# Kinquett Extensions Documentation 1.3 (dev update 12)

Kinquett extensions are stored as directories with python files. 

## `main.py`

When `import` is called on an extension, the `main.py` file in the directory is called. The `main.py` file should be a direct child of the extension directory. The `main.py` file should be built off of the following template, which contains definitions and dictionaries of all the operations and inline operations of the extension.
```python
def expect_type(value, val_type):
    if not ((bool in val_type) and (value == 0 or value == 1)):
        if not ((None in val_type) and (value is None)):
            if not type(value) in val_type:
                raise ValueError(f"Expected {val_type}")
            else:
                return type(value)
        else:
            return None
    else:
        return bool

def set_line(line_set, line):
    line = line_set - 1

def str_to_list(string):
    ord_list = []
    for i in string:
        ord_list.append(ord(i))
    return ord_list
    
def list_to_str(string_list):
    chr_string = ""
    for i in string_list:
        chr_string += chr(i)
    return string
    
class Operation:
    def example_op(params, globals):
        print("called op")
        
class Inop:
    def example_inop(params, globals):
        print("called inop")


OPERATIONS = {
    "example": Operation.example_op,
}
INOPS = {
    "example": Inop.example_inop,
}
```
When an operation / inline operation is called it searches the `OPERATIONS` / `INOPS` dictionaries for the appropiate function object (typically in the `Operation` / `Inop` classes) with the name as the key and executes the function with the parameters passed as `params` and the global variables as `globals`. The value passed through `globals` is typically as follows:
```python
{
    "mem": mem,
    "line": line,
}
``` 
`mem` and `line` are the memory list and current line global variables in the main Kinquett program respectively.

### `expect_type`

Format: `expect_type(value, val_type)`

Raises an error when the value type isn't in the list of types. A value is considered a bool when it is equal to `0` or `1`. Returns the class of the type of the value, except for `None`, which returns `None` rather than `<class 'NoneType'>`. Special values in Kinquett are represented as strings.

### `set_line`

Format: `set_line(line_set, line)`

Sets the line to the line specified by `line_set`, accounting for the line increment by automatic line incrementing when reading code. Set `line` to the `"line"` value in the `globals` dictionary passed when an operation or inline operation is called.

### `str_to_list` and `list_to_str`

Format: `str_to_list(string)`

Format: `list_to_str(list)`

Turns a string into a list with each letter as the unicode pointer and vice versa.

### `Operation` and `Inop` 

Classes containing operations and inline operations respectively.

### `OPERATIONS` and `INOPS`

Dictionaries containing operation / inline operation strings as keys and appropiate function objects as values respectively.
