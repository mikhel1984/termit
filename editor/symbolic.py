# Wrapper for the parser and symbolical operations
# of the sympy module

import sympy
from sympy.parsing.sympy_parser import parse_expr, \
  standard_transformations, convert_xor

class Sym:
  """Interface for symbolical operations"""

  def __init__(self):
    self._transform = standard_transformations + (convert_xor,)
    self._xor = True
    self._simp = False

  # ====== properties ========

  def simpParse(self,use):
    """Simplify expression during the parsing"""
    self._simp = use

  def powXOR(self,use):
    """Use '^' as a power symbol"""
    self._xor = use
    if use:  # symbol ^
      self._transform = standard_transformations + (convert_xor,)
    else:    # symbol **
      self._transform = standard_transformations

  # ====== internal ========

  def _parse(self, s):
    """Get sympy expression from the string"""
    try:
      expr = parse_expr(s, evaluate=self._simp, transformations=self._transform)
      return True, expr
    except Exception as err:
      return False, err

  def _toString(self, expr):
    """Convert expression to string"""
    s = str(expr)
    if self._xor:
      s = s.replace('**','^')
    return s

  def _eval(self, s, fn):
    """Parse string and apply function"""
    ok, res = self._parse(s)
    if not ok:
      return False, res
    expr = fn(res)
    return True, self._toString(expr)

  def _eval_arg(self, s, fn, arg):
    """Parse string and apply function with additional parameter"""
    ok, res = self._parse(s)
    if not ok:
      return False, res
    expr = fn(res, arg)
    return True, self._toString(expr)

  def subs(self, s, a, b):
    """Parse string and substitute variable"""
    ok, res = self._parse(s)
    if not ok:
      return False, res
    expr = res.subs(a,b)
    return True, self._toString(expr)

  def evalf(self, s):
    """Parse string and evaluate float value"""
    ok, res = self._parse(s)
    if not ok:
      return False, res
    expr = res.evalf()
    return True, self._toString(expr)

  # ======= base ===========

  def expand(self,s):
    """Expand expression"""
    return self._eval(s, sympy.expand)

  def factor(self,s):
    """Factorise expression"""
    return self._eval(s, sympy.factor)

  def simplify(self,s):
    """Apply all avilable simplifications"""
    return self._eval(s, sympy.simplify)

  def collect(self, s, arg):
    """Collect common powers"""
    return self._eval_arg(s, sympy.collect, arg)

  # ===== trigonometry ======

  def trigExpand(self,s):
    """Expand trigonometric expression"""
    return self._eval(s, sympy.expand_trig)

  def trigSimp(self,s):
    """Simplify trigonometric expression"""
    return self._eval(s, sympy.trigsimp)

  # ======= power ===========

  def powExpandExp(self,s):
    """Expand power expression"""
    return self._eval(s, sympy.expand_power_exp)

  def powExpandBase(self,s):
    """Expand power base"""
    return self._eval(s, sympy.expand_power_base)

  def powSimp(self, s):
    """Simplify expression with powers"""
    return self._eval(s, sympy.powsimp)

  # ===== rational ==========

  def cancel(self,s):
    """Get standard canonical form of rational function"""
    return self._eval(s, sympy.cancel)

  def apart(self,s):
    """Partial fractional decomposition"""
    return self._eval(s, sympy.apart)

  # ==== logarithm ==========

  def logExpand(self,s):
    """Expand logarithm expression"""
    return self._eval(s, sympy.expand_log)

  def logCombine(self,s):
    """Combine logarithm expression"""
    return self._eval(s, symb.logcombine)
