# one-penny-book-tracker
Beginnings of web app to monitor the price of books on amazon, and notify users when price drops below threshold.

Using Flask and SQLAlchemy and Marshmallow so far for the backend.

JWT for user authentication.
Basic Flask-Mail config for sending email.

No frontend yet - expected to be based on regularly scraping Amazon product pages for items added to user database (or look at user's amazon wishlist in an advanced iteration), and send email when minimum listed price drops below preset.
