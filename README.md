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
has to use his credentials to retin access token.See the diagram below to understand how
OAuth service will work to access protected resources.

![image](https://user-images.githubusercontent.com/19213074/128780863-f707e567-00a7-4c0d-9cab-fe901ff180ea.png)

