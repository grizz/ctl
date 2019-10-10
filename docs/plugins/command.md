# Command Plugin

Allows you to configure and run custom shell commands.

## Example: Starting off simple

In this first example we will create a command that echos a static
string into a text file.

```yaml
{!examples/plugins/command/echo/Ctl/config.yaml!}
```

### Run the command

The command will be exposed as an operation to the ctl cli

```sh
ctl echo

[2019-10-09 07:55:34,916] [usage] ran command: `echo`
```

Then verify that it did a thing

```sh
cat example.txt

this is an example
```

## Example: Custom arguments

Taking the example from above we can make it a tiny bit more useful, and give some arguments to our command

```yaml
{!examples/plugins/command/better_echo/Ctl/config.yaml!}
```

We can check that our arguments are in place by running the `--help` function

```sh
ctl better_echo --help

usage: ctl better_echo [-h] [--working-dir WORKING_DIR] [content] [output]

positional arguments:
  content
  output                echo to this file

optional arguments:
  -h, --help            show this help message and exit
  --working-dir WORKING_DIR
                        set a working directory before running the commands
```

Looking good, so now we run our improved echo command like this

```sh
ctl better_echo "marginally more useful" better_example.txt
```

## Usage

```sh
usage: ctl test_chain [-h] [--end END] [--start START]

optional arguments:
  -h, --help     show this help message and exit
  --end END      stop at this stage
  --start START  start at this stage
```
