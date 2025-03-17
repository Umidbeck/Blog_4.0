# Blog_4.0
Blog_4.0
Blog_4.0 is the latest iteration of a minimalist blog platform developed using Django. This version introduces enhanced features and optimizations to improve both user and admin experiences.

Features
Admin-Only Content Creation: Only administrators have the authority to create and manage blog posts, ensuring content integrity and quality.

User Commenting: Visitors can engage with posts through a straightforward commenting system, fostering interaction without the need for user registration.

Password Reset Functionality: Secure password recovery mechanisms are in place to assist administrators in maintaining account access.

Optimized Caching: Implemented caching strategies enhance performance by reducing load times and server requests.

SEO-Friendly URLs: Utilization of slug-based URLs improves search engine visibility and user-friendly navigation.

Technology Stack
Backend: Django (Python)
Database: SQLite
Frontend: HTML, CSS, Bootstrap
Caching: Django Cache Framework
Installation & Setup
Clone the repository:

bash
Copy
Edit
git clone https://github.com/Umidbeck/Blog_4.0.git
cd Blog_4.0
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Apply migrations:

bash
Copy
Edit
python manage.py migrate
Create a superuser (admin):

bash
Copy
Edit
python manage.py createsuperuser
Run the development server:

bash
Copy
Edit
python manage.py runserver
Access the blog at http://127.0.0.1:8000/
