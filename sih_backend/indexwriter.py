#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 08:56:05 2022

@author: Soni, Ishan
"""

import lucene
import java

from java.io import File
from java.nio.file import Paths, Files
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import QueryBuilder
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher

import indexsearch
import pyluceneutils
# import loggingutils
# log = loggingutils.time_rotated_log()
# log.info("Running IndexWriter, Log Initialized")




def addDocToIndex(log, stdAnalyzer: StandardAnalyzer, indexDir: FSDirectory, indexWriter: IndexWriter, searchAttributeName: str, bookTitle: str, hymnChapterTitle: str, fileContents: str, hitsPerPage: int):
    doc = Document()
    #use a string field for values that shouldnt be tokenized and considered as a phrase
    doc.add(StringField("bookTitle", bookTitle, Field.Store.YES))
    doc.add(StringField("HymnChapterTitle", hymnChapterTitle, Field.Store.YES))
    count=0
    for line in fileContents.split("\n"):
        queryString = line
        queryResponseTime, searchHits = indexsearch.searchPhraseQuery(log, stdAnalyzer, indexDir, queryString, searchAttributeName, hitsPerPage)
        # Add line to Index if it does not exist
        if len(searchHits)==0:
            count+=1
            doc.add(StringField("lineNumber", str(count),Field.Store.YES))
            doc.add(TextField("lineContent", line.strip(), Field.Store.YES))
            indexWriter.addDocument(doc)
    log.info("Added {2} new lines to {0} : {1}".format(bookTitle,hymnChapterTitle,count))
        
        

def createIndexFromDocs(log, index_path: str, data_path: str, searchAttributeName: str, hitsPerPage: int):
    # Initialize the JVM for Lucene
    _ = pyluceneutils.initilaizeVM(log)
    stdAnalyzer = StandardAnalyzer()
    indexDir = FSDirectory.open(Paths.get(index_path))
    writerConfig = IndexWriterConfig(stdAnalyzer)
    indexWriter = IndexWriter(indexDir, writerConfig)
    
    filesList = File(data_path).listFiles()
    for txtFileDoc in filesList:
        fileName = txtFileDoc.getName()
        filePath = Paths.get(txtFileDoc.getPath())
        fileContents = java.lang.String(Files.readAllBytes(filePath),"UTF-8")
        fileNameComponents = fileName.split("_") 
        bookTitle = fileNameComponents[0]
        hymnChapterTitle = fileNameComponents[-1].split(".")[0]
        addDocToIndex(log, stdAnalyzer, indexDir, indexWriter, searchAttributeName, bookTitle, hymnChapterTitle, fileContents, hitsPerPage)
        
        
    indexWriter.close()
    return stdAnalyzer,indexWriter


# index_path = "index/combined_index/"
# data_path = "data/english/yajur_veda/"
# searchAttributeName = "lineContent"
# hitsPerPage = 20

# _,_ = createIndexFromDocs(log, index_path, data_path, searchAttributeName, hitsPerPage)
