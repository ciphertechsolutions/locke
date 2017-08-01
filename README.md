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

$ PYTHONPATH=. python3 apm/server.py
$ python3 apm/client.py big_file.exe
```

### TODO

Rewrtite plugins to use metaclasses?
