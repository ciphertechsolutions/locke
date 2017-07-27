apm
===

APM is a simple but scalable pattern matcher, providing the ability to scan files
for patterns of interest (POIs) declared as Python classes.

APM patterns can also contain weights, which can be used to describe the importance
of matches.

### Command-line usage

```bash
$ pip3 install click # click is needed for the CLI
$ python3 apm.py match big_file.exe
$ python3 apm.py weight big_file.exe
```
