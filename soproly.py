#! /usr/bin/python3

# coding: utf-8

import logging as log
log.basicConfig(
    level = log.INFO,
    format = '%(message)s'
)

import sys
sys.path.append('.')

from subprocess import call
import os
from lxml import etree

import configspl

confs = {}
fixed_imports = []
fixed_package = []

def setup_project(product):
    global confs 
    confs = {'product': product}
    log.info("Creating project to %(product)s product." % confs)
    android = configspl.sdkdir + "/tools/android "
    # TODO generalize the activity and the package params
    params = "create project --target 1 --name %(product)s \
--path ../%(product)s --activity MMUnBActivity \
--package br.unb.mobileMedia.%(product)s" % confs
    log.info(android + params)
    os.system(android + params)
    
    files = ['.classpath', '.project']
    for f in files:
        params = {'file': f, 'product': confs['product']}
        copiar = 'cp ./%(file)s ../%(product)s/' % params
        os.system(copiar)
        
    tree = etree.parse("../%(product)s/.project" % confs)
    name = tree.find('name')
    name.text = confs['product']
    file1 = open("../%(product)s/.project" % confs, 'wb')
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

def process_core():
    # TODO filter core files by features
    if 'resfiles' in configspl.core:
        add_resfiles(configspl.core['resfiles'])

def main_activity():
    pass
    # copiar arquivo .java
    # atualizar AndroidManifest
    # atualizar res/main.xml

def fix_package(path, file_):
    log.info('\t ' + file_)
    full_file = path + '/' + file_
    data = open(full_file).readlines()
    end = '.' + path[path.rfind('/')+1:] + ';'
    if not full_file in fixed_package:
        data[0] = data[0].replace(';', end)
        o = open(path + '/' + file_,"w")
        o.writelines(data)
        o.close()
        fixed_package.append(full_file)

def fix_imports(path, file_):
    full_file = path + '/' + file_
    
    if full_file in fixed_imports:
        return
        
    data = open(full_file).readlines()
    old_import = 'import ' + path[path.rfind('src/')+4: path.rfind('/')].replace('/', '.')
    while old_import.count('.') > 2:
        old_import = old_import[:old_import.rfind('.')]
    for i, line in enumerate(data):
        if line.find(old_import)>-1:
            new_import = line[:line.rfind('.')+1]  + path[path.rfind('/')+1:] + line[line.rfind('.'):]
            data[i] = new_import
    o = open(path + '/' + file_,"w")
    o.writelines(data)
    o.close()
    fixed_imports.append(full_file)

def fix_files(path):
    log.info('Fixing the file''s packages')
    for file_ in os.listdir(path):
        fix_package(path, file_)
        fix_imports(path, file_)

def add_srcfiles(files):
    log.info('Copying source files')
    for file_ in files:
        log.info('Copying %s' % file_)
        new_path = file_[:file_.rfind('/')+1]  + confs['product']
        new_dir = '../%(product)s/src/' % confs +'%s' % new_path
        mkdir = 'mkdir -p %s' % new_dir 
        os.system(mkdir)
        cmd = 'cp src/' + file_ + ' ' + new_dir
        os.system(cmd)
        fix_files(new_dir)

def add_feature(feature):
    log.info('Add the %s' % (feature))
    log.info(configspl.features[feature])
    params = configspl.features[feature]
    if 'srcfiles' in params:
        add_srcfiles(params['srcfiles'])
    if 'resfiles' in params:
        add_resfiles(params['resfiles'])

def process_features(product):
    log.info(product)
    if configspl.ALL in product:
        log.info('Adding all features')
        for feature in configspl.features:
            #playlist = configspl.features[configspl.PLAYLIST]
            add_feature(feature)



for product in configspl.products:
    global confs
    global fixed_imports
    global fixed_package
    confs = {}
    fixed_imports = []
    fixed_imports = []
    setup_project(product)
    process_core()
    process_features(configspl.products[product])
