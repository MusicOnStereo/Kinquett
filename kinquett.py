mem = []
line = 0

# I hate this function.


def split_level(line, split_char):
    parentheses = 0
    line_split = []
    parentheses_visibility = []
    element = ""
    for i in line:
        if i == "(":
            in_list = element.startswith(("&#", "#", "$#"))
            if parentheses > 0 or in_list:
                element = element + i
                parentheses_visibility.append(True)
            else:
                parentheses_visibility.append(False)
            parentheses += 1
        elif i == ")":
            parentheses -= 1
            if parentheses_visibility.pop():
                element = element + i
        elif i == split_char and parentheses == 0:
            line_split.append(element)
            element = ""
        else:
            element = element + i
    if element != "":
        line_split.append(element)
    return line_split


# At least this function hasn't broken ever.
def process_operation(line):
    line_split = split_level(line, " ")
    line_processed = []
    for i in range(1, len(line_split)):
        line_processed.append(process_value(line_split[i]))
    OPERATIONS[line_split[0]](line_processed)


# Why does it always have to be ***this*** function?? THIS ONE. This
# function has caused me much agony and it is ***unbearingly*** difficult
# to debug at times. I hate this stupid function and the nature of its
# existence.  Why, why, why?? I see the function's name pop up in the
# traceback after an error and I get infuriated.
def process_value(value):
    if not value.split(" ")[0] in INOPS:
        value_type = value[0]
        value_val = value[1:]
        STATIC_CHARACTERS = [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "&", "#"
        ]
        if value_type in STATIC_CHARACTERS:
            if value_type != "&":
                value_val = value_type + value_val
            if value_val[0] == "#":
                value_val = split_level(value_val[1:], ",")
                value_processed = []
                for i in value_val:
                    value_processed.append(process_value(i))
                return value_processed
            else:
                if "." in value_val:
                    return float(value_val)
                else:
                    return int(value_val)
        elif value_type == "$":
            if value_val[0] == "#":
                value_val = split_level(value_val[1:], ",")
                value_processed = []
                for i in range(0, 2):
                    value_processed.append(int(process_value(value_val[i])))
                return mem[value_processed[0]: value_processed[1]]
            else:
                return mem[int(process_value(value_val))]
        elif value_type == ":":
            return value_val
        elif value_type + value_val == "null":
            return None
        else:
            raise ValueError(f"Invalid inop / identifier")
    else:
        value_split = split_level(value, " ")
        value_processed = []
        for i in range(1, len(value_split)):
            value_processed.append(process_value(value_split[i]))
        return INOPS[value_split[0]](value_processed)


# The most useful function.
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


# Because I was too lazy to just do a bit of subtraction, lol
def set_line(set):
    global line

    line = set - 1

# I don't actually know what classes do but I'm just using them to
# organize stuff


class Operation:
    def prt(params):
        param_type = expect_type(params[0], [int, float, None, list])
        if param_type is list:
            string = ""
            for i in params[0]:
                string = string + chr(i)
            print(string)
        elif param_type is None:
            print("null")
        else:
            print(params[0])

    def alloc(params):
        expect_type(params[0], [int])
        expect_type(params[1], [int])
        for i in range(0, params[0]):
            mem.insert(params[1], None)

    def set(params):
        param_type = expect_type(params[0], [int, None])
        expect_type(params[1], [int, float, None])
        if param_type is not None:
            mem[params[0]] = params[1]

    def free(params):
        param_type = expect_type(params[0], [int])
        param_type = expect_type(params[1], [int])
        del mem[params[0]: params[1] + params[0]]

    def goto(params):
        expect_type(params[0], [int])
        set_line(params[0])

    def conditional(params):
        expect_type(params[0], [bool])
        expect_type(params[1], [int])
        expect_type(params[2], [int])
        if params[0] == 1:
            set_line(params[1])
        else:
            set_line(params[2])


