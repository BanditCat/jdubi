import random
import numpy as np
import time

def etransform( s, l, sq ):
  m = l
  for i in range( len( s ) ):
    s[ i ] = sq[ m ][ s[ i ] ]
    m = s[ i ]

def irreversible( pre, s, sq, rounds ):
  ret = s.copy()
  for r in range( rounds ):
    for i in range( len( pre ) ):
      etransform( ret, pre[ i ], sq )
    for i in range( len( s ) ):
      etransform( ret, s[ ( len( s ) - 1 ) - i ], sq )
  return ret
    
ex1sq = [ [ 2, 1, 0, 3 ],
          [ 3, 0, 1, 2 ],
          [ 1, 2, 3, 0 ],
          [ 0, 3, 2, 1 ] ]
ex2 = [ 0, 1, 2, 3, 0 ]

# test against examples in paper
# https://eprint.iacr.org/2005/352.pdf page 4, should see 0 0 1 0 3 and 0 3 2 0 2
print( ex1sq )
print( irreversible( [], ex2, ex1sq, 1 ) )
print()
print( irreversible( [], ex2, ex1sq, 2 ) )

# 256square.txt must be 256 lines long with each line containing 256 elements of 0-255. It makes a latin square that defines the function used for cryptography. https://sci-hub.tw/10.1002/(SICI)1520-6610(1996)4:6%3C405::AID-JCD3%3E3.0.CO;2-J prints BURN!!! warning if not a latin square
with open( '256square.txt' ) as f:
  arr = [[int(x) for x in line.split()] for line in f]
  array = np.array( arr, dtype = np.uint8 )
  print( array )
  for i in range( 256 ):
    row = np.zeros( shape = 256, dtype = np.uint8 )
    col = np.zeros( shape = 256, dtype = np.uint8 )
    for j in range( 256 ):
      if row[ array[ i ][ j ] ] != 0:
        print( "\n\n\nBURN!!!\n\n\n\n\n\nBURN!!!\n\n\n\n\n\nBURN!!!\n\n\n" )
      row[ array[ i ][ j ] ] = 1
      if col[ array[ j ][ i ] ] != 0:
        print( "\n\n\nBURN!!!\n\n\n\n\n\nBURN!!!\n\n\n\n\n\nBURN!!!\n\n\n" )
      col[ array[ j ][ i ] ] = 1
      


class Crypt:
  def __init__( self, password, sq ):
    self.latinSquare = sq
    self.password = np.fromstring( password, dtype = np.uint8 )
    self.reset( np.arange( 256, dtype = np.uint8 ) )
  def reset( self, arr ):
    self.state = irreversible( self.password, arr, self.latinSquare, 5 )
  def nextstate( self ):
    next = irreversible( self.password, self.state, self.latinSquare, 5 )
    self.state += next
  def encrypt( self, string ):
    str = np.fromstring( string, dtype = np.uint8 )
    pre = str.copy()
    if len( pre ) < 256:
      pre = np.append( pre, np.zeros( 256 - len( pre ), dtype = np.uint8 ) )
    else:
      pre = pre[:256]
    q = int( time.time() * 100 )
    pre[ 0 ] += q >> 0 & 255
    pre[ 1 ] += q >> 8 & 255 
    pre[ 2 ] += q >> 16 & 255 
    pre[ 3 ] += q >> 24 & 255 
    self.reset( pre )
    ret = self.state.copy()
    self.nextstate()
    modlength = ( len( str ) + 1 ) % 256
    str = np.append( np.array( [ modlength ], dtype = np.uint8 ), str )
    str = np.append( str, np.zeros( 256 - modlength, dtype = np.uint8 ) )
    while len( str ) > 0:
      self.state += str[:256]
      ret = np.append( ret, self.state )
      str = str[256:]
      self.nextstate()
    return ret
  def decrypt( self, string ):
    str = string.copy()
    self.state = str[:256]
    str = str[256:]
    ret = np.empty( 0, dtype = np.uint8 )
    while len( str ) > 0:
      self.nextstate()
      dec = str[:256] - self.state
      ret = np.append( ret, dec )
      self.state += dec
      str = str[256:]
    return ret[ 1 : len( ret ) - ( 256 - ret[ 0 ] ) ] 
      
e = Crypt( "correct Horse B@ttery 5taple", array )
e.nextstate()
enc = e.encrypt( 'catactus' * 1000 )
print( 'enc' )
f = Crypt( "correct Horse B@ttery 5taple", array )
dec = f.decrypt( enc ).tostring()
print( 'dec' )
