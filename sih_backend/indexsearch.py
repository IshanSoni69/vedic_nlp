#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 09:51:40 2022

@author: Soni, Ishan
"""

import pyluceneutils

from org.apache.lucene.util import QueryBuilder
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import FSDirectory
from timeutils import Stopwatch


def searchPhraseQuery(log, stdAnalyzer: StandardAnalyzer, indexDir: FSDirectory, queryString: str, searchAttributeName: str, hitsPerPage: int):
    # Initialize the JVM for Lucene
    # _ = pyluceneutils.initilaizeVM()
    hits = ""
    queryResponseTime = 0.0
    try:
        stopWatch = Stopwatch(start=True)
        queryBuilderObj = QueryBuilder(stdAnalyzer)
        queryObj = queryBuilderObj.createPhraseQuery(searchAttributeName, queryString)
        indexReader = DirectoryReader.open(indexDir)
        indexSearcher = IndexSearcher(indexReader)
        docs = indexSearcher.search(queryObj, hitsPerPage)
        hits = docs.scoreDocs
        stopWatch.stop()
        queryResponseTime = stopWatch.elapsed_seconds 
        log.info("Search for {0} yielded {1} results in {2} seconds.".format(queryString,len(hits),queryResponseTime))
    except Exception as e:
        log.error("Java error {0}".format(e.message()))
    finally:
        return queryResponseTime,hits