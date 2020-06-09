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
import csv2yaml
import pytest
from tempfile import TemporaryDirectory

_TEST_ASSETS_PATH = '{}/assets'.format(os.path.dirname(__file__))


def test_require_csv():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    assert os.path.exists(csv_filename)


def test_require_csv_is_a_file():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    assert os.path.isfile(csv_filename)


def test_require_not_empty_csv():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'empty.csv')
    assert os.path.exists(csv_filename)
    args = csv2yaml._parse_args([csv_filename])

    with pytest.raises(Exception) as e:
        csv2yaml.run(args)
    assert 'Empty CSV' in str(e.value)


def test_require_template_path_exists():
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')
    assert os.path.exists(template_filename)


def test_require_template_is_a_file():
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')
    assert os.path.isfile(template_filename)


def test_single_file_generation():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')

    tmpdir = TemporaryDirectory()

    args = csv2yaml._parse_args([csv_filename, template_filename, '-s', '-o', tmpdir.name])
    csv2yaml.run(args)

    assert os.path.exists(os.path.join(tmpdir.name, '{}.yaml'.format(csv2yaml.OUTPUT_DEFAULT_NAME)))


def test_single_file_generation_with_prefix():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')

    tmpdir = TemporaryDirectory()

    prefix = 'dafak'

    args = csv2yaml._parse_args([csv_filename, template_filename, '-s', '-o', tmpdir.name, '-p', prefix])
    csv2yaml.run(args)

    assert os.path.exists(os.path.join(tmpdir.name, '{}{}.yaml'.format(prefix, csv2yaml.OUTPUT_DEFAULT_NAME)))


def test_single_file_generation_when_already_exists():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')

    tmpdir = TemporaryDirectory()

    # create empty file
    with open(os.path.join(tmpdir.name, '{}.yaml'.format(csv2yaml.OUTPUT_DEFAULT_NAME)), 'w'):
        pass

    args = csv2yaml._parse_args([csv_filename, template_filename, '-s', '-o', tmpdir.name])
    csv2yaml.run(args)

    # Verify that two different outputs have been created
    assert os.path.exists(os.path.join(tmpdir.name, '{}.yaml'.format(csv2yaml.OUTPUT_DEFAULT_NAME)))
    assert os.path.exists(os.path.join(tmpdir.name, '{}_1.yaml'.format(csv2yaml.OUTPUT_DEFAULT_NAME)))


def test_single_file_generation_with_blank_separator():
    blank_separator_filename = os.path.join(_TEST_ASSETS_PATH, 'blank_separator.csv')
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')

    # run with blanks
    tmpdir1 = TemporaryDirectory()
    args = csv2yaml._parse_args([blank_separator_filename, template_filename, '-s', '--sep', ' ', '-o', tmpdir1.name])
    csv2yaml.run(args)

    # run without blanks
    tmpdir2 = TemporaryDirectory()
    args = csv2yaml._parse_args([csv_filename, template_filename, '-s', '-o', tmpdir2.name])
    csv2yaml.run(args)

    # compare
    with open(os.path.join(tmpdir1.name, '{}.yaml'.format(csv2yaml.OUTPUT_DEFAULT_NAME)), 'r') as f1:
        with open(os.path.join(tmpdir2.name, '{}.yaml'.format(csv2yaml.OUTPUT_DEFAULT_NAME)), 'r') as f2:
            content1 = f1.read()
            content2 = f2.read()
            assert content1 == content2


def test_single_file_generation_to_a_different_extension():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')

    tmpdir = TemporaryDirectory()

    ext = 'json'

    args = csv2yaml._parse_args([csv_filename, template_filename, '-s', '-o', tmpdir.name, '-e', ext])
    csv2yaml.run(args)

    assert os.path.exists(os.path.join(tmpdir.name, '{}.{}'.format(csv2yaml.OUTPUT_DEFAULT_NAME, ext)))


def test_multiple_file_generation():
    csv_filename = os.path.join(_TEST_ASSETS_PATH, 'test.csv')
    template_filename = os.path.join(_TEST_ASSETS_PATH, 'test.template')

    tmpdir = TemporaryDirectory()

    args = csv2yaml._parse_args([csv_filename, template_filename, '-o', tmpdir.name])
    csv2yaml.run(args)

    names = []
    with open(csv_filename, mode='r') as f:
        line = f.readline().strip()
        line = f.readline().strip()
        while line:
            n = line[:line.index(',')]
            names.append(n)
            line = f.readline()

    for n in names:
        assert os.path.exists(os.path.join(tmpdir.name, '{}.yaml'.format(n)))
