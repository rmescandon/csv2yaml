# CSV2YAML

Converts a csv + template in an yaml output file 

## What is this

Another cli tool to use in Ubuntu like OS supporting snaps

Provide a csv file whose first line is comprised of certain headers
that will be considered the placeholders in a template
Every line in the csv, from second onwards, is a data line.
Provide the template with placeholders in the format $thisisaplaceholder.
This tool replaces placeholders by data of every csv file line. The
output are a bunch of yaml files, one per line. Or could it be all
included in a single yaml file, repeating same structure per csv line


## How it works

Say you have a CSV file, whose content is

```
uno,dos,tres,catorce
value1,value2,value3,value4
value5,value6,value7,value8
```

and you want to build certain yaml files, whose content is:

```yaml
label-for-value: ONEVALUE
    label-for-another-value: ANOTHERVALUE
    lable-for-array:
        - ANOTHERONE
        - THELASTONE
```
but replacing the values by the ones in the csv file, so that an 
individual yaml output file is generated per data in every line
of the csv file.

You can define a template to be used with the provided csv like this:
```yaml
label-for-value: $uno
    label-for-another-value: $dos
    lable-for-array:
        - $tres
        - $catorce
```

Those placeholders with the dollar symbol will be replaced by csv 
values of every line. Then, you get two files:

```yaml
label-for-value: value1
    label-for-another-value: value2
    lable-for-array:
        - value3
        - value4
```

```yaml
label-for-value: value5
    label-for-another-value: value6
    lable-for-array:
        - value7
        - value8
```

Or maybe you prefer having both files in a single one:

```yaml
label-for-value: value1
    label-for-another-value: value2
    lable-for-array:
        - value3
        - value4
label-for-value: value5
    label-for-another-value: value6
    lable-for-array:
        - value7
        - value8
```

easy!. Don't you think so?. 

## How can I install it

Install it as a snap:

```sh
snap install csv2yaml
```

and you're good to go

## How can I use it

The very basic execution needs a path to a csv file and a path to a template:

```sh
csv2yaml path/to/input.csv path/to/template
```

if you prefer generating only one single output file, you can use the *-s* flag:

```sh
csv2yaml path/to/input.csv path/to/template -s
```

## What other parameters can I provide?

If you don't provide any argument, the help is shown:

Positional Arguments:
* csv: a path to a csv file acting as input data. First row defines the headers
    to use as placeholders in the template
* template: a path to a yaml file acting as template with placeholders. These
    placeholders match the names in the first row of the csv file

Optional Arguments:
* -e, --ext: the extension of the files to create (default: yaml)
* -o, --output: the folder where leaving the resultant files (default: output)
* -p, --prefix: a prefix for every name of every generated file
* -s, --single: a single output file is generated as the addition of every line
    merged with the template
* -sep, --separator: the separator to use for splitting the values of the csv file (Default: ,)

## Thigs to consider

You could generate other format different from yaml. That's depending on what
the template contains

Every generated files takes the name of the first values in the related csv row.

In case you prefer to generate a single output file, that takes the name _csv2yaml_output.yaml_


