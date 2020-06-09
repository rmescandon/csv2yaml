# CSV2YAML

Converts a csv + template in an yaml output file 

## What is this

Provide a csv file whose first line is comprised of certain headers
that will be considered the placeholders in a template
Every line in the csv, from second onwards, is a data line.
Provide the template with placeholders in the format $thisisaplaceholder.
This tool replaces placeholders by data of every csv file line. The
output are a bunch of yaml files, one per line. Or could it be all
included in a single yaml file, repeating same structure per csv line
