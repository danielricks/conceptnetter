
# conceptnetter

This code provides an interface for ConceptNet 5 in Python.

## Requirements

A copy of ConceptNet 5 as a comma-separated values file (.csv) is required. This is available [here](http://conceptnet5.media.mit.edu/downloads/current/conceptnet5_flat_csv_5.4.tar.bz2).

Move to the conceptnetter directory and run ConceptNetter.py:

```python
python conceptNetter.py
```

This will truncate the data to only use the English langauge assertions found in the ConceptNet 5 database.

## Usage

This code is set up to run in Python. Example commands are below.

```python
import conceptnetter.conceptNetter as cn
c = cn.ConceptNetter()
c.look_up_words('dog')
c.get_parts('mailbox')
c.get_related_words('door')
c.get_hypernyms('door')
```

