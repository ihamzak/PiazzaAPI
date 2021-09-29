# PiazzaAPI
Piazza API is a Social Media Platform API. 
API Resources can be accessed through OAuth2.0 
See the below  link for API  documentation . 

https://documenter.getpostman.com/view/12170320/TzJpifH8


### Phase A: Install and deploy software in virtualised environments
In phase A we will install the necessary packages required to run our API without any
dependency issues. We will install the following packages in order to support our API .

● django

● django-rest-framework

● django-oauth-toolkit



Source folder consists of 3 subfolders PiazzaAPI, Piazza and Users. PiazzaAPI contains all
the settings file of our project. While the other two subfolders Users and Piazza are app
folders which contain all the necessary files for our Users and Piazza apps.

### Phase B: Development of authorisation and authentication services

In phase B we will develop OAuth authorisation service for our API. OAuth protocol will allow
the registered users to access the resources in our piazza application service.

OAuth introduces an authorization layer and separates the role of the client from that of the
resource owner. In OAuth, the client requests access to resources controlled by the resource
owner and hosted by the resource server and is issued a different set of credentials than
those of the resource owner. Instead of using the resource owner's credentials to access
protected resources, the client obtains an access token--a string denoting a specific scope,
lifetime, and other access attributes. Access tokens are issued to third-party clients by an
authorization server with the approval of the resource owner. Then the client uses the
access token to access the protected resources hosted by the resource server.[1]

To access the resources in Piazza service , first user’s have to register themselves and a
new token will be issued to newly registered users. If the user is already registered, the user
has to use his credentials to retain access token.See the diagram below to understand how
OAuth service will work to access protected resources.

![Development of a Cloud Software as a Service (1)](https://user-images.githubusercontent.com/19213074/128781388-fa29d1a3-1043-4d60-abe6-52001e735023.jpg)



### Services

We have developed SaaS in Python using Django and Django Rest Framework. There are
mainly 2 services in our SaaS application. The first service is Authentication service which
is used to register the user if the user is not already registered in the system. Registered
users can get access token information using their credentials. The second service is Piazza
service which provides the main functionality to authenticated users such as creating a post
in a specific topic with expiration time and allowing other users to like, dislike and comment
on other user’s posts.

### Piazza Service Data Model

The database design of our Piazza service is shown below.

![image](https://user-images.githubusercontent.com/19213074/128780994-a60f22ff-c7e8-475b-9614-a745f19708c7.png)

From the above ERD diagram we can see that each Post can have one topic but a topic
can have zero or many posts. While each comment is referenced to one post but a Post can
have zero or many comments and each post can have many likes or dislikes but a like and
dislike entity can have reference to one and only one like or dislike.

### Services Endpoints

##### User Service / Authentication Service

User service allows the user to register if they are not already registered in the system. If the
user is already registered then they can use their credentials to get their access token.

##### Piazza Service
Piazza service allows authenticated/registered users to perform many operations. See the
attached link below to read API documentation. As there are many end points in my API so
I have created documentation for my API.

https://documenter.getpostman.com/view/12170320/TzJpifH8






