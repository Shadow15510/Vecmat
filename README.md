# Vecmat

## General presentation

### Presentation

Vecmat is a librairie of vectorial and matricial manipulations. This librairie is oriented-object, so you can use `Vector` and `Matrix` like `list` or `str` objects. This librairie was made by Charlotte THOMAS and Sha-Chan~.

Version 1.3.2 - Bêta released on 13 of July.

### Licence

This code is provided with licence (CC BY-NC-SA 4.0). For more information about licence please [click here](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Vector's manipulations

### Generalities

The `Vector` objets was designed for support n dimensions. Such as `u = Vector(1, 1)` creates a two-dimensional vector, or even `u = Vector(1, 2, 3, 4, 5)` creates a five-dimensional vector. (Don't forget the dot for use the handlings, for instance : `my_vector.unitV()`.)

### Vectorial manipulations available

#### Handlings on the vector itself

 - Vectors are printable and return a string representation of their coordonates.
 - Theys also are subscriptable : `my_vector[0]` returns the first coordinate.
 - For the vector's norm, use `abs`function. `abs(my_vector)`
 - `unitV()` : Returns the unitary vector.

#### Basical mathematical operations between two vectors

The vectors supports the basic operation `+` and `-` for the addition and substraction between two vectors and `*` and `/` for the multiplication and division between a vector and a real number, they also work for element-wise multiplication between two vectors.

#### Advanced vector manipulations

 - `dotP(vec)` : Returns the dot product.
 - `crossP(vec)` : Returns the cross product. (Only available for two three-dimensions vectors.)
 - `det(*vec)` : Returns the vectors's determinant. You can pass several vectors without any problem. (Please take care to pass n vectors to n dimensions.)
 - `colinear(vec)` : Tests the colinearty between the vectors. Return a boolean.
 - `angle(vec)` : Returns the angle in degrees between the vectors.

## Matrix's manipulations

### Generalities

`Matrix` was designed for support n * m dimensions, so you don't have to take care at dimensions. If an error occured, it's because the dimensions doesn't allow to calculate what you want. For exemple, the matrix's determinant is only available with squarred matrix. As well as for `Vector`, don't forget the dot for use these handlings.

For initialise a matrix follow this scheme `M = Matrix([1, 2], [3, 4])`. You can everything you want, just take care to have one row per argument : `Matrix([0])` for a matrix with one row and one column.

### Matricial manipulations available

#### Handlings on the matrix itself

 - The matrices are printable and return a string representation of the column and rows.
 - They also are subscriptable.
 - `get_dim()` : Returns the dimension of the matrix. The results is a tuple : `(row, column)`.
 - `switch_row(row_1, row_2)` : Reverses the two rows.
 - `switch_column(column_1, column_2)` : Reverses the two columns.
 - `write_row(index, new_row)` : Replaces the index-row by the new row
 - `write_column(index, new_column)` : Replaces the index-column by the new column

#### Basical mathematical operations

The matrices supports basic operation, `+` and `-` for addition/substraction between two matrices and `*` and `/` for multiplication and division between a matrix and a real number, they also work for multiplication between two matrices.

#### Advanced matricial manipulations

 - `augment(mat)` : Allows to augment the size of the matrix by adding another matrix to the first one.
 - `sub(row_st, column_st, row_ed, column_ed)` : Returns a sub-matrix between the given limits.
 - `det()` : Returns the matrix's determinant.
 - `tranpose()` : Returns the transpose matrix.
 - `s_mat(jmp_i, jmp_j)` : Returns the matrix without the i-row and j-column.
 - `comat()` : Returns the co-matrix.
 - `inverse()` : Returns the inverse matrix. (Please take care to the determinant.)

## Other manipulations

### Generalities

These handlings are not concerned by the oriented-object code.

### Available functions

 - `identity(n)` : Returns an identity matrix of order n. (This is a `Matrix` object.)
