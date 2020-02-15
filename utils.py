import re


def build_route_regexp(path):
    named_groups = lambda match: f'(?P<{match.group(1)}>[a-zA-Z0-9_-]+)'

    regex_str = re.sub(r'{([a-zA-Z0-9_-]+)}', named_groups, path)
    return re.compile(f'^{regex_str}$')