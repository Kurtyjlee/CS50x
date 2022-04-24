# InteetSgintern #
#### Video Demo:  https://youtu.be/W1S9pEKPdN4

#### Description: This is our submission for the CS50 final project.
###### We are Kurt, Yao Yang and Chin Yi from Singapore. We have experienced how tough it is for pre-university students to reach out to companies and mentors for internships, especially in Singapore, hence we thought of creating a platform where employers and students can connect more directly.

###### We used HTML, CSS and flask to create website where users interact, python to programme the bot for telegram and firebase as our main database to connect both platforms. The website is designed using the bootstrap framework for a more modern finish.

###### We believe that having the connection between the website and telegram is a strong driving factor as telegram is a widely used messaging platform for youngsters in Singapore. With telegram, it would be easier for companies to reach out the students and for students to stay more up to date on their job seeking journey.

###### Kurt: HTML, CSS and flask. YaoYang: Python and firebase Chin Yi: Python and Telegram

###### Usage: The user is directed to home.html where he is being greeted by our motto, "Creating opportunities for our youths.". The user can then decide to create an account as a business owner or a student. The username is verified using the database, to check if the username is unique. The user can then login into their account where their session is stored. The user is greeted by the different job postings on the website and can click on the postings to find out more. The user, if an employer can create a new post and upload it directly to the server. If a student however, can update their profile and searches, if their interests and qualifications have changed. All data is sent to the firebase server where the user profile and other data is stored in json format, for easy retievval using python. When logging out, the session of the user is then removed from the programme. On the telegram side, students interact with the telegram bot on the go, receiving job offers regularly and connecting with employers more directly. Users who decide to create an account through telegram can also do so and receive information in that intance.

###### flask app.py runs the flask programme, connecting all the sites and simple user interface logic using helper.py that contains the required_login function to check if users are still logged in.
###### python: web_firebaseDB.py runs the server-side logic for the login, register and pages, verifying the users and their password, and sending it to the server for the telegram bot to have access it to. database.py runs the server-side logic for the index page, pulling posts into and displaying onto the webpage dynamically.
###### html and css. The templates include layout.html as the main app, index.html as the main user page, home.html as the greeting page, login.html, register.html and emp_reg.html as the user identification pages. upload.html is meant for employers to upload data onto the server and profile.html is meant for users to update their profile.
###### Telegram: The telegram logic is in the Telegram_bot_Github_safe folder, where the bot retrieves information from the server and sends it to the user on telegram. It also allows user to create their account using telegram.

