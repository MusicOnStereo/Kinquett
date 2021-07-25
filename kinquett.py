mem = []
ascii = {i: chr(i) for i in range(128)}
line = 0
program = []

class init:
  def initMain():
    global mem
    global ascii
    mem = []
    ascii = {i: chr(i) for i in range(128)}
    line = 0
  
  def multiLineInput(prompt):
    singleLine = None
    multiLine = []
    print(prompt)
    while True:
      singleLine = input()
      if singleLine != "":
        multiLine.append(singleLine)
      else:
        return multiLine
    

def splitlevel(line, splitchar):
  linelist = list(line)
  parentheses = 0
  linesplit = []
  element = ""
  for i in linelist:
    if i == "(":
      parentheses += 1
    elif i == ")":
      parentheses -= 1
    elif i == splitchar and parentheses == 0:
      linesplit.append(element)
      element = ""
    else:
        element = element + i
  linesplit.append(element)
  return linesplit
                
def processoperation(line):
  linesplit = splitlevel(line, " ")
  lineprocessed = []
  for i in range(1, len(linesplit)):
    lineprocessed.append(processvalue(linesplit[i]))
  operations[linesplit[0]](lineprocessed)
            
def processvalue(value):
  if not value.split(" ")[0] in inops:
    valuetype = value[0]
    valueval = value[1:]
    if valuetype == "&":
      if valueval[0] == "#":
        valueval = splitlevel(valueval[1:], ",")
        valueprocessed = []
        for i in valueval:
          valueprocessed.append(int(processvalue(i)))
        return valueprocessed
      else:
        return int(valueval)
    elif valuetype == "$":
      if valueval[0] == 0:
        valueval = splitlevel(valueval[1:], ",")
        valueprocessed = []
        for i in range(0, 2):
          valueprocessed.append(int(processvalue(valueval[i])))
        return mem[valueprocessed[0]: valueprocessed[1]]
      else:
        return mem[int(valueval)]
    elif valuetype == ":":
      return valueval
    else:
      raise ValueError(f"Invalid inop / identifier: {line}")
  else:
    valuesplit = splitlevel(value, " ")
    valueprocessed = []
    for i in range(1, len(valuesplit)):
      valueprocessed.append(processvalue(valuesplit[i]))
    return inops[valuesplit[0]](valueprocessed)
    
def expecttype(value, valtype):
  if not ((bool in valtype) and (value == 0 or value == 1)):
    if not type(value) in valtype:
      raise ValueError(f"Expected {valtype}: {line}")
    else:
      return type(value)
  else:
    return bool

def setline(set):
  global line
  line = set - 1
  
class operation:
  def prt(params):
    expecttype(params[1], [bool])
    if params[1] == 0:
      expecttype(params[0], [int])
      print(params[0])
    else:
      paramtype = expecttype(params[0], [int, list])
      if paramtype is int:
        print(ascii[params[0]])
      else:
        string = ""
        for i in params[0]:
          string = string + ascii[i]
        print(string)
        
  def alloc(params):
    global mem
    expecttype(params[0], [int])
    for i in range(0, params[0]):
      mem.append(0)
  
  def set(params):
    global mem
    expecttype(params[0], [int])
    expecttype(params[1], [int])
    mem[params[0]] = params[1]
    
  def goto(params):
    expecttype(params[0], [int])
    setline(params[0])
    
  def conditional(params):
    expecttype(params[0], [int])
    expecttype(params[1], [int])
    expecttype(params[2], [int])
    if params[0] == 1:
      setline(params[1])
    elif params[0] == 0:
      setline(params[2])
    else:
      raise ValueError("Out of range")


class inop:
  def math(params):
    stack = []
    for i in params:
      if i == "+":
        curr = stack.pop(-1)
        curr = curr + stack.pop(-1)
        stack.append(curr)
      elif i == "-":
        curr = stack.pop(-1)
        curr = curr - stack.pop(-1)
        stack.append(curr)
      elif i == "*":
        curr = stack.pop(-1)
        curr = curr * stack.pop(-1)
        stack.append(curr)
      elif i == "/":
        curr = stack.pop(-1)
        curr = curr / stack.pop(-1)
        stack.append(curr)
      elif i == "^":
        curr = stack.pop(-1)
        curr = curr ** stack.pop(-1)
        stack.append(curr)
      elif i == "%":
        curr = stack.pop(-1)
        curr = curr % stack.pop(-1)
        stack.append(curr)
      else:
        expecttype(i, [int])
        stack.append(i)
    return stack[0]
    
  def compare(params):
    expecttype(params[0], [int])
    expecttype(params[1], [str])
    expecttype(params[2], [int])
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
    
  class logic:
    def logicand(params):
      expecttype(params[0], [bool])
      expecttype(params[1], [bool])
      return int(bool(params[0]) and bool(params[1]))
      
    def logicor(params):
      expecttype(params[0], [bool])
      expecttype(params[1], [bool])
      return int(bool(params[0]) or bool(params[1]))
      
    def logicnot(params):
      expecttype(params[0], [bool])
      return int(not bool(params[0]))

operations = {
"print": operation.prt,
"alloc": operation.alloc,
"set": operation.set,
"goto": operation.goto,
"if": operation.conditional,

}
inops = {
"math": inop.math,
"compare": inop.compare,
"and": inop.logic.logicand,
"or": inop.logic.logicor,
"not": inop.logic.logicnot,
}

program = init.multiLineInput("Input program")
while line < len(program):
  processoperation(program[line])
  line += 1