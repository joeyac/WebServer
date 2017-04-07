# -*- coding: utf-8 -*-
import os
from zipfile import ZipFile
from django.utils.html import format_html


# return 64 bit hash sum
def get_dir_hash(directory):
    import checksumdir
    if os.path.exists(directory):
        return checksumdir.dirhash(directory, 'sha256')
    else:
        return -1


# return zip file path
def zip_test_case(test_case_dir):
    path = os.path.join('/tmp', 'a_temp_zip_file')
    zipfile = ZipFile(path, 'w')
    os.chdir(test_case_dir)
    for parent, dir_names, file_names in os.walk(os.getcwd()):
        for filename in file_names:
            zipfile.write(filename)
    zipfile.close()
    return path


def get_status_html(value):
    value = str(value).lower().title()
    if value == 'Accepted':
        return format_html('<span class="ac">{str}</span>'.format(str=value))
    elif value == 'Compile Error' or value == 'Compilation Error':
        return format_html('<span class="ce">{str}</span>'.format(str=value))
    elif 'error' in value.lower() or 'wrong answer' in value.lower() or 'exceed' in value.lower():
        return format_html('<span class="er">{str}</span>'.format(str=value))
    else:
        return format_html('<i class="fa fa-refresh fa-spin"></i> <span class="wt">{str}</span>'.format(str=value))
# def get_status_html(value):
#     value = str(value).lower().title()
#     if value == 'Waiting' or 'running' in value.lower() or 'queuing' in value.lower():
#         return format_html('<i class="fa fa-refresh fa-spin"></i> <span class="wt">{str}</span>'.format(str=value))
#     elif value == 'Accepted':
#         return format_html('<span class="ac">{str}</span>'.format(str=value))
#     elif value == 'Compile Error':
#         return format_html('<span class="ce"><a>{str}</a></span>'.format(str=value))
#     else:
#         return format_html('<span class="er">{str}</span>'.format(str=value))
