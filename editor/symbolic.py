
import sympy
from sympy.parsing.sympy_parser import parse_expr, \
  standard_transformations, convert_xor


class Sym:

  def __init__(self):
    self._transform = standard_transformations + (convert_xor,)
    self._xor = True
    self._simp = False

  #===========================
  #        properties 
  #===========================

  def simpParse(self,use):
    self._simp = use

  def powXOR(self,use):
    self._xor = use
    if use:  # symbol ^
      self._transform = standard_transformations + (convert_xor,)
    else:    # symbol **
      self._transform = standard_transformations

  #==========================
  #        internal
  #==========================

  def _parse(self, s):
    try:
      expr = parse_expr(s, evaluate=self._simp, transformations=self._transform)
      return True, expr
    except Exception as err:
      return False, err

  def _toString(self, expr):
    s = str(expr)
    if self._xor:
      s = s.replace('**','^')
    return s

  def _eval(self, s, fn):
    ok, res = self._parse(s)
    if not ok:
      return False, res
    expr = fn(res)
    return True, self._toString(expr)

  #==========================
  #          base
  #==========================

  def expand(self,s):
    return self._eval(s, sympy.expand)

  def factor(self,s):
    return self._eval(s, sympy.factor)

  def simplify(self,s):
    return self._eval(s, sympy.simplify)

  #==========================
  #      trigonometry 
  #==========================

  def trigExpand(self,s):
    return self._eval(s, sympy.expand_trig)

  def trigSimp(self,s):
    return self._eval(s, sympy.trigsimp)

  #==========================
  #        power 
  #==========================

  def powExpandExp(self,s):
    return self._eval(s, sympy.expand_power_exp)

  def powExpandBase(self,s):
    return self._eval(s, sympy.expand_power_base)

  def powSimp(self, s):
    return self._eval(s, sympy.powsimp)
#sym = Sym()
#print(sym.expand('a*(b+c)'))
