def make_function(var_names, expression, environment=globals()):
    args = ''
    for n in var_names:
        args = args + "," + n
    return eval("lambda " + args[1:] + ": " + expression + ")", environment)
