def create_tag(name, indent_level=0, attr={}, value="{}", single_line=False):
    ''' Create a tag by name with value. set indent by indent_level.
        If the tag should be single line, then set single_line to True.
    '''
    indent = "    "*indent_level
    nl = "" if single_line else "\n"
    close_indent = "" if single_line else indent
    attr_str = ""
    for k, v in attr.items():
        attr_str += ' {}="{}"'.format(k, v)
    return "{indent}<{name}{attr_str}>{nl}{value}{nl}{close_indent}</{name}>".format(indent=indent, name=name, attr_str=attr_str, nl=nl, value=value, close_indent=close_indent)
