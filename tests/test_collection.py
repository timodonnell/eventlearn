#!/usr/bin/env python3

import random, shutil, pytest, os
from eventlearn import collection

def test_basic(tmpdir):
    c = collection.empty()
    assert len(c) == 0
    
    v1 = c.add_verb("foo", ["tag1", "tag2"])
    c.insert_multiple(
        [100],
        [v1],
        [5],
        [0.1])
    assert len(c) == 1
    
    v2 = c.add_verb("foobar", ["tag7", "tag2"], [])
    c.insert_multiple(
        [500],
        [v2],
        [7],
        [0])
    assert len(c) == 2
    
    c.insert_multiple(
        [50],
        [v2],
        [9],
        [1])
    assert len(c) == 3

    filename = tmpdir.strpath + "/eventlearn-test.h5"
    c.write(filename)
    print(c)

    c2 = collection.open(filename)
    assert len(c2) == 3
    assert (c2.events_df == c.events_df).all().all()
    assert c2.verb_info(v2).tags == set(["tag7", "tag2"])


