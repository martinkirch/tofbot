# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Christophe-Marie Duquesne <chm.duquesne@gmail.com>
"""
Naive Bayesian classifier.

This was implemented from the explanation on
http://en.wikipedia.org/wiki/Naive_Bayes_classifier
"""

def product(iterable):
    """
    Returns the product of the elements of an iterable
    """
    res = 1
    for i in iterable:
        res *= i
    return res

class StorageBackend:
    """
    Storage backend for the classifier.
    """

    def add_match(self, c, f=''):
        """
        Increments the number of matchs between the class c and the
        feature f. If no feature is provided, increment the total number
        of matches for c.
        """
        raise NotImplementedError

    def nb_matches(self, c, f=''):
        """
        Returns the number of matches between the class c and the feature
        f. If no feature is provided, this should return the total number
        of matches for c.
        """
        raise NotImplementedError

    def classes(self):
        """
        Returns the available classes.
        """
        raise NotImplementedError

class SqliteBackend(StorageBackend):
    """
    Sqlite storage backend.
    """

    def __init__(self, db_file):
        try:
            import sqlite3
        except ImportError:
            raise ImportError, "You need sqlite3 to use this storage backend"
        import os.path
        if not os.path.exists(db_file):
            self.conn = sqlite3.connect(db_file)
            self.conn.text_factory = str
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE occurrences(
                    class TEXT,
                    feature TEXT,
                    occurrences INTEGER,
                    PRIMARY KEY(feature, class)
                    )
                """
            )
            self.conn.commit()
            cursor.close()
        else:
            self.conn = sqlite3.connect(db_file)
            self.conn.text_factory = str

    def add_match(self, c, f=''):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO occurrences
            VALUES (?, ?,
                COALESCE((
                    SELECT occurrences
                    FROM occurrences
                    WHERE class=? AND feature=?), 0) + 1
            )
            """, (c, f, c, f)
            )
        self.conn.commit()
        cursor.close()

    def nb_matches(self, c, f=''):
        res = 0
        cursor = self.conn.cursor()
        cursor.execute(
                """
                SELECT occurrences
                FROM occurrences
                WHERE class=? AND feature=?
                """, (c ,f)
                )
        l = list(cursor)
        if l:
            res = int(l[0][0])
        cursor.close()
        return res

    def classes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT class FROM occurrences")
        res = [row[0] for row in cursor]
        cursor.close()
        return res

class NaiveBayesClassifier:
    """
    A Bayes Classifier knows "features" (properties used to recognize) and
    "classes" (categories to classify a given set of properties).

    How to use it:

    1) provide it with a storage backend
    >>> import classifier
    >>> s = classifier.SqliteBackend("my_file")
    >>> c = classifier.NaiveBayesClassifier(s)

    2) train it with sets of features and their corresponding classes. The
    "train" method takes as input an iterable containing features, and the
    corresponding class.
    >>> c.train("I like".split(), "that's what she said")

    You provide any set of features, provided these are string: This means
    you could split a sentence in digrams rather than words.
    >>> c.train(["I like", "I", "like"], "that's what she said")

    3) use it to classify
    Once the classifier is trained, it can be used to classify. For a
    given set of features, it will returns an ordered list of classes
    along with their score (from the most probable to the least probable)
    >>> c.classify("I like".split())
    [(u"that's what she said", 0.3333333333333333)]

    Note:
    strings should be converted to utf8 when passed to the classifier.
    >>> s = s.decode(<previous encoding>).encode('utf8')
    """

    def __init__(self, storage_backend):
        """
        You can provide your own storage backend (it just need to
        implement the same interface as StorageBackend)
        """
        self.storage = storage_backend

    def train(self, features, c):
        """
        Trains the classifier: these features => this class
        """
        self.storage.add_match(c)
        for f in features:
            self.storage.add_match(c, f)

    def proba_c(self, c):
        """
        Returns P(C=c) after the training.
        """
        s = self.storage
        res = (float(s.nb_matches(c)) /
                sum([s.nb_matches(i) for i in s.classes()]))
        #print "P(%s) = %s" %(c, str(res))
        return res

    def proba_f_given_c(self, c, f):
        """
        Returns P(F=f | C=c) after the training.
        """
        s = self.storage
        cf_matches = s.nb_matches(c, f)
        if not cf_matches:
            res = 1.0/sum([s.nb_matches(i) for i in s.classes()])
        else:
            res = float(cf_matches)/s.nb_matches(c)
        #print "P(%s|%s) = %s" %(f, c, str(res))
        return res

    def classify(self, features):
        """
        Given a list of features, returns the most probable class
        """
        scores = []
        for c in self.storage.classes():
            scores.append(
                    (c, self.proba_c(c) * product(
                        [self.proba_f_given_c(c, f) for f in features]))
                    )
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
