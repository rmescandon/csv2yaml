#!/usr/bin/env python3
#
# Copyright (C) 2020 Roberto Mier Escandon <rmescandon@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from argparse import ArgumentParser
from string import Template

OUTPUT_DEFAULT_NAME = 'csv2yaml_output'


def _parse_args(args):
    parser = ArgumentParser()
    parser.add_argument('csv',
                        help='Path to the file with the input data to create the output yaml file(s).'
                        'First line is taken as the parameter names to replace in the template')
    parser.add_argument('template',
                        nargs='?',
                        help='Path to the file with the template to use for creating the output yaml files.'
                             'parameters are replaced by values in every line of the input data')
    parser.add_argument('-e', '--ext',
                        default='yaml',
                        help='The extension to use for the output file names. Default: \'yaml\'')
    parser.add_argument('-o', '--output',
                        default='output',
                        help='The folder where generating the ouput yaml files. Default: \'output\'')
    parser.add_argument('-p', '--prefix',
                        default='',
                        help='The prefix to use for the output files names')
    parser.add_argument('-s', '--single',
                        dest='single_file',
                        action='store_true',
                        help='If wanted the output to be a single file where template replacement'
                        'is repeated once per input line. If this parameter is omitted'
                        'one yaml output file is created per input line, whose name is'
                        'based on the first value of every line. If filename matches an'
                        'existing one, another name is considered until finding an available one.')
    parser.add_argument('-sep', '--separator',
                        default=',',
                        help='The separator used to discriminate CSV file values in every line. Default: \',\'')

    # Show help if no parameter is provided
    if len(args) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args(args)


def _validate_args(args):
    if not os.path.exists(args.csv) or not os.path.isfile(args.csv):
        raise Exception('CSV file does not exist or is not a file')

    if args.template and (not os.path.exists(args.template) or not os.path.isfile(args.template)):
        raise Exception(
            'Provided template file does not exist or is not a file')

    if os.path.exists(args.output) and not os.path.isdir(args.output):
        raise Exception('Output file already exists but it is not a folder')


def _obtain_output_filename(base_name, output_folder, ext):
    '''Calculates a filename based on a certain one. If the file
    already exists, a counter is initialized and increased until
    finding an available name'''
    n = '{}.{}'.format(base_name, ext)
    c = 0
    while os.path.exists(os.path.join(output_folder, n)):
        c += 1
        n = '{}_{}.{}'.format(base_name, c, ext)
    return os.path.join(output_folder, n)


def _write_to_file(prefix, filename, folder, ext, data):
    '''Writes certain data to a file whose name is composed
    of a prefix + filename in a specific folder'''
    base_name = '{}{}'.format(prefix, filename)
    f = _obtain_output_filename(base_name, folder, ext)

    if os.path.isdir(f):
        raise Exception(
            'A subfolder with the same name of the output file {} is found'.format(f))

    if not os.path.isfile(f):
        with open(f, mode='w') as o:
            o.write(data)


def run(args):
    '''Executes the generation of yaml file(s)'''
    # Create the output folder if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Load the template
    template = None
    if args.template:
        with open(args.template, mode='r') as f:
            template = f.read()

    # Extract the headers from csv file
    headers = []
    with open(args.csv, mode='r') as f:
        line = f.readline().strip()
        if not line:
            raise Exception('Empty CSV')
        headers = line.split(args.separator)
        if not headers or len(headers) < 1:
            raise Exception('No headers found in CSV')

        # In case that template is not provided, let's create one taking the
        # headers as names of the config parameters to fill
        if not template:
            template = ''
            for h in headers:
                template += '{0}: {{ {0} }}'.format(h)

        t = Template(template)

        aggregated_data = ''
        line = f.readline().strip()
        while line:
            fields = line.split(args.separator)
            if len(fields) != len(headers):
                raise Exception(
                    'Found a line with not the same number of values than headers are')

            d = {}
            for i, h in enumerate(headers):
                d[h] = fields[i]

            # Replace template fields with current line values
            data = t.safe_substitute(d)

            # Write output file or cummulate results to write it all at the end
            if args.single_file:
                aggregated_data += data + os.linesep
            else:
                _write_to_file(args.prefix, fields[0].strip(
                    '\''), args.output, args.ext, data)

            line = f.readline().strip()

        if args.single_file:
            _write_to_file(args.prefix, OUTPUT_DEFAULT_NAME,
                           args.output, args.ext, aggregated_data)


def main():
    args = _parse_args(sys.argv[1:])
    _validate_args(args)
    run(args)


if __name__ == '__main__':
    main()
