#!/usr/bin/python

# pywordpress: access wordpress blog over XML-RPC protocol
# using xmlrpclib library

import xmlrpclib
import urllib2
import datetime

PUBLISHED = 1 # status indicators for a post
DRAFT = 0

def check_url(url):
	try:
		url_object = urllib2.urlopen(url)
		if not url_object.geturl() == url:
			# TODO: instead of raising an HTTPError on 
			# encountering redirection, raise a meaningful
			# exception
			raise urllib2.HTTPError

	except urllib2.HTTPError:
		print "Bad Url."
		return False
	else:
		return True

class Wordpress(object):
	"""Defines the Wordpress blog."""
	
	def __init__(self, wp_user, wp_pass, wp_url):
		"""Initialize your wordpress blog.

		wp_user: login username
		wp_pass: your password
		wp_url : the url to your xmlrpc server in wordress.
				 (ex: http://myblog.com/xmlrpc.php,
				 	  http://mysite.com/myblog/xmlrpc.php)
		The xml-rpc.php (i.e. the XML-RPC server to communicate
		to) is normally resided within the root of a wordpress blog.
		In rare circumstances, it might not. Hence the need to provide
		the exact location.
		"""

		self.blog_id = ''
		self.wp_user = wp_user
		self.wp_pass = wp_pass
		
		# check if the server url is correct
		if check_url(wp_url):
			self.wp_url = wp_url
		else:
			pass
			# TODO: make an exception and raise it here

		

		# Open Server connection
		self.server = xmlrpclib.ServerProxy(wp_url)

	def newPost(self, post):
		"""Publish a post described by the post object"""
		post_id = self.server.metaWeblog.newPost(self.blog_id, self.wp_user, 
						self.wp_pass, post.get_dict(), post.get_status())

			

class Post(object):
	"""Defines a blog Post which can be passed to the blog.

	A Post object describes the categories, tags, title, body, summary
	and date attributes for a post. 
	The Post object can be published by passing it to a Wordpress instance.
	"""

	def __init__(self, title, description, categories, mt_keywords, 
	                        dateCreated = None, mt_text_more = ''):
	    """Initializes a new Post.
	    
	    A post is defined by a 
		title		: Title of the post/subject, 
		description : Body of the post,
		dateCreated : a datetime object if provided or else will be set to now(),
		categories  : list of categories for the post to be posted in,
		mt_keywords : list of tags for the post,
		mt_text_more: If the post has a summary and full post, the full post is 
					  posted here and the summary in description.
		"""

	    self.title = title
	    self.description = description
	    self.categories = categories,
	    self.mt_keywords = mt_keywords,
	    if not dateCreated:
	    	self.dateCreated = datetime.datetime.now()
	    else:
	        self.dateCreated = dateCreated
	    self.mt_text_more = mt_text_more
	    # default status for a post is PUBLISHED
	    # use Post.change_status(status) to change the status
	    # status can be PUBLISHED or DRAFT
	    self.status = PUBLISHED
	
	def change_status(self, status):
		""" Changes status of a post.

		Viable status: PUBLISHED* and DRAFT
		*:default
		"""
		self.status = status

	def get_status(self):
		""" return the status of the post."""
		return self.status
	
	def get_dict(self):
		"""Compiles the properties of a post in a dictionary.

		When publishing a post through xmlrpclib.metaWeblog.newPost(..),
		the post has to passed as a dictionary.
		The keys of the the dictionary are the same as the ones accepted in 
		the constructor of Post.
		"""
		self.data = { 'title': self.title,
				 'description': self.description,
				 'categories' : self.categories,
				 'mt_keywords': self.mt_keywords,
				 'dateCreated': self.dateCreated,
				 'mt_text_more': self.mt_text_more
			}
		return self.data
		


		
		

