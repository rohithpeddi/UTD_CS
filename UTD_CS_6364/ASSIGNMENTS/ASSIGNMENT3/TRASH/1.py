def unify(x, y, s={}):
    """
    [Figure 9.1]
    Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. Expr('x')), constants, lists, or Exprs.
    >>> unify(x, 3, {})
    {x: 3}
    """
    if s is None:
        return None
    elif x == y:
        return s
    elif is_variable(x):
        return unify_var(x, y, s)
    elif is_variable(y):
        return unify_var(y, x, s)
    elif isinstance(x, Expr) and isinstance(y, Expr):
        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str):
        return None
    elif issequence(x) and issequence(y) and len(x) == len(y):
        if not x:
            return s
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    else:
        return None


def is_variable(x):
    """A variable is an Expr with no args and a lowercase symbol as the op."""
    return isinstance(x, Expr) and not x.args and x.op[0].islower()


def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    elif x in s:
        return unify(var, s[x], s)
    elif occur_check(var, x, s):
        return None
    else:
        new_s = extend(s, var, x)
        cascade_substitution(new_s)
        return new_s


def occur_check(var, x, s):
    """Return true if variable var occurs anywhere in x
    (or in subst(s, x), if s has a binding for x)."""
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif isinstance(x, Expr):
        return (occur_check(var, x.op, s) or
                occur_check(var, x.args, s))
    elif isinstance(x, (list, tuple)):
        return first(e for e in x if occur_check(var, e, s))
    else:
        return False


unify(x,3,{})