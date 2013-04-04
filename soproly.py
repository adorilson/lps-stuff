#! /usr/bin/python3

# coding: utf-8

import logging as log
log.basicConfig(
    level = log.INFO,
    format = '%(message)s'
)

import os
import shutil
import sys
sys.path.append('.')

from subprocess import call
from lxml import etree

import configspl


def setup_project(product):
    global confs 
    confs = {'product': product}
    log.info("Creating project to %(product)s product." % confs)
    android = configspl.sdkdir + "/tools/android "
    # These acitivity and package params will be rewrite
    params = "create project --target 1 --name %(product)s \
--path ../%(product)s --activity MainActivity \
--package br.ufrn.dimap.%(product)s" % confs
    log.info(android + params)
    os.system(android + params)
    shutil.rmtree("../%(product)s/src/br/ufrn" % confs)
    
    files = ['.classpath', '.project', 'AndroidManifest.xml']
    for f in files:
        params = {'file': f, 'product': confs['product']}
        copiar = 'cp ./%(file)s ../%(product)s/' % params
        os.system(copiar)
    
    # Changes in .project file
    tree = etree.parse("../%(product)s/.project" % confs)
    name = tree.find('name')
    name.text = confs['product']
    file1 = open("../%(product)s/.project" % confs, 'wb')
    xml = [b'<?xml version="1.0" encoding="UTF-8"?>\n'] + etree.tostringlist(tree)
    file1.writelines(xml)
    file1.close()
    
    # Changes in AndroidManifest.xml file
    tree = etree.parse("../%(product)s/AndroidManifest.xml" % confs)
    root = tree.getroot()
    root.attrib['package'] += '.' + confs['product']
    file1 = open("../%(product)s/AndroidManifest.xml" % confs, 'wb')
    xml = [b'<?xml version="1.0" encoding="UTF-8"?>\n'] + etree.tostringlist(tree)
    file1.writelines(xml)
    file1.close()

def add_resfiles(files):
    log.info('Copying resource files')
    for file_ in files:
        log.info('Copying %s' % file_)
        new_path = file_[:file_.rfind('/')+1]
        new_dir = '../%(product)s/res/' % confs +'%s' % new_path
        mkdir = 'mkdir -p %s' % new_dir 
        os.system(mkdir)
        cmd = 'cp res/' + file_ + ' ' + new_dir
        os.system(cmd)

def main_activity():
    pass
    # copiar arquivo .java
    # atualizar AndroidManifest
    # atualizar res/main.xml

def fix_packages(path, file_):
    full_file = path + '/' + file_
    
    if full_file in fixed_imports:
        return
    
    data = open(full_file).read().\
            replace(configspl.DEFAULT_SRC_DIR.replace('/', '.')[:len(configspl.DEFAULT_SRC_DIR)-1],
                    configspl.DEFAULT_SRC_DIR.replace('/', '.') + '%(product)s' % confs)
    o = open(path + '/' + file_,"w")
    o.writelines(data)
    o.close()
    fixed_imports.append(full_file)

def fix_files(path):
    log.info('Fixing the file''s packages')
    for file_ in os.listdir(path):
        fix_packages(path, file_)

def add_srcfiles(files):
    log.info('Copying source files')
    for file_ in files:
        log.info('Copying %s' % file_)
        new_path = file_[:file_.rfind('/')+1]
        
        new_dir = '../%(product)s/src/' % confs +'%s' % new_path
        new_dir = new_dir.replace(configspl.DEFAULT_SRC_DIR,
                                    configspl.DEFAULT_SRC_DIR + '/%(product)s/' % confs)
        log.info('New dir = %s' % new_dir)
        mkdir = 'mkdir -p %s' % new_dir 
        os.system(mkdir)
        cmd = 'cp src/' + file_ + ' ' + new_dir
        os.system(cmd)
        fix_files(new_dir)