class Inop:
    # Yandere moment
    def math(params):
        expect_type(params[0], [list])
        stack = []
        expression = params[0]
        for i in expression:
            if i == "+":
                curr = stack.pop(-1)
                curr = stack.pop(-1) + curr
                stack.append(curr)
            elif i == "-":
                curr = stack.pop(-1)
                curr = stack.pop(-1) - curr
                stack.append(curr)
            elif i == "*":
                curr = stack.pop(-1)
                curr = stack.pop(-1) * curr
                stack.append(curr)
            elif i == "/":
                curr = stack.pop(-1)
                curr = stack.pop(-1) / curr
                stack.append(curr)
            elif i == "^":
                curr = stack.pop(-1)
                curr = stack.pop(-1) ** curr
                stack.append(curr)
            elif i == "%":
                curr = stack.pop(-1)
                curr = stack.pop(-1) % curr
                stack.append(curr)
            else:
                expect_type(i, [int, float])
                stack.append(i)
        return stack[0]

    def compare(params):
        expect_type(params[0], [int, float, list, None, bool])
        expect_type(params[1], [str])
        expect_type(params[2], [int, float, list, None, bool])
        if params[1] == "<":
            return int(params[0] < params[2])
        elif params[1] == "<=":
            return int(params[0] <= params[2])
        elif params[1] == "==":
            return int(params[0] == params[2])
        elif params[1] == "!=":
            return int(params[0] != params[2])
        elif params[1] == ">":
            return int(params[0] > params[2])
        elif params[1] == ">=":
            return int(params[0] >= params[2])

    # I don't know how I feel about the logic functions being their own
    # seperate inops, especially since the compare function exists...
    class Logic:
        def logic_and(params):
            expect_type(params[0], [bool])
            expect_type(params[1], [bool])
            return int(bool(params[0]) and bool(params[1]))

        def logic_or(params):
            expect_type(params[0], [bool])
            expect_type(params[1], [bool])
            return int(bool(params[0]) or bool(params[1]))

        def logic_not(params):
            expect_type(params[0], [bool])
            return int(not bool(params[0]))

    def text_input(params):
        param_type = expect_type(params[0], [int, list])
        prompt = ""
        if param_type is list:
            for i in params[0]:
                expect_type(i, [int])
                prompt = prompt + chr(i)
        else:
            prompt = chr(params[0])
        input_list = []
        for i in list(input(prompt)):
            input_list.append(ord(i))
        return input_list

    # This inop is useless.
    def get(params):
        expect_type(params[0], [int])
        return mem[params[0]]

    class Conversions:
        def convert_int(params):
            string = ""
            expect_type(params[0], [list, float, int])
            for i in params[0]:
                expect_type(i, [int])
                string = string + chr(i)
            return int(string)

        def convert_str(params):
            def convert(value):
                param_type = expect_type(value, [int, float, bool, None, list])
                if param_type is None:
                    return [110, 117, 108, 108]
                elif param_type is list:
                    string = [35]
                    for i in value:
                        if isinstance(i, list):
                            string += [40] + convert(i) + [41, 44]
                        else:
                            string += convert(i) + [44]
                    if string == [35]:
                        return string
                    else:
                        return string[0:-1]

                else:
                    string = str(value)
                    string_list = []
                    for i in string:
                        string_list.append(ord(i))
                    return string_list
            return convert(params[0])

        def convert_float(params):
            string = ""
            expect_type(params[0], [list, float, int])
            for i in params[0]:
                expect_type(i, [int])
                string = string + chr(i)
            return float(string)

    def allocated(params):
        return len(mem)

    # This function has been revised over countless times, it used to be an op
    def load(params):
        expect_type(params[0], [int])
        expect_type(params[1], [bool])
        expect_type(params[2], [list])
        length = len(params[2])
        for i, v in enumerate(params[2]):
            expect_type(i, [int])
            if params[0] + i > len(mem) or bool(params[1]):
                mem.insert(params[0] + i, v)
            else:
                mem[i] = v
        return length

    # The following two functions didn't exist until much later in the
    # development
    def length(params):
        expect_type(params[0], [list])
        return len(params[0])

    def index(params):
        expect_type(params[0], [list])
        expect_type(params[1], [int])
        return params[0][params[1]]
    
    def cat(params):
        expect_type(params[0], [list])
        expect_type(params[1], [list])
        return params[0] + params[1]


OPERATIONS = {
    "print": Operation.prt,
    "alloc": Operation.alloc,
    "set": Operation.set,
    "goto": Operation.goto,
    "if": Operation.conditional,
    "free": Operation.free
}
INOPS = {
    "math": Inop.math,
    "compare": Inop.compare,
    "and": Inop.Logic.logic_and,
    "or": Inop.Logic.logic_or,
    "not": Inop.Logic.logic_not,
    "input": Inop.text_input,
    "get": Inop.get,
    "load": Inop.load,
    "int": Inop.Conversions.convert_int,
    "float": Inop.Conversions.convert_float,
    "str": Inop.Conversions.convert_str,
    "allocated": Inop.allocated,
    "length": Inop.length,
    "index": Inop.index,
    "cat": Inop.cat,
}


def main():
    program = []

    def init():
        global mem
        global line
        nonlocal program

        mem = []
        line = 0
        program = []

    def multi_line_input(prompt):
        single_line = None
        multi_line = []
        print(prompt)
        while True:
            single_line = input()
            if single_line != "":
                multi_line.append(single_line)
            else:
                return multi_line

    while True:
        global line

        init()
        program = multi_line_input("Input program")
        while line < len(program):
            process_operation(program[line])
            line += 1


if __name__ == "__main__":
    main()
