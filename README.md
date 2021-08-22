# Kinquett Documentation 1.0 (dev update 8)

Kinquett is an esoteric programming language based on assembly syntax programmed in everyone's favorite language, *Python*

## Why learn Kinquett?

Don't.

## What does Kinquett look like?

Here are some examples:

```
alloc 2 0
set 0 (load 2 1 (input #84,121,112,101,119,114,105,116,101,58,32))
set 1 0
if (compare $1 :< $0) 4 7
print $#2,(math #2,$1,:+)
set 1 (math #1,$1,:+)
goto 3
print $#2,(math #2,$0,:+)
```
```
alloc 3 0
set 2 (load 3 1 (input #))
set 1 (math #$2,3,:+)
set 0 0
alloc 1 allocated
set $1 35
if (compare $0 :< $2) 7 12
set null (load allocated 1 (str $(math #$0,3,:+)) 0)
alloc 1 allocated
set (math #allocated,1,:-) 44
set 0 (math #$0,1,:+)
goto 6
print $#$1,(math #allocated,1,:-)
```
### What do they do?

dunno.
## Kinquett miscellaneous information

- Kinquett memory is handled as an ordered array, with addresses for each cell of memory.
- You have to allocate memory before using it.
- Memory cells can only hold floats and integers.
- Kinquett is case-sensitive.
- Kinquett's line index starts at `0`.
- Booleans in Kinquett are represented as `0` and `1`.
- Strings in Kinquett are represented as lists with unicode codes.

## Kinquett syntax

***The code in this section is not valid code. It is only meant to demonstrate the syntax of Kinquett.***

The Kinquett syntax is rather simplistic, featuring **Operations** and **Inline Operations** (referred to internally as `ops` and `inops`)

### Operations

Operations are always referenced first in a line. Parameters follow an operation afterward with a space. Parameters are separated with a space as well.

*e.g.*
```
operation param1 param2 param3
```

### Inline operations

Inline operations return values and hence cannot be treated like operations. They are used in the parameters of an operation. Inline operations with parameters have to be enclosed in parameters. 

*e.g.*
```
operation inop (inop param2-1 param2-2)
```

### Values

Static values and memory values can also be referenced in both inline operation and operation parameters. It is optional for static values to be prefixed with a `&` but mandatory for memory values to be prefixed with a `$`. `:` specifies a special value. Any value can be passed as a special value, except whitespace characters. It is used for certain inline operations and operations.

*e.g.*
```
operation &7 7 $3
```

### Lists and ranges

There can also be lists and memory ranges. Static lists / ranges can be defined with a `#` after the initial identifier (`&` or `$` or nothing). Lists / ranges are separated with a `,`. Lists are specified with `&` and are defined by specifying each element of the list. Embedded lists (lists inside lists) have to be enclosed in parentheses. Ranges return the elements between 2 pointers, and are specified with a `$`. The first item is the start pointer and the last item is the end pointer. It is optional to have a trailing comma after the last element / pointer of a list / range. 

*e.g.*
```
operation #5,8,$3,(#4,5), $#0,3,
```

### Null

Null specifies... Null. What did you think it did?

*e.g.*
```
operation null
```

### These can be combined to replicate any computational task.

*e.g.*
```
operation $3 (inop #5,2,$6 $#2,7)
```

## Kinquett functions

### Operations 
- `print` *`{value : int,float,list,null}`*: What do you think it does? It prints a value. If the value is a `list` it will treat it as a string and print the unicode characters for each element, else it will just print the value.
- `alloc`  *`{amount : int}` `{start : int}`*: Allocates the specified `amount` of memory at the specified `start` pointer. The index of the first allocated cell will be the `start` pointer value.
- `free` *`{amount : int}` `start : int}`*: Frees the specified `amount` of memory at the specified `start` pointer. 
- `set` *`{pointer : int,null}` `{value : int,float,null}`*: Sets the specified `pointer` to the specified value. If the pointer is `null` then it does nothing. 
- `goto` *`{line : int}`*: Goes to the specific line. 
- `if` *`{condition : bool}` `{true : int}` `{false : int}`*: If the specified `condition` is `true` (represented as `1`), it goes to the specified `true` parameter line, else it goes to the specified `false` parameter line.

### Inline operations

- `math` *`{instructions : list}`* returns: `{result : int,float}`: An implementation of Reverse Polish Notation. The list can contain an arbitrary amount of instructions, and each element can either be a `float`, `int` or `special`. Mathematical operations can be specified by a `special` value and include `+`, `-`, `*`, `/`, `^`, and `%`. 
- `compare` *`{value_1 : int,float,list,bool,null}` `{compare : special}` `{value_2 : int,float,list,bool,null}`* returns: `{result : bool}`: Compares `value_1` with `value_2` by the specified `compare`. Comparison operators for the `compare` parameter include `<`, `<=`, `==`, `!=`, `>=`, and `>`.
- `and` *`{value_1 : bool}` `{value_2 : bool}` returns: `{result : bool}`: Performs the `and` comparison between 2 values. 
- `or` *`{value_1 : bool}` `{value_2 : bool}` returns: `{result : bool}`: Performs the `or` comparison between 2 values. 
- `not` *`{value : bool}` returns: `{result : bool}`: Inverts a boolean.
- `int` *`{value : int,float,list}`* returns: `{result : int}`: Converts a value to an integer.
- `float` *`{value : int,float,list}`* returns: `{result : float}`: Converts a value to a float.
- `str` *`{value : int,float,list,bool,null}`* returns: `{result : list}`: Converts a value to a string (represented as a list).
- `allocated` returns: `{allocated : int}`: returns the amount of memory allocated.
- `input` *`{prompt : list}`* returns: `{input : list}`: Prompts the user with a specified `prompt` interpreted as a string and returns the input as a string. 
- `load` *`{start : int}` `{overwrite : bool}` `{value : list}`* returns: `{length : int}`: Loads a `list`, specified as the `value` parameter, into memory at the specified `start` pointer. If `overwrite` is true, it will overwrite existing values in memory as it loads the list into memory, else it will allocate memory as it loads the list. This function will allocate new memory if it reaches the end of the allocated memory, regardless of the `overwrite` setting. It returns the length of the list afterward.
- `length` *`{list : list}`*: returns the length of a specified `list`.
- `index` *`{list : list}` `{index : int}`*: returns the value of a specified `index` in the specified `list`


## Oh- and another thing

I have spent a month developing this and I have sacrificed my mental health in the creation of this messy, unreadable code. If literally anyone is reading this, thank you for making my suffering worth it.

##### Code and documentation written by MusicOnStereo/MusicOnMono
