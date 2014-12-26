eventlearn
==========

feature extraction from irregularly-spaced timeseries

This is just getting started, and the API is going to change a lot.

The motivation for this is a clinical data mining application.

The idea is to have a very compact representation of a series of events, where
each event has:
 - a timestamp (uint32)
 - a "subject" (int32)
 - a "verb" (int32)
 - an optional value (float32)

In our clinical data analysis application, the "subject" is a patient, the
"verb" is an event that happens, such as admission, medication prescribed, or a
particular lab test result, and the "value" is an optional value associated
with the event, such as the numerical lab result value. We have hundreds of
millions of events, and we want to work with them in memory on a single node.

Given a series of events, at any point in time we want to be able to build a
fixed-length feature vector that reflects the state of a particular subject at
that time. This vector should summarize the preceeding events, and be usable as
features in a machine learning model.  For example, one element in that vector
might be the number of events of a particular verb that subject has had up to
that point. Another element might be the value for the most recent event of a
certain verb. Most of this is not implemented yet.

## Try it (not much here currently)
Install:
```
cd eventlearn
pip install .
```

Run tests:
```
py.test tests
```
