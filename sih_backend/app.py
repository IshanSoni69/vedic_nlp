#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:27:07 2022

@author: Soni, Ishan
"""

import lucene
import java

from java.io import File
from java.nio.file import Paths, Files
import loggingutils
import indexwriter, indexsearch
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import FSDirectory
log = loggingutils.time_rotated_log()
log.info("Running IndexWriter, Log Initialized")



index_path = "index/combined_index/"
data_path = "data/english/yajur_veda/"
# Column Name in the storage, each line of vedic chapters will be considered as unit of storage
searchAttributeName = "lineContent"
# This can be varied to get max hits per page to be returned in a search
hitsPerPage = 20

# Uncomment the following for indexing new content also change the data and index path variables suitably
_,_ = indexwriter.createIndexFromDocs(log, index_path, data_path, searchAttributeName, hitsPerPage)

sample_search_query = "agni"

stdAnalyzer = StandardAnalyzer()
indexDir = FSDirectory.open(Paths.get(index_path))
writerConfig = IndexWriterConfig(stdAnalyzer)
indexWriter = IndexWriter(indexDir, writerConfig)
queryResponseTime, queryHits = indexsearch.searchPhraseQuery(log, stdAnalyzer, indexDir, sample_search_query, searchAttributeName, hitsPerPage)
indexWriter.close()
log.info("Query : {0} :: with response time: {1} seconds and results count:{2}".format(sample_search_query,queryResponseTime,len(queryHits)))