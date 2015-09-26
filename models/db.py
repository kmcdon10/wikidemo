# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

db = DAL('sqlite://storage.sqlite')

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
#crud = Crud(db)

db.define_table("image",
    Field("title", unique=True),
    Field("file", "upload"),
    format = "%(title)s")

db.define_table("club",
    Field("name", unique=True),
    Field("city", unique=True),
    Field("state"))

db.define_table('comment',
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(title)s')

db.define_table('document',
    Field('name'),
    Field('file', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(name)s')

db.define_table('blogpost',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    Field('comment_id', 'reference comment'),
    Field('document_id', 'reference document'),
    Field('tags', 'list:string'))

db.define_table('page',
    Field('title'),
    Field('body', 'text'),  # essentially serves as an about me section
    Field('blogpost_id', 'list:reference blogpost'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(title)s')

db.define_table("user",
    Field("first_name"),
    Field("last_name"),
    Field("username", unique=True),
    Field("email", unique=True),
    Field("photo_id", "reference image"),
    Field("page_id", "list:reference page"),
    Field("club", "reference club"))

db.club.name.requires = IS_NOT_EMPTY()
db.club.city.requires = IS_NOT_EMPTY()
db.club.state.requires = IS_NOT_EMPTY()

db.comment.body.requires = IS_NOT_EMPTY()
db.comment.created_by.readable = db.comment.created_by.writable = False
db.comment.created_on.readable = db.comment.created_on.writable = False

db.blogpost.body.requires = IS_NOT_EMPTY()
db.blogpost.created_on.readable = db.blogpost.created_on.writable = False
db.blogpost.created_by.readable = db.blogpost.created_by.writable = False
db.blogpost.comment_id.readable = db.blogpost.comment_id.writable = False
db.blogpost.document_id.readable = db.blogpost.document_id.writable = False

db.page.title.requires = IS_NOT_EMPTY()
db.page.body.reference = IS_NOT_EMPTY()
db.page.blogpost_id.readable = db.page.blogpost_id.writable = False
db.page.created_on.readable = db.page.created_on.writable = False
db.page.created_by.readable = db.page.created_by.writable = False

db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.document.created_by.readable = db.document.created_by.writable = False
db.document.created_on.readable = db.document.created_on.writable = False
