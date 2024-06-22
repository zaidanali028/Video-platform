# Paul Leonard's Video Platform

## Page Contents
# Project Documentation
- Project Title : Paul Leonard's Video Platform

- [Aim Of Project](#aim-of-project)
    - Defines the overarching goals and objectives the video patform project aims to achieve.

- [Home Page](#home-page)
    - A simple Homepage For Paul Leonard's Video Platform

- [Customer Specifications](#client-specifications)
    - Outlines the specifications and expectations provided by the customer(Paul Leonard).


- [Video Page](#video-page)
    - Describes the video page features and functionalities that will be included in the project.

- [Project Deliverables](#project-deliverables)
    - Specifies the key outputs and results that will be delivered upon project completion.
- [Installation](#installation)
    - Provides detailed steps for installing and setting up the project environment.
- [Usage Instructions](#usage-instructions)
    - Offers a comprehensive guide on how to operate and utilize the project effectively.
-[Admin Credentials](#admin-credentials)
    - Demo Login Details(Admin)
-[User Credentials](#user-credentials)
    - Demon Login Details(User)

- [Contributing](#contributing)
    - Details the process and guidelines for contributing to the project’s development.
- [License](#license)
    - Explains the terms and conditions under which the project can be used and distributed.

## Aim Of Project
Paul Leonard, a video creator, is looking for a customized video hosting platform to meet his business's branding needs. Unhappy with current options, he wants a unique solution that allows him to exclusively upload videos under his own brand. Recommended to him by close friends, you now have the opportunity to deliver this tailored solution.

## Home Page

![image](/screens/home_page.png)

## Client Specifications

### Clients -> Users

1. **Signup & Login**: Users must create an account and log in using an email and password. Account verification is required. Additionally, there should be a feature for resetting passwords to recover lost access.



- Register
![image](/screens/registration.png)

- Log in
![image](/screens/login.png)

-  Reset Password
-![image](/screens/reset.png)

-  Reset Password Email
-![image](/screens/reset_email.png)


 **Video Pages**: Users should be able to seamlessly navigate between videos(previous, and next buttons are hidden respectively - if the need be.. )
-  Video Pages
-![image](/screens/video_page.png)


3. **Share Videos**: Users need to have the capability to distribute video links across multiple pages.

![image](/screens/sharing.png)



### Administrators -> Admin
1. **Upload Videos**: Administrators need to be able to upload videos, including adding titles and descriptions.

## Video Page

![image](/screens/admin_video_page.png)


## Project Deliverables
- **Source Code**: [github source](https://github.com/zaidanali028/Video-platform)
- **ER Diagram**: ![image](/screens/ERD.png)
- **Deployed Link**: [live demo](hhttps://aliusmanzaidan.pythonanywhere.com//)

## Installation
Here are the steps to install and run this project locally:

1. **Clone this repository.**
``git clone github.com/zaidanali028/video-platform``

2. **Navigate to the project directory.**
``cd Video-platform``

3. **Install requirements.**
`` pip install -r requirements.txt``

4. **Set Environment Variables**
- Add a `.env` file in the `frame_fusion` directory with these values:
  ```
  API_KEY=<FIREBASE_API_KEY>
  AUTH_DOMAIN=<FIREBASE_AUTH_DOMAIN>
  PROJECT_ID=<FIREBASE_PROJECT_ID>
  STORAGE_BUCKET=<FIREBASE_STORAGE_BUCKET>
  MESSAGING_SENDER_ID=<FIREBASE_MESSAGING_SENDER_ID>
  APP_ID=<FIREBASE_API_ID>
  MEASUREMENT_ID=<FIREBASE_MEASUREMENT_ID>
  CLOUDINARY_API_KEY=<CLOUDINARY_API_KEY>
  CLOUDINARY_API_SECRET=<CLOUDINARY_API_SECRET>
  CLOUDINARY_CLOUD_NAME=<CLOUDINARY_CLOUD_NAME>
  EMAIL_PORT=<SMTP_EMAIL_PORT>
  EMAIL_HOST=<SMTP_EMAIL_HOST>
  EMAIL_HOST_USER=<EMAIL_ADDRESS>
  EMAIL_HOST_PASSWORD=<EMAIL_PASSWORD>
  EMAIL_USE_TLS=TRUE
  DEFAULT_FROM_EMAIL=<EMAIL_ADDRESS>
  ```

5. **Configure Firebase Cloud Storage**
- You can configure Firebase Cloud Storage [here](https://firebase.google.com/docs/storage/web/start).

6. **Configure Cloudinary API Keys**
- You can configure your Cloudinary API keys [here](https://cloudinary.com/documentation/how_to_integrate_cloudinary).

7. **Configure SMTP for Sending Emails**
- Configure SMTP settings for sending emails [here](https://docs.djangoproject.com/en/5.0/topics/email/).

8.**Running migrations**
``python3 manage.py migrate``

9. **Creating superuser:** ``python manage.py createsuperuser``

10. **Starting the dev server:** ``python manage.py runserver``

11. **Access the video platform at** ``http://127.0.0.1:8000/``

## Usage Instructions
1. [Register](https://aliusmanzaidan.pythonanywhere.com/auth/register/) or [log in](https://aliusmanzaidan.pythonanywhere.com/auth/login/) to access the platform.

2. Explore various video pages using the provided navigation controls on the videos Page.

3. Upload videos [Administrators only](https://aliusmanzaidan.pythonanywhere.com/admin-app/videos/).

4. Share video links with others.

5. You can access the demo of this application at [https://aliusmanzaidan.pythonanywhere.com/](https://aliusmanzaidan.pythonanywhere.com/).

### Admin Credentials
- **Email**: king3@dj.com
- **Password**: b022903920::AAAA

### User Credentials
- **Email**: zaidanali028@gmail.com
- **Password**: zizu!)@93290;

## Contributing
- [Ali Usman Zaidan](zaidanali028@gmail.com)
  - Email: zaidanali028@gmail.com
  - Portfolio: [MY CV FILES](https://drive.google.com/drive/folders/1Ud9eYWR10HjFUyK4WM5m0rLnQWQrbVcZ?usp=sharing)

## License
This project is licensed under the [MIT License](LICENSE).

## Frontend Reactivity And Templating Credits

- **HTMX**
  HTMX is a lightweight JavaScript library that allows you to access AJAX, WebSockets, and Server-Sent Events directly in HTML, using attributes like `hx-get` and `hx-post`. It simplifies the integration of dynamic content into your web applications.
  [Learn more about HTMX](https://htmx.org/)

- **Soft UI Tailwind Admin Dashboard by Creative Tim**
  The Soft UI Tailwind Admin Dashboard is a modern, responsive admin template built with Tailwind CSS. It provides a clean and customizable interface for building web applications with ease.
  [Explore the Soft UI Tailwind Admin Dashboard](https://www.creative-tim.com/product/soft-ui-dashboard)

- **Colorlib Bootstrap Anime Video Template**
  The Colorlib Bootstrap Anime Video Template is a responsive web template designed for showcasing anime videos. It utilizes Bootstrap framework for layout and styling, making it easy to create visually appealing video-centric websites.
  [Check out the Colorlib Bootstrap Anime Video Template](https://colorlib.com/)
