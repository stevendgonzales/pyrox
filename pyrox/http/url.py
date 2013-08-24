import re

try:
    #import from python 2 stdlib
    from urlparse import urlparse
except ImportError:
    #import from python 3 stdlib
    from urllib.parse import urlparse


def parse_url(url):
    """
    Parses a url into a dictionary containing fields:
    scheme, netloc, path, params, query, fragment

    Example:
    >>>parse_url('http://pyrox-http.org:80/tenant/1234')
    {'scheme': 'http', 'netloc': 'pyrox-http.org:80', 'path': '/tenant/1234',
    'params': '', 'fragment': '', 'query': '', }
    """
    parsed = urlparse(url)
    return dict(parsed._asdict())


class UrlPathParser(object):
    """
    A utility class for parsing uri template variables
    from a list of compiled regex templates
    """

    def __init__(self):
        self.compiled_templates = list()

    def add_path_template(self, template):
        """
        Accepts a rfc6570 level 1 uri template, compiles the template
        into a regex pattern matcher, and adds the pattern matcher to
        list of compiled_templates
        """
        #validate template
        if not isinstance(template, str):
            raise TypeError('uri_template is not a string')
        if not template.startswith('/'):
            raise ValueError("uri_template must start with '/'")
        if '//' in template:
            raise ValueError("uri_template may not contain '//'")
        if template != '/' and template.endswith('/'):
            template = template[:-1]

        # Convert Level 1 var patterns to equivalent named regex groups
        expression_pattern = r'{([a-zA-Z][a-zA-Z_]*)}'
        escaped = re.sub(r'[\.\(\)\[\]\?\*\+\^\|]', r'\\\g<0>', template)
        pattern = re.sub(expression_pattern, r'(?P<\1>[^/]+)', escaped)
        pattern = r'\A' + pattern + r'\Z'

        #add the compiled regex to the list of compiled_templates
        self.compiled_templates.append(re.compile(pattern, re.IGNORECASE))

    def parse_template_vars(self, path):
        """
        Accepts the path component of a url, attempts to match it to
        an existing compiled_template.  If there is a match then a
        dictionary of the template fields and values is returned
        """
        for template in self.compiled_templates:
            match = template.match(path)
            if match:
                return match.groupdict()


if __name__ == '__main__':

    parsed_url = parse_url('http://pyrox-http.org:80/tenant/1234')

    path_parser = UrlPathParser()
    path_parser.add_path_template('/tenant/{tenant_id}')
    path_vars = path_parser.parse_template_vars(parsed_url['path'])
    print(path_vars)
    tenant_id = path_vars['tenant_id']
    print(tenant_id)
