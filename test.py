#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import os


def main():
  print 'Content-Type: text/plain'
  print ''
  print 'TESTING'
  print '==='
  print 'TO DO'
  print ' * test submission form to /submit/.+'
  print '==='
  print 
  for k, v in os.environ.items():
    print "%s = %s" % (k, v)

if __name__ == '__main__':
  main()
