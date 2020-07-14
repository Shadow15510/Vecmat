# --------------------------------------------------
# Vecmat (Version 1.3.4 - Bêta)
# by Charlotte THOMAS and Sha-Chan~
# last version released on the 14 of July.
#
# code provided with licence (CC BY-NC-SA 4.0)
# for more information about licence :
# https://creativecommons.org/licenses/by-nc-sa/4.0/
# --------------------------------------------------

from math import *

class Vector:
  def __init__(self, *coord):
    self.coord = list(coord)
    self.dim = len(coord)

  def __add__(self, vec: "Vector"):
    if vec.dim != self.dim:
      raise ArithmeticError("The dimensions are incompatible")
    return Vector(*map(lambda x,y: x+y, self.coord, vec.coord))

  def __sub__(self, vec: "Vector"):
    if vec.dim != self.dim:
      raise ArithmeticError("The dimensions are incompatible")
    return Vector(*map(lambda x,y: x-y, self.coord, vec.coord))

  def __mul__(self, x):
    if isinstance(x, (float, int)):
      return Vector(*map(lambda y: x*y, self.coord))
    if isinstance(x, Vector):
      return Vector(*map(lambda y,z: y*z, self.coord, x.coord))
    else:
      raise TypeError("The wrong types were given")

  def __truediv__(self, x):
    if isinstance(x, (float, int)):
      return Vector(*map(lambda y: y/x, self.coord))
    if isinstance(x, Vector):
      return Vector(*map(lambda y,z: y/z, self.coord, x.coord))
    else:
      raise TypeError("The wrong types were given")

  def __str__(self):
    return str(tuple(self.coord))

  def __abs__(self):
    return sqrt(sum(list(map(lambda i: i**2, self.coord))))

  def __getitem__(self, index):
    return self.coord[index]

  __radd__ = __add__
  __rmul__ = __mul__

  def unitV(self):
    a = abs(self)
    return Vector(*map(lambda x: x/a, self.coord))
    
  def dotP(self, vec: "Vector"):
    return sum(list(map(lambda x,y: x*y, self.coord, vec.coord)))
  
  def crossP(self, vec: "Vector"):
    if self.dim == 3 and vec.dim == 3: return Vector(self.z*vec.y - self.y*vec.z, self.x*vec.z - self.z*vec.x, self.y*vec.x - self.x*vec.y)

  def det(self, *vec):
    return Matrix([self.coord] + [i.coord for i in vec]).det()
  
  def colinear(self, vec: "Vector"):
    return not self.det(vec)

  def angle(self, vec: "Vector"):
    return round(degrees(acos(self.dotP(vec) / (abs(self)*abs(vec)))), 2)


class Matrix:
  def __init__(self, *row):
    self.content = [i for i in row]

  def __getitem__(self, index):
    return self.content[index]

  def __add__(self, matrix: "Matrix"):
    if self.get_dim() != matrix.get_dim():
      raise ArithmeticError("The dimensions are incompatible")
    return Matrix(*[[self[i][j] + matrix[i][j] for j in range(len(self[0]))] for i in range(len(self.content))])
  
  def __sub__(self, matrix: "Matrix"):
    if self.get_dim() != matrix.get_dim():
      raise ArithmeticError("The dimensions are incompatible")
    return Matrix(*[[self[i][j] - matrix[i][j] for j in range(len(self[0]))] for i in range(len(self.content))])
 
  def __mul__(self, x):
    if isinstance(x, (float, int)):
      return Matrix(*[[self[i][j] * x for j in range(len(self[0]))] for i in range(len(self.content))])
    elif isinstance(x, Matrix):
      return Matrix(*[[sum([self[j][i] * x[i][j] for i in range(len(self[0]))]) for k in range(len(x[0]))] for j in range(len(self.content))])
    else:
      raise TypeError("The wrong types were given")

  def __truediv__(self, x):
    if isinstance(x, (float, int)):
      return Matrix(*[[self[i][j] / x for j in range(len(self[0]))] for i in range(len(self.content))])
    elif isinstance(x, Matrix):
      return self * x.inverse()
    else:
      raise TypeError("The wrong types were given")
  
  def __str__(self):
    return "\n".join(map(str, self.content))

  __radd__ = __add__
  __rmul__ = __mul__

  
  def __gauss_jordan_elimination(self):
    def add_multiple_of_row(mat, row1: int, row2: int, multiple: float):
      mat[row2][:] = list(map(lambda x,y: x+y, map(lambda x: x*multiple, self[row1]), self[row2]))
      return mat
      
    j, mat, sign, det = -1, self, 0, 1
    
    for i in range(len(mat.content) - 1):
      j += 1
      det *= mat[i][j]
      
      for k in range(i + 1, len(mat[0])):
        if not mat[i][j]:
          mat.switch_row(k, i)
          sign += 1
        mat = add_multiple_of_row(mat, i, k, -mat[k][j] / mat[i][j])
        
    return mat, mat.trace() * det * (-1)**sign
  
  def get_dim(self):
    return len(self.content), len(self[0])
    
  def augment(self, mat: "Matrix"):
     [self[i].append(mat[i][j]) for j in range(len(self[0])) for i in range(len(self.content))]
        
  def sub(self, row_st, column_st, row_ed, column_ed):
    return Matrix(*[[self[i][j] for j in range(column_st, column_ed+1)] for i in range(row_st, row_ed+1)])
  
  def det(self):
    return self.__gauss_jordan_elimination()[1]

  def row_echelon_form(self):
    return self.__gauss_jordan_elimination()[0]

  def trace(self):
    rslt = 1
    for i in range(len(self.content)):
      for j in range(len(self[0])):
        if i == j: rslt *= self[i][j]
    return rslt
        
  def transpose(self):
    return Matrix(*[[self[i][j] for i in range(len(self.content))] for j in range(len(self[0]))])
  
  def comat(self):
    return Matrix(*[[(-1) ** (i + j) * self.s_mat(i, j).det() for i in range(len(self.content))] for j in range(len(self[0]))])

  def inverse(self):
    return self.comat().transpose() * (1/self.det())

  def switch_row(self, row_1: "int", row_2: "int"):
    self[row_1][:], self[row_2][:] = self[row_2][:], self[row_1][:]

  def switch_column(self, column_1: "int", column_2: "int"):
    for i in range(len(self.content)): self[i][column_1], self[i][column_2] = self[i][column_2], self[i][column_1]
    
  def write_row(self, index: "int", new_row: "list"):
    self[index][:] = new_row[:]

  def write_column(self, indef: "int", new_column: "list"):
    for i in range(len(self.content)): self[i][index] = new_column[i][0]
     
def identity(n: "int"):
  return Matrix(*[[int(i == j) for i in range(n)] for j in range(n)])
    
    
    
