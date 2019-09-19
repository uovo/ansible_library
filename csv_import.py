#!/usr/bin/env python

import csv
from ansible.module_utils.basic import *

def convert_csv(file):
    result = {"ansible_facts":{}}
    spreadsheet = {"csvimport":[]}
    try:
        with open(file) as csvfile:
            data = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in data:
                spreadsheet["csvimport"].append(row)
    except IOError:
        return (1, "Unable to process input file: %s (IOError)" % file)
    csvfile.close()

    result["ansible_facts"] = spreadsheet
    return (0, result)

def main():
    module = AnsibleModule(argument_spec = dict(
            src = dict(required=True, type='str')),
            check_invalid_arguments=False)

    returncode, response = convert_csv(module.params["src"])
    if returncode == 1:
        module.fail_json(msg=response)
    else:
        module.exit_json(**response)
    return returncode


if __name__ == '__main__':
    main()
