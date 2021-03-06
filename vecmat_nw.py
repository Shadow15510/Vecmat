# --------------------------------------------------
# Vecmat (Version 1.5.1 NumWorks)
# by Charlotte THOMAS and Sha-chan~
# last version released on the 13rd of September 2020.
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

from math import *

class Vector:
  def __init__(self, *coord):
    self.coord = list(coord)
    self.dim = len(coord)

  def __add__(self, vec):
    return Vector(*map(lambda x,y: x+y, self.coord, vec.coord))

  def __sub__(self, vec):
    return Vector(*map(lambda x,y: x-y, self.coord, vec.coord))

  def __mul__(self, x):
    if isinstance(x, (float, int)):
      return Vector(*map(lambda y: x*y, self.coord))
    if isinstance(x, Vector):
      return Vector(*map(lambda y,z: y*z, self.coord, x.coord))

  def __truediv__(self, x):
    if isinstance(x, (float, int)):
      return Vector(*map(lambda y: y/x, self.coord))
    if isinstance(x, Vector):
      return Vector(*map(lambda y,z: y/z, self.coord, x.coord))

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
    
  def dotP(self, vec):
    return sum(list(map(lambda x,y: x*y, self.coord, vec.coord)))
  
  def crossP(self, vec):
    if self.dim == 3 and vec.dim == 3: return Vector(self.z*vec.y - self.y*vec.z, self.x*vec.z - self.z*vec.x, self.y*vec.x - self.x*vec.y)

  def det(self, *vec):
    return Matrix([self.coord] + [i.coord for i in vec]).det()
  
  def colinear(self, vec):
    return not self.det(vec)

  def angle(self, vec):
    return round(degrees(acos(self.dotP(vec) / (abs(self)*abs(vec)))), 2)


class Matrix:
  def __init__(self, *row):
    self.content = [i for i in row]

  def __getitem__(self, index):
    return self.content[index]

  def __add__(self, matrix):
    return Matrix(*[[self[i][j] + matrix[i][j] for j in range(len(self[0]))] for i in range(len(self.content))])
  
  def __sub__(self, matrix):
    return Matrix(*[[self[i][j] - matrix[i][j] for j in range(len(self[0]))] for i in range(len(self.content))])
 
  def __mul__(self, x):
    if isinstance(x, (float, int)):
      return Matrix(*[[self[i][j] * x for j in range(len(self[0]))] for i in range(len(self.content))])
    elif isinstance(x, Matrix):
      return Matrix(*[[sum([self[j][i] * x[i][j] for i in range(len(self[0]))]) for k in range(len(x[0]))] for j in range(len(self.content))])

  def __truediv__(self, x):
    if isinstance(x, (float, int)):
      return Matrix(*[[self[i][j] / x for j in range(len(self[0]))] for i in range(len(self.content))])
    elif isinstance(x, Matrix):
      return self * x.inverse()

  def __str__(self):
    return "\n".join(map(str, self.content))

  __radd__ = __add__
  __rmul__ = __mul__

  def __copy(self):
    return Matrix(*[[nb for nb in row] for row in self.content])
  
  def __gauss_jordan_elimination(self):
    def add_multiple_of_row(mat, row1, row2, multiple):
      mat[row2][:] = list(map(lambda x,y: x+y, map(lambda x: x*multiple, mat[row1]), mat[row2]))
      return mat      
    mat, sign, det = self.__copy(), 0, 1
    
    for i in range(len(mat.content) - 1):
      det *= mat[i][i]
      
      for k in range(i + 1, len(mat.content)):
        if not mat[i][i]:
          mat.switch_row(k, i)
          sign += 1
        mat = add_multiple_of_row(mat.__copy(), i, k, -mat[k][i] / mat[i][i])
        
    return mat, mat.trace() * det * (-1)**sign

  def __s_mat(self, jmp_i, jmp_j):
    return Matrix(*[[self.content[j][i] for i in range(len(self.content)) if i != jmp_i] for j in range(len(self.content[0])) if j != jmp_j])  

  def get_dim(self):
    return len(self.content), len(self[0])
    
  def augment(self, mat):
     [self[i].append(mat[i][j]) for j in range(len(mat[0])) for i in range(len(mat.content))]
        
  def sub(self, row_st, column_st, row_ed, column_ed):
    return Matrix(*[[self[i][j] for j in range(column_st, column_ed+1)] for i in range(row_st, row_ed+1)])
  
  def det(self):
    return self.__gauss_jordan_elimination()[1]

  def ref(self):
    return self.__gauss_jordan_elimination()[0]

  def rref(self):
    mat = self.__copy()
    mat = mat.ref()
    for row in range(len(mat.content)):
      pivot = mat[row][row]
      if pivot:
        for column in range(len(mat.content)):
          mat[row][column] /= pivot          
    return mat

  def trace(self):
    rslt = 1
    for i in range(len(self.content)): rslt *= self[i][i]
    return rslt
        
  def transpose(self):
    return Matrix(*[[self[i][j] for i in range(len(self.content))] for j in range(len(self[0]))])
  
  def comat(self):
    return Matrix(*[[(-1) ** (i + j) * self.__s_mat(i, j).det() for i in range(len(self.content))] for j in range(len(self[0]))])

  def inverse(self):
    return self.comat().transpose() * (1/self.det())

  def switch_row(self, row_1, row_2):
    self[row_1][:], self[row_2][:] = self[row_2][:], self[row_1][:]

  def switch_column(self, column_1, column_2: "int"):
    for i in range(len(self.content)): self[i][column_1], self[i][column_2] = self[i][column_2], self[i][column_1]
    
  def write_row(self, index, new_row):
    self[index][:] = new_row[:]

  def write_column(self, index, new_column):
    for i in range(len(self.content)): self[i][index] = new_column[i][0]
       
def identity(n: "int"):
  return Matrix(*[[int(i == j) for i in range(n)] for j in range(n)])
    
