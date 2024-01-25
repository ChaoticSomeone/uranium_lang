# Uranium Lang


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

**Please Note: Functions cannot be called yet**

## Comments
As of right now Uranium Lang only has support for single-line comments, multi-line comments will be added in the future.
```
// This is a single-line comment
```


# Uranium Lang - How does it work

The Uranium Compiler "runs through" your source code and tokenizes it. The resulting tokens are then
rearranged and resstructured so that they can be tarnslated to C++ more easily.
Yes, Uranium Lang is not directly compiled to machine code, it gets compiled into C++ and
relies on an external C++ Compiler to do the rest of the compilation.
