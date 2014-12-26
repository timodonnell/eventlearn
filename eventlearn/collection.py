import collections
import numpy, pandas, humanize

def open(filename):
    with pandas.HDFStore(filename) as store:
        return Collection(store["events"], store["metadata"])

def empty():
    def empty_array(dtype):
        return numpy.array([], dtype=dtype)
    events_df = pandas.DataFrame({
        'when': empty_array(numpy.uint32),
        'verb': empty_array(numpy.int32),
        'subject': empty_array(numpy.int32),
        'value': empty_array(numpy.float32),
    })
    metadata_df = pandas.DataFrame({
        'verb': empty_array(numpy.object),
        'tags': empty_array(numpy.object),
        'categorical_values': empty_array(numpy.object),
    })
    return Collection(events_df, metadata_df)

class Collection(object):
    def __init__(self, events_df, metadata_df):
        self.events_df = events_df
        self.metadata_df = metadata_df
        self.unsorted = True

    def sort(self):
        if self.unsorted:
            self.events_df.sort(["when"], inplace=True) 
        self.unsorted = False

    def write(self, filename):
        self.sort()
        with pandas.get_store(filename, mode='w') as store:
            store.put("events", self.events_df)
            store.put("metadata", self.metadata_df)

    def add_verb(self, name, tags=set(), categorical_values=None):
        num = len(self.metadata_df) + 1
        if categorical_values is not None:
            categorical_values = list(categorical_values)
        self.metadata_df.ix[num] = [name, set(tags), categorical_values]
        return num

    def verb_info(self, num):
        return self.metadata_df.ix[num]

    def insert_df(self, new_events_df):
        df = pandas.DataFrame(new_events_df)
        if df.when.dtype == "M8[ns]":
            # Convert pandas 64-bit datetime to unix 32-bit timestamp.
            df.when = df.when.map(lambda x: x.value / 1e9).astype(numpy.uint32)
        for column in self.events_df.columns:
            df[column] = df[column].astype(self.events_df.dtypes[column])
        self.events_df = self.events_df.append(df, ignore_index=True)
        self.unsorted = True
        
    def insert_multiple(self, when, verb, subject, value=None):
        df = pandas.DataFrame({
                "when": when,
                "verb": verb,
                "subject": subject,
                "value": value})
        self.insert_df(df)

    def __len__(self):
        return len(self.events_df)

    def __str__(self):
        return repr(self)
 
    def __repr__(self):
        nbytes = sum(self.events_df[column].nbytes
            for column in self.events_df.columns)
        return "<Collection at 0x%0x: %d events of %d verbs [%s]>" % (
            id(self),
            len(self.events_df),
            len(self.metadata_df),
            humanize.naturalsize(nbytes))
        
