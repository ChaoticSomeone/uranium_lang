# Uranium Lang

**This is an open-source project, feel free to contribute**

# Uranium Lang - Features & Syntax

## Variables

### Primitive Datatypes:
- int
- float
- string
- bool

### Decleration and Assignment
```
// decleration (doesn't work at the moment)
name: datatype

// assignment
name: datatype = value
```

Example:
```
number: int = 0
```

## The main function
```
func main() -> int {
	return 0
}
```

## Functions
```
func name(param_name: param_type, ...) -> return_type {
	// your code goes here
}
```

Example:
```
func add(a: int, b: int) -> int {
	return a + b
}
```

**Please Note: Functions cannot be called yet (I might have fixed this already)**

## Comments
As of right now Uranium Lang only has support for single-line comments, multi-line comments will be added in the future.
```
// This is a single-line comment
```

## If, Else if, Else
```
if condition1 {
	...
} else if condition2 {
	...
} else {
	...
}
```

Example:
```
num: int = 10
if num < 5 {
	// do something here
} else if num > 5 {
	// do something else here
} else {
	// do something here too
}
```

## While loops
```
while condition {
	...
}
```

Example:
```
num: int = 0
while i < 10 {
	i = i +1
}
```

## For loops
Uranium Lang will support different types of for-loops, however only the
classic iterative for-loop is implemented right now.
```
for name: datatype = value, condition, de/- incrementation value {
	...
}
```

Example:
```
for i: int = 0, i < 10, 1 {
	// this achieves the same as the above while loop example
}
```


# Uranium Lang - How does it work

The Uranium Compiler "runs through" your source code and tokenizes it. The resulting tokens are then
rearranged and resstructured so that they can be tarnslated to C++ more easily.
Yes, Uranium Lang is not directly compiled to machine code, it gets compiled into C++ and
relies on an external C++ Compiler to do the rest of the compilation.
