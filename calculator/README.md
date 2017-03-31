# [pyp-w1] Extensible calculator

Today you will be coding to build a calculator. Even though that sounds simple,
this won't be a regular calculator. You must implement it in a way that users
of the calculator are able to "extend" its functionally by adding as many
custom operations as they want. For that to be doable, we will make usage of
the high-order functions concept we've covered in class.

Operations will be defined as regular functions. There's just one important thing
you must have in mind. All operations need to keep the same interface, meaning
they all must be executable sending the same parameters. To have extra
flexibility, we will assume that all operations receives a variable number
or arguments (`*args`), like the following code:

```python
def add(*args):
    """
    Returns a number representing the sum of all given arguments.
    """
    # your implementation here
    pass
```

In many cases, operations are simple enough to be implemented just using a `lambda`:

```python
subtract = lambda *args: pass  # your code here
```

Operations are independent entities. You should be able to use them outside
any other code, even outside of the calculator you are supposed to build.
To use an operator follow this logic:

```python
>>> subtract(100, 20, 10, 20)
50
>>> subtract(100, 20)  # must accept variable number of arguments
80
```

If you reached this point, you should now be ready to start coding your calculator.
To create a new calculator you must follow this interface:

```python
>>> calc = create_new_calculator(operations={'add': add, 'subtract': subtract, ...})
{
    'operations': {
        'add': add,
        'subtract': subtract,
        ...
    },
    'history': [
        ('2016-05-18 12:00:00', 'add', (1, 2, 3, 4), 10),
        ('2016-05-18 12:10:00', 'multiply', (1, 2, 3, 4), 24),
        ...
    ]
}
```

As it's shown in the sample code, a `calculator` is just a data structure
(dict in this case) holding the collection of operations the calculator supports
and keeping track of the operation execution history.

Once you have the calculator created, you can start using it:

```python
>>> perform_operation(calc, 'add', params=(1, 2, 3, 4))
10
```

You must consider possible errors that might occur while using the calculator:

```python
>>> perform_operation(calc, 'something-weird', params=(1, 2, 3, 4))
InvalidOperation: "something-weird" operation not supported.
>>> perform_operation(calc, 'something-weird', params=False)
InvalidParams: Given params are invalid.
>>> perform_operation(calc, 'something-weird')  # params not sent
InvalidParams: Given params are invalid.
```

As the title of this group work says, the calculator must be extensible. That
means, after a calculator is created, new operations can be dynamically added to it.
To do that, you must implement the following method:

```python
>>> square_root = lambda ...
>>> add_new_operation(calc, operation={'square_root': square_root})
```
If at any time you need to know the whole list of supported operations, you
can invoke the `get_operations` method on the calculator, which will return
a collection of the operation names:

```python
>>> get_operations(calc)
['add', 'subtract', 'divide', 'multiply']
```

The calculator must be smart enough to keep track of the list of operations
the user has executed since the last reset. For each operation in the history
you must record the operation name, the collection of arguments the user sent
and a datetime object representing the execution time.

To query the history of executed operations, just call the `get_history` method:

```python
>>> get_history(calc)
[
    ('2016-05-18 12:00:00', 'add', (1, 2, 3, 4), 10),
    ('2016-05-18 12:10:00', 'multiply', (1, 2, 3, 4), 24),
    ...
]
```

Reseting the history is also possible by executing the `reset_history` method:

```python
>>> reset_history(calc)
>>> get_history(calc)
[]
```

As we keep track of all the operations we execute, it must be possible too to
repeat the last executed action. From time to time this is useful to avoid re
writing the whole operation command.

```python
>>> perform_operation(calc, 'subtract', params=(10, 2, 3, 4))
1
>>> repeat_last_operation(calc)
1
```

As a quick summary, this is the interface your calculator must respect:

```
create_new_calculator

perform_operation

add_new_operation

get_operations

get_history

reset_history

repeat_last_operation
```

If you want to get some extra points, and have some extra fun you can add
a new `plot` operation to your calculator. This `plot` operation takes a function
expression as a parameter (ie: '-2*x + 4'), and two digits representing the range
in which the variable "x" must be evaluated. Example:

```
>>> plot = lambda *args: ...
>>> add_new_operation(calc, operation=plot)
>>> perform_operation(calc, 'plot', params=('-x**2', -2, 2))
-0 |             ... ...
   |           ..       ..
   |          /           \
   |         /             \
   |        /               \
   |       /                 \
   |      .                   .
-2 | ------------------------------
   |     .                     .
   |    .                       .
   |
   |   .                         .
   |
   |  .                           .
-4 | /
     -2         0              2
```

*Hint: Investigate `sympy` library*
