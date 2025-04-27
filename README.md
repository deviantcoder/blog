# Django Blog App
A feature-rich blog application built with Django, supporting authentication, post management, comments, upvotes, and search functionality.

## Features  

### Authentication  
- Standard login via username or email  
- 2-step user registration with email activation  
- Social authentication via Google and GitHub  
- Password reset functionality  

### User Profiles  
- Profile management and editing  

### Posts  
- Full CRUD functionality  
- EasyMDE for Markdown content editing  
- Commenting system with hierarchical (MPTT) structure  
- Upvoting system 
- Recently viewed posts (stored in session)  
- Pagination
- Dynamic filtering (django-filter, htmx)
- Infinite scroll

### Search  
- Elasticsearch-powered search running in Docker

### API  
- Django Rest Framework 