def add_libfiles(files):
    log.info('Copying library files')
    for file_ in files:
        log.info('Copying %s' % file_)
        new_dir = '../%(product)s/libs/' % confs
        cmd = 'cp libs/' + file_ + ' ' + new_dir
        os.system(cmd)

def add_feature(feature):
    log.info('Add the %s' % (feature))
    log.info(configspl.features[feature])
    params = configspl.features[feature]
    if 'srcfiles' in params:
        add_srcfiles(params['srcfiles'])
    if 'resfiles' in params:
        add_resfiles(params['resfiles'])
    if 'libfiles' in params:
        add_libfiles(params['libfiles'])

FEATURE_BEGIN = 'FEATURE BEGIN'
FEATURE_END = 'FEATURE END'

def filter_by_features(features):
    
    def filter_xml(path_):
        for path in [path_]:
            print(path)
            file_ = open(path).readlines()
            filtered_file = []
            len_file = len(file_)
            i = 0
            while i<len_file:
                line = file_[i]
                if not FEATURE_BEGIN in line.strip():
                    filtered_file.append(line)
                else:
                    feature = line[line.find(' ')+1: line.rfind(' ')]
                    feature = feature[feature.rfind(' ')+1:].strip()
                    log.info('Feature %s found' % feature)
                    log.info('FEATURE = ' + feature)
                    print(features)
                    while True:
                        if feature in features:
                            filtered_file.append(line)
                            log.info('Feature in product')
                        else:
                            log.info('Product without feature')
                        i = i+1
                        line = file_[i]
                        if FEATURE_END in line.strip():
                            break
                    if feature in features and FEATURE_END in line.strip():
                        filtered_file.append(line)
                i = i + 1
                
                
                o = open(path,"w")
                o.writelines(filtered_file)
                o.close()

    def filter_java(path_):
        for path in [path_]:
            print(path)
            file_ = open(path).readlines()
            filtered_file = []
            len_file = len(file_)
            i = 0 
            while i<len_file:
                line = file_[i]
                if not FEATURE_BEGIN in line.strip():
                    filtered_file.append(line)
                else:
                    feature = line[line.rfind(' ')+1:].strip()
                    log.info('Feature %s found' % feature)
                    log.info('FEATURE = ' + feature)
                    print(features)
                    while True:
                        if feature in features:
                            filtered_file.append(line)
                            log.info('Feature in product')
                        else:
                            log.info('Product without feature')
                        i = i+1
                        line = file_[i]
                        if FEATURE_END in line.strip():
                            break
                    if feature in features and FEATURE_END in line.strip():
                        filtered_file.append(line)
                i = i + 1
                
                
                o = open(path,"w")
                o.writelines(filtered_file)
                o.close()

    log.info('Filter files by features')
    for root, dirs, files in os.walk("../%(product)s/" % confs):
        for file_ in files:
            path = root + '/' + file_
            if file_.endswith('.java'):
                log.info('Filtering the ' + path + ' java file')
                filter_java(path)
            if file_.endswith('.xml'):
                log.info('Filtering the ' + path + ' xml file')
                filter_xml(path)

def process_core():
    log.info('Processing the core')
    # TODO filter core files by features
    if 'resfiles' in configspl.core:
        add_resfiles(configspl.core['resfiles'])
    if 'srcfiles' in configspl.core:
        add_srcfiles(configspl.core['srcfiles'])

def process_features(product):
    log.info('Processing the ' + product + ' product')
    p = configspl.products[product]
    if configspl.ALL_FEATURES in p:
        log.info('Adding all features')
        for feature in configspl.features:
            add_feature(feature)
    else:
        for feature in p:
            log.info('Adding the ' + feature)
            add_feature(feature)
            filter_by_features(p)

for product in configspl.products:
    global confs
    global fixed_imports
    global fixed_package
    confs = {}
    fixed_imports = []
    fixed_package = []
    
    setup_project(product)
    process_core()
    
    process_features(product)
