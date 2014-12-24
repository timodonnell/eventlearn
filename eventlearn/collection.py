import collections
import numpy, pandas, h5py

def open(filename):
    with pandas.HDFStore(filename) as store:
        return Collection(store["events"], store["metadata"])

def empty():
    def empty_array(dtype):
        return numpy.array([], dtype=dtype)
    events_df = pandas.DataFrame({
        'when': empty_array(numpy.int32),
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
        num = len(self.metadata_df)
        if categorical_values is not None:
            categorical_values = dict(categorical_values)
        self.metadata_df.ix[num] = [name, set(tags), categorical_values]
        return num

    def verb_info(self, num):
        return self.metadata_df.ix[num]

    def insert_df(self, new_events_df):
        self.events_df = self.events_df.append(
            new_events_df,
            ignore_index=True)
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
 
        
