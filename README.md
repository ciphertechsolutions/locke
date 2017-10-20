Locke
=====

Locke is a refactoring and remodeling of [Balbuzard](https://github.com/decalage2/balbuzard).

### Installation

Requires Python3.5 + 

Requires Time. A lot of time. Or a Super Computer (prefer a Quantum Computer)

Requires apm server to be running. Just cd to apm and run PYTHONPATH=. apm/server/tcp_server.py

### Usage

Locke is simple to use. Just run
``` bash
python3 locke.py --help
```
After each command, you can run ``--help`` to get more information about the command.

Some basic commands are:
```
Usage: locke.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  be verbose
  --help         Show this message and exit.

Commands:
  crack       Use patterns of interest to crack the...
  patterns    List all patterns known by Locke.
  search      Search for patterns of interest in the...
  transforms  List all transformations known by Locke.
```

For a basic search just run 
```
python3 locke.py search <filename>
```
You can add in `` --csv <outputName>`` to save the result as a csv

Decoding a file have some parameters that may be of interest:
```
Usage: locke.py crack [OPTIONS] FILENAME

  Use patterns of interest to crack the supplied files.

Options:
  -l, --level INTEGER    Select transformers with level 1, 2, or 3 and below
  -o, --only INTEGER     Only use transformers on that specific level
  -n, --name TEXT        A list of transformer classes to use in quotes and is
                         commas separated
  -k, --keep INTEGER     How many transforms to saveafter stage 1
  -s, --save INTEGER     How many transforms to saveafter stage 2
  -z, --zip_file         Mark this fileas a zip file. Use --password to enter
                         zip password
  --password TEXT        Only works if -z is set. Allows input of password for
                         zip file
  --no-save              Don't save result to disk
  -v, --verbose INTEGER  Set the verbose level Valid inputs are 0 - 2 (lowest
                         output to highest). Note that -v 2 is not human
                         friendly
  --help                 Show this message and exit.

```

To start a basic start with all the transformers (from level 1 - 3), run ``python3 locke.py crack <filename>``
This will decode the files, search each decoded instance and save the top 10 scoring instance to disk

To adjust how many files to keep/save, enter a number after ``-k`` or ``-s``. The lower the number,
the fast the program will run, but you will be limiting your results.

To select what transformation to run, use either ``-l``, ``-o``, or ``-n`` command. There is an order of
precedence. Only one of the value will be used to filter the transformers list. The order is as follow:
``Name > Only > Select``

For example if you run the script with ``-n transformxor -l 2 -o 1``, only the Transformer TransformXOR will
be applied to the file as name is the highest precedence; the level and only option will be disregarded. 
Likewise, if you run ``-l 2 -o 1``, only Transformers on level 1 will be run as only have a higher precedence 
than level.

To select more than one Transformer by name, wrap the list in quotes and separate each Transformers by a comma.
EX: ``--name "transformxor, transformadd, transformsub"``

This program also support decoding files inside a zip. Run with ``-z`` to mark the file as a zip. If the zip is
password encrypted, you can supply the password by using the ``--password <password>`` option. The script
will attempt to read the zip and list the files available and ask which files do you want to decode (if there are
more than one files).


For a list of all available Transformers, run ``python3 locke.py transforms``.

For a list of all available Patterns, run ``python3 locke.py patterns``.
apm
===

APM is a simple but scalable pattern matcher, providing the ability to scan files
for patterns of interest (POIs) declared as Python classes.

APM patterns can also contain weights, which can be used to describe the importance
of matches.

### Command-line usage

```bash
$ pip3 install click # click is needed for the CLI
$ pip3 install msgpack-python # msgpack is needed for client/server communication

$ PYTHONPATH=. python3 apm/server/tcp_server.py
$ PYTHONPATH=. python3 apm/client/tcp_client.py big_file.exe
```

### TODO

Rewrtite plugins to use metaclasses?
