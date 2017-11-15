Locke
=====

Locke is a refactoring and remodeling of [Balbuzard](https://github.com/decalage2/balbuzard).
Locke was a refactoring of Balbuzard to port the code to Python3 as well as 
increase its overall performance.
### Installation

Requires Python3

##### From source
```
python3 setup.py install
```
##### pip install
```
pip3 install --index-url https://test.pypi.org/simple/ locke
```

Locke will be installed into your path and should be able to be run like any
other executable in your path. 

### Usage

Locke is simple to use. Just run:
```
locke --help
```

#### Quickstart
With a given ``<filename>`` run the following commands:

```
locke search <filename>
```
This should show you some patterns found within the provided file without doing
any transformations to find encoded data.

```
locke crack <filename>
```
This should take under a minute to process (depends on the filesize). This will 
go through all the stage 1 and stage 2 transformations and stage 1 of the 
patterns to find any matches. This will also save the transformed file for 
the top 10 results.

To get more information about the matches either run:

```
locke crack -v 1 <filename>
``` 
(this will rerun everything and give you detailed output on the top 10 matches)
or run:
```
locke search <transformed_filename>
``` 
(this will search the provided transformed file for patterns and output 
detailed information)
#### Commands
After each command, you can run ``--help`` to get more information about the command.

Some basic commands are:
```
Usage: locke [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  be verbose
  --help         Show this message and exit.

Commands:
  crack       Use patterns of interest to crack the...
  patterns    List all patterns known by Locke.
  search      Search for patterns of interest in the...
  transforms  List all transformations known by Locke.
```
##### patterns
Usage statement:
```
locke patterns --help
Usage: locke patterns [OPTIONS]

  List all patterns known by Locke.

Options:
  --help  Show this message and exit.
```
##### search
Usage statement:
```
locke search --help
Usage: locke search [OPTIONS] [FILES]...

  Search for patterns of interest in the supplied files.

Options:
  --csv TEXT  output results as CSV
  --help      Show this message and exit.
```
For a basic search just run 
```
locke search <filename>
```
You can add in `` --csv <outputName>`` to save the result as a csv

##### transforms
Usage statement:
```
locke transforms --help
Usage: locke transforms [OPTIONS]

  List all transformations known by Locke. Also generate a new transforms.db
  and test algorithm duplications.

Options:
  -l, --level INTEGER  Select transformers with level 1, 2, or 3 and below
  -o, --only INTEGER   Only use transformers on that specific level
  -n, --name TEXT      A list of transformer classes to use in quotes and is
                       commas separated
  -t, --test           test transformations for simplification
  -g, --generate       generate transforms database
  --help               Show this message and exit.
```

For the stage 1 and 2 transforms Locke uses a generated database to increase the
performance of the overall system. When adding new stage 1 and 2 algorithms you
must run the ``-g`` option to regenerate the database.

##### crack
Usage statement:
```
locke crack --help
Usage: locke crack [OPTIONS] FILENAME

  Use patterns and transformations of interest to crack the supplied files.

Options:
  -l, --level INTEGER    Select transformers with level 1, 2, or 3 and below
  -o, --output TEXT      Output directory for transformed files
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

To start a basic start with all the transformers (from level 1 - 3), run ``locke crack <filename>``
This will decode the files, search each decoded instance and save the top 10 scoring instance to disk

To adjust how many files to keep/save, enter a number after ``-k`` or ``-s``. The lower the number,
the faster the program will run, but you will be limiting your results.

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

### Differences made to Locke from Balbuzard
- Uses Python 3 instead of 2
- Multiprocessed for faster execution
- Dedups translation alphabets
- With the dedupped translations you won't get the same results for two separate algorithms that are functionally equivalent
- Preprocesses the generation of the translation alphabets into a database for stage1

### TODO
- Want to configure the weights for the patterns to make the tool even more accurate.
- If needed, make locke truly an expandable distributed process.
- Testing on multiple samples of different sizes to see where performance and accuracy enhancement can be made.
