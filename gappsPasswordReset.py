#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
Google Apps for Domains Force Password Change Utility

Author: Gavin M. Roy <gmr@myyearbook.com>
Since: 2009-01-26
License: BSD
'''

import gdata.apps.service, getpass, optparse,sys

def forcePasswordChange( user ):
  print 'Forcing password change for %s' % user.login.user_name
  user.login.change_password = 'true'
  try:
    service.UpdateUser( user.login.user_name, user )
  except gdata.apps.service.AppsForYourDomainException, e:
    print e.reason
    sys.exit( 1 )  

usage = "usage: %prog [options]"
version = "%prog 0.1"
description = "Command line utility to force password resets for all Google Apps for Domain Users"
parser = optparse.OptionParser( usage=usage, version=version, description=description )
parser.add_option( '--domain', '-d', action="store", help='Google Apps for Domains account domain' )
parser.add_option( '--email', '-e', action="store", help='Administrator email address' )
parser.add_option( '--password', '-p', action="store", help='Administrator password' )
parser.add_option( '--all', '-a', action="store_true", default=True, help='Force a reset for all accounts' )
parser.add_option( '--user', '-u', action="store", help='Force a reset for just one user account' )
        
( options, args ) = parser.parse_args( )   

if not options.domain:
  print 'You must specify the Google Apps for Domains domain.'
  sys.exit( 1 )

if not options.email:
  print 'You must specify an administrator email address.'
  sys.exit( 1 )

if options.user:
  options.all = False
  
if not options.password:
  options.password = getpass.getpass( 'Password: ' )

service = gdata.apps.service.AppsService( email = options.email, domain = options.domain, password = options.password )
service.ProgrammaticLogin( )

if options.all is False and options.user:
  try:
    user = service.RetrieveUser( options.user )
  except gdata.apps.service.AppsForYourDomainException, e:
    print e.reason
    sys.exit( 1 )  
  forcePasswordChange( user )

if options.all is True:
  try:
    users = service.RetrieveAllUsers()
  except gdata.apps.service.AppsForYourDomainException, e:
    print e.reason
    sys.exit( 1 )
  for user in users.entry:
    forcePasswordChange( user )

