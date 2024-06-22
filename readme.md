# Paul Leonard's Video Platform

## Page Contents
# Project Documentation
- Project Title : Paul Leonard's Video Platform

- [Aim Of Project](#aim-of-project)
    - Defines the overarching goals and objectives the video patform project aims to achieve.

- [Customer Specifications](#client-specifications)
    - Outlines the specifications and expectations provided by the customer(Paul Leonard).



- [Video Page](#video-page)
    - Describes the video page features and functionalities that will be included in the project.
- [Deliverables](#deliverables)
    - Specifies the key outputs and results that will be delivered upon project completion.
- [Installation](#installation)
    - Provides detailed steps for installing and setting up the project environment.
- [Usage](#usage)
    - Offers a comprehensive guide on how to operate and utilize the project effectively.
- [Contributing](#contributing)
    - Details the process and guidelines for contributing to the project’s development.
- [License](#license)
    - Explains the terms and conditions under which the project can be used and distributed.

## Aim Of Project
Paul Leonard, a video creator, is looking for a customized video hosting platform to meet his business's branding needs. Unhappy with current options, he wants a unique solution that allows him to exclusively upload videos under his own brand. Recommended to him by close friends, you now have the opportunity to deliver this tailored solution.



## Client Specifications
### Clients -> Users
1. **Signup & Login**: Users must create an account and log in using an email and password. Account verification is required. Additionally, there should be a feature for resetting passwords to recover lost access.



- Register
![image](/screenshot/signup.png)
- Log in
![image](/screenshot/sign%20in.png)
- Password Reset
-![image](/screenshot/pr.png)
2. **Share Videos**: Users should have the ability to share links to videos across various pages.
![image](/screenshot/share.png)

### Admin
1. **Upload Videos**: Administrators should have the capability to upload videos along with titles and descriptions.

## Video Page

![image](/screenshot/s1.png)

## Home Page

![image](/screenshot/s2.png)
## Deliverables
- **ER Diagram**: ![image](/screenshot/er.jpg)
- **Deployed Link**: [live demo](https://lusitech.pythonanywhere.com/)

## Installation
To install and run this project locally, follow these steps:
1. Clone this repository.
``git clone https://github.com/hamdani2020/Video-Platform.git``
2. Navigate to the project directory.
``cd Video-Platform``
3. Install requirements.
`` pip3 install -r requirements.txt``
4. Run migrations
``python3 manage.py migrate``
5. Create superuser: ``python3 manage.py createsuperuser``
6. Start the development server: ``python3 manage.py runserver``
7. Access the platform at ``http://127.0.0.1:8000/``

## Usage
1. Sign up or log in to access the platform.
2. Navigate through different video pages using the provided controls.
3. Upload videos (Admin only).
4. Share video links with others.

## Contributors
- [Hamdani Alhassan Gandi](www.github.com/hamdani2020)

## License
This project is licensed under the [MIT License](LICENSE).

