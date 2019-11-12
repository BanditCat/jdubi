
import numpy as np
import time
import click

def etransform2( s, l, sq ):
  m = l
  for i in range( len( s ) ):
    s[ i ] = sq[ m ][ s[ i ] ]
    m = s[ i ]
  return s

def etransform( s, l, sq ):
  s2 = np.append( np.array( [ l ], dtype = np.uint8 ), np.array( s[:len(s) - 1], dtype = np.uint8 ) )
  s = (sq.flatten())[ len( sq ) * s + s2 ]
  return s

def irreversible2( pre, s, sq, rounds ):
  ret = s.copy()
  for r in range( rounds ):
    for i in range( len( pre ) ):
      ret = etransform2( ret, pre[ i ], sq )
    for i in range( len( s ) ):
      ret = etransform2( ret, s[ ( len( s ) - 1 ) - i ], sq )
  return ret
   
def irreversible( pre, s, sq, rounds ):
  ret = s.copy()
  for r in range( rounds ):
    for i in range( len( pre ) ):
      ret = etransform( ret, pre[ i ], sq )
    for i in range( len( s ) ):
      ret = etransform( ret, s[ ( len( s ) - 1 ) - i ], sq )
  return ret
    

# 256square.txt must be 256 lines long with each line containing 256 elements of 0-255. It defines a latin square that is the function used for cryptography. https://sci-hub.tw/10.1002/(SICI)1520-6610(1996)4:6%3C405::AID-JCD3%3E3.0.CO;2-J prints warning and exits if not a latin square.
with open( '256square.txt' ) as f:
  arr = [[int(x) for x in line.split()] for line in f]
  array = np.array( arr, dtype = np.uint8 )
  for i in range( 256 ):
    row = np.zeros( shape = 256, dtype = np.uint8 )
    col = np.zeros( shape = 256, dtype = np.uint8 )
    for j in range( 256 ):
      if row[ array[ i ][ j ] ] != 0:
        print( "256square.txt was not a latin square!" )
        exit()
      row[ array[ i ][ j ] ] = 1
      if col[ array[ j ][ i ] ] != 0:
        print( "256square.txt was not a latin square!" )
        exit()
      col[ array[ j ][ i ] ] = 1
      


class Crypt:
  def __init__( self, password, sq ):
    self.latinSquare = sq
    # Strengthen all passwords
    self.password = np.fromstring( password, dtype = np.uint8 )
    self.password = np.append( self.password, np.zeros( 32, dtype = np.uint8 ) )
    self.password = irreversible( self.password, self.password, self.latinSquare, 3 )
  def reset( self, arr ):
    self.state = irreversible( self.password, arr, self.latinSquare, 3 )
  def nextstate( self ):
    next = irreversible( self.password, self.state, self.latinSquare, 3 )
    self.state += next
  def encrypt( self, string ):
    str = np.fromstring( string, dtype = np.uint8 )
    pre = str.copy()
    if len( pre ) < 256:
      pre = np.append( pre, np.zeros( 256 - len( pre ), dtype = np.uint8 ) )
    else:
      pre = np.append( pre, np.zeros( 256 - ( len( pre ) % 256 ), dtype = np.uint8 ) )
      temp = pre[:256]
      while( len( pre ) > 256 ):
        pre = pre[256:]
        temp += pre[:256]
      pre = temp
    q = int( time.time() * 100 )
    for i in range( 8 ):
      pre[ i ] += q >> ( i * 8 ) & 255
    self.reset( pre )
    self.ret = self.state.copy()
    self.nextstate()
    modlength = ( len( str ) + 1 ) % 256
    str = np.append( np.array( [ modlength ], dtype = np.uint8 ), str )
    self.str = np.append( str, np.zeros( 256 - modlength, dtype = np.uint8 ) )
    return len( self.str ) // 256
  def encryption( self ):
    self.state += self.str[:256]
    self.ret = np.append( self.ret, self.state )
    self.str = self.str[256:]
    self.nextstate()
    return len( self.str ) // 256
  def decrypt( self, string ):
    self.str = string.copy()
    self.state = self.str[:256]
    self.str = self.str[256:]
    self.ret = np.empty( 0, dtype = np.uint8 )
    return len( self.str ) // 256
  def decryption( self ):
    self.nextstate()
    dec = self.str[:256] - self.state
    self.ret = np.append( self.ret, dec )
    self.state += dec
    self.str = self.str[256:]
    if len( self.str ) == 0:
      self.ret = self.ret[ 1 : len( self.ret ) - ( 256 - self.ret[ 0 ] ) ]
    return len( self.str ) // 256

@click.command()
@click.option( '-t', '--test/--no-test', help = 'Run tests from https://eprint.iacr.org/2005/352.pdf, 00103 and 03202 should be displayed.' )
@click.option( '-d', '--decrypt/--encrypt', help = 'Decrypt rather than encrypt. Encryption is the default.' )
@click.option( '-pw', '--password-file', help = 'Password file.' )
@click.option( '-i', '--input-file', help = 'Input file.' )
@click.option( '-o', '--output-file', help = 'Output file.' )

def prog( password_file, test, decrypt, input_file, output_file ):
  """Encrypts/decrypts using latin squares."""
  if test:
    ex1sq = np.array( [ [ 2, 1, 0, 3 ],
                        [ 3, 0, 1, 2 ],
                        [ 1, 2, 3, 0 ],
                        [ 0, 3, 2, 1 ] ], dtype = np.uint8 )
    ex2 = np.array( [ 0, 1, 2, 3, 0 ], dtype = np.uint8 )

    # test against examples in paper
    # https://eprint.iacr.org/2005/352.pdf page 4, should see 0 0 1 0 3 and 0 3 2 0 2
    click.echo( "Latin square: %s" % ex1sq )
    click.echo( "Example r1: %s" % irreversible2( [], ex2, ex1sq, 1 ) )
    click.echo()
    click.echo( "Example r2: %s" % irreversible2( [], ex2, ex1sq, 2 ) )
    exit()

  if not input_file or not output_file:
    print( "Input and output file are required." )
    exit()
    
  if password_file:
    try:
      with open( password_file ) as f:
        pw = f.read()
    except IOError as x:
      print( "Could not open password file." )
      exit()
  else:
    pw = click.prompt( "Password", hide_input = True, confirmation_prompt = True )

  try:
    with open( input_file ) as f:
      input = np.fromstring( f.read(), dtype = np.uint8 )
  except IOError as x:
    print( "Could not open input file." )
    exit()

  c = Crypt( pw, array )
  if decrypt:
    word = 'decrypt'
    f1 = c.decrypt
    f2 = c.decryption
  else:
    word = 'encrypt'
    f1 = c.encrypt
    f2 = c.encryption
  click.echo( "Starting %sion of %s." % ( word, input_file ) ) 
  t = time.time() * 1000.0
  
  r = range( f1( input ) )
  with click.progressbar( r ) as progbar:
    for i in progbar:
      te = f2()
  res = c.ret
  try:
    with open( output_file, "wb" ) as f:
      f.write( res )
      f.close()
  except IOError as x:
    print( "Could not open output file." )
    exit()
  click.echo( "Finished %sion of %s: %d milliseconds." % ( word, input_file, time.time() * 1000.0 - t ) ) 

  
if __name__ == '__main__':
  prog()
