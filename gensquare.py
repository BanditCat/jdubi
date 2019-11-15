
import numpy as np
import random

#The algorithm used to generate the latin square is https://sci-hub.tw/10.1002/(SICI)1520-6610(1996)4:6%3C405::AID-JCD3%3E3.0.CO;2-J

def gencube( n ):
  ret = np.zeros( shape = ( n, n, n ), dtype = np.int8 )
  for x in range( n ):
    for y in range( n ):
      ret[ x ][ y ][ ( x + y ) % n ] = 1
  return ret


def printcube( c ):
  print()
  n = c.shape[ 0 ]
  for x in range( n ):
    for y in range( n ):
      for z in range( n ):
        if c[ x ][ y ][ z ] == 1:
          print( '% 4d' % z, end = '' )
    print()


def plusminuscubemove( c, c1, c2 ):
  x, y, z = c1
  x2, y2, z2 = c2
  c[ x ][ y ][ z2 ] = 0
  c[ x ][ y2 ][ z ] = 0
  c[ x2 ][ y ][ z ] = 0
  c[ x ][ y2 ][ z2 ] = 1
  c[ x2 ][ y ][ z2 ] = 1
  c[ x2 ][ y2 ][ z ] = 1
  return c[ x2 ][ y2 ][ z2 ] == 1
    
def movecube( c ):
  n = c.shape[ 0 ]
  # First set x, y, z to a 0-cell and turn it to a 1-cell
  x = random.randint( 0, n - 1 )
  y = random.randint( 0, n - 1 )
  z = random.randint( 0, n - 2 )
  for i in range( z + 1 ):
    if c[ x ][ y ][ i ] == 1:
      z += 1
  # Find x2, y2, z2 based on the 1-cells around ( x, y, z )
  for i in range( n ):
    if c[ i ][ y ][ z ] == 1:
      x2 = i
    if c[ x ][ i ][ z ] == 1:
      y2 = i
    if c[ x ][ y ][ i ] == 1:
      z2 = i
  c[ x ][ y ][ z ] = 1
  # Do the move
  found = plusminuscubemove( c, ( x, y, z ), ( x2, y2, z2 ) )
  if found:
    c[ x2 ][ y2 ][ z2 ] = 0
  else:
    while True:
      x = x2
      y = y2
      z = z2
      x2 = y2 = z2 = -1
      for i in range( n ):
        if c[ i ][ y ][ z ] == 1:
          if x2 == -1:
            x2 = i
          else:
            if random.randint( 0, 1 ) == 0:
              x2 = i
        if c[ x ][ i ][ z ] == 1:
          if y2 == -1:
            y2 = i
          else:
            if random.randint( 0, 1 ) == 0:
              y2 = i
        if c[ x ][ y ][ i ] == 1:
          if z2 == -1:
            z2 = i
          else:
            if random.randint( 0, 1 ) == 0:
              z2 = i
      found = plusminuscubemove( c, ( x, y, z ), ( x2, y2, z2 ) )
      if found:
        c[ x2 ][ y2 ][ z2 ] = 0
        break;

c = gencube( 256 )

printcube( c )

for i in range( 10000 ):
  print( i )
  movecube( c )

printcube( c )
