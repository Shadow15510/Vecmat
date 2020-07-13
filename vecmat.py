# --------------------------------------------------
# Vecmat (Version 1.3)
# by coco33920 and Shadow15510
# last version released on the 11 of July.
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

  __radd__ = __add__
  __rmul__ = __mul__

  def __abs__(self):
    return sqrt(sum(list(map(lambda i: i**2, self.coord))))

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


  def __add__(self, matrix: "Matrix"):
    if self.get_dim() != matrix.get_dim():
      raise ArithmeticError("The dimensions are incompatible")
    return Matrix(*[[self.content[i][j] + matrix.content[i][j] for j in range(len(self.content[0]))] for i in range(len(self.content))])
  
  def __sub__(self, matrix: "Matrix"):
    if self.get_dim() != matrix.get_dim():
      raise ArithmeticError("The dimensions are incompatible")
    return Matrix(*[[self.content[i][j] - matrix.content[i][j] for j in range(len(self.content[0]))] for i in range(len(self.content))])
 
  def __mul__(self, x):
    if isinstance(x, (float, int)):
      return Matrix(*[[self.content[i][j] * x for j in range(len(self.content[0]))] for i in range(len(self.content))])
    elif isinstance(x, Matrix):
      return Matrix(*[[sum([self.content[j][i] * x.content[i][j] for i in range(len(self.content[0]))]) for k in range(len(x.content[0]))] for j in range(len(self.content))])
    else:
      raise TypeError("The wrong types were given")

  def __truediv__(self, x):
    if isinstance(x, (float, int)):
      return Matrix(*[[self.content[i][j] / x for j in range(len(self.content[0]))] for i in range(len(self.content))])
    elif isinstance(x, Matrix):
      return self * x.inverse()
    else:
      raise TypeError("The wrong types were given")
  
  def __str__(self):
    return "\n".join(map(str, self.content))

  __radd__ = __add__
  __rmul__ = __mul__

  def get_coef(self, i, j):
    return self.content[i][j]
    
  def get_dim(self):
    return len(self.content), len(self.content[0])
    
  def augment(self, mat: "Matrix"):
     [self.content[i].append(mat.content[i][j]) for j in range(len(self.content[0])) for i in range(len(self.content))]
        
  def sub(self, row_st, column_st, row_ed, column_ed):
    return Matrix(*[[self.content[i][j] for j in range(column_st, column_ed+1)] for i in range(row_st, row_ed+1)])
  
  def det(self):
    def calc_det(mat: "Matrix"):
      rslt = 0
      if mat.get_dim() == (1, 1): rslt += mat.content[0][0]
      else:
        for i in range(len(mat.content[0])): rslt += (mat.content[0][i], -mat.content[0][i])[i % 2] * calc_det(mat.s_mat(i, 0))
      return rslt
    return calc_det(self)

  def gauss_jordan_determinant(self):
    pass
    
  def swapping_rows(self, r1: int, r2: int):
    self.content[r1], self.content[r2] = self.content[r2], self.content[r1]

  def add_multiple_of_row(self, row1: int, row2: int, multiple: float):
    #Multiply row1 by multiple and adding that to row2
    self.content[row2] = list(map(lambda x,y: x+y, map(lambda x: x*multiple, self.content[row1]), self.content[row2]))

  def transpose(self):
    return Matrix(*[[self.content[i][j] for i in range(len(self.content))] for j in range(len(self.content[0]))])
  
  def s_mat(self, jmp_i: "int", jmp_j: "int"):
    return Matrix(*[[self.content[j][i] for i in range(len(self.content)) if i != jmp_i] for j in range(len(self.content[0])) if j != jmp_j])  

  def comat(self):
    return Matrix(*[[(-1) ** (i + j) * self.s_mat(i, j).det() for i in range(len(self.content))] for j in range(len(self.content[0]))])

  def inverse(self):
    return self.comat().transpose() * (1/self.det())

  def switch_row(self, row_1: "int", row_2: "int"):
    for j in range(len(self.content[0])): self.content[row_1][j], self.content[row_2][j] = self.content[row_2][j], self.content[row_1][j]

  def switch_column(self, column_1: "int", column_2: "int"):
    for i in range(len(self.content)): self.content[i][column_1], self.content[i][column_2] = self.content[i][column_2], self.content[i][column_1]
    
  def write_row(self, index: "int", new_row):
    for j in range(len(self.content[0])): self.content[index][j] = new_row.content[0][j]

  def write_column(self, indef: "int", new_column):
    for i in range(len(self.content)): self.content[i][index] = new_column.content[i][0]
    
def identity(n: "int"):
  return Matrix(*[[int(i == j) for i in range(n)] for j in range(n)])
    
    
    
