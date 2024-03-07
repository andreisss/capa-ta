# Capa-ta - Enhance Your Malware Analysis

![PyPI](https://img.shields.io/pypi/v/capa-ta)
![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Number of Rules](https://img.shields.io/badge/rules-1000+-brightgreen)
![Downloads](https://img.shields.io/github/downloads/andreisss/capa-ta/total.svg)
![License](https://img.shields.io/github/license/andreisss/capa-ta)

## Based On

This tool leverages the capabilities of two major resources:

- **Capa:** An open-source tool designed for the automatic detection of patterns in binary files. It's developed and maintained by Mandiant. For more details, visit [Capa on GitHub](https://github.com/mandiant/capa).

- **VT API:** The VirusTotal API allows for easy integration of VT's comprehensive file scanning capabilities into applications. For API documentation and usage, see the [VirusTotal API Documentation](https://docs.virustotal.com/).

Capa-ta leverages advanced analysis techniques to dissect and understand malware and give your team the possibility to analyze malware.

## Admin 
----------------------------------------------------------------------------------------
- **User Management**
  - **Create User:** Add new users to the application.
  - **Edit User:** Update user information and roles.
  - **Delete User:** Remove users from the application.

- **Team Management**
  - **Create Team:** Establish new teams for organizing users.
  - **Modify Team:** Change team details or member assignments.

- **Settings**
  - **Modify Settings:** Update application-wide settings, including:
    - **VT API Key:** Configure the VirusTotal API key for malware analysis.
    - **Admin Password:** Set or change the admin password for enhanced security.
    - **Capa Path:** Specify the path to Capa rules for automated analysis.
    - **Analysis Folder:** Designate a folder for storing analysis reports.
    - **Allowed extensions:** Decide the extensions which can be uploaded.
    - **Upload folder:** Decide which folder to upload the files.
      
## User Side
----------------------------------------------------------------------------------------
- **Upload File:** Submit files for analysis or review.
- **Collaborate with Your Team:** Work together with team members on projects or analyses.
- **Default Team:** Users not assigned to a specific team can use the Default team for their activities.


## Features

- **Automated Malware Analysis:** Quickly identifies known malware patterns, saving time of manual analysis.
- **Extensive Rule Set:** With over 1000+ rules, Capa-ta can recognize a wide range of malware characteristics.
- **Easy to Use:** Designed for usability, it integrates seamlessly into existing workflows.

The capa-ta web leverages the **Capa tool** and **VT** API to detect capabilities in executable files, offering a collaborative platform with the following features:

![image](https://github.com/andreisss/capa-ta/assets/10872139/45ee9a28-1e2b-4f10-b322-4cf39b9ec929)

----------------------------------------------------------------------------------------------------------------------------------------


- **Team Collaboration:** 
  - Create teams to share analysis reports effortlessly.
  - Assign users to specific teams to streamline workflow.

- **User Management:**
  - Facilitate the creation of user accounts for personalized access.
  - Enhance security and accountability within the team environment.

- **🚀Participation and Collaboration:**
  - Emphasize the importance of active participation and collaboration.
  - Foster a culture of shared knowledge and collective problem-solving.


Enhance your team's executable analysis capabilities from the outset with **Capa-ta**. Dive into your first malware analysis approach armed with a tool designed to streamline and empower your investigative processes.

```bash
gunicorn -w 4 -b 143.181.123.123:7665 app:app
```
----------------------------------------------------------------------------------------------------------------------------------------

### Admin gui

Default Access: admin - password123

![image](https://github.com/andreisss/capa-ta/assets/10872139/01a286e6-91ac-4e4a-8c6e-61d247dc4e5c)

# Application Functions

Our application offers a comprehensive set of functions to manage users and teams efficiently. Here's a quick overview of the key functionalities:

- **Create Users**: Allows administrators to add new users to the application, specifying essential information like usernames, passwords, and roles.

- **Create Teams**: Facilitates the creation of teams within the application, enabling better organization and collaboration among users.

- **Change User Team**: Enables the reassignment of users from one team to another, supporting flexible team management and project reorganization.

- **Delete User**: Provides the option to remove users from the application, ensuring that access is tightly controlled and can be revoked when necessary.

- **Delete Team**: Allows for the deletion of teams, making it easy to manage the application's organizational structure as projects evolve or conclude.

Each of these functions is designed to simplify administrative tasks, making it straightforward to manage the application's user base and organizational setup.

----------------------------------------------------------------------------------------------------------------------------------------


![image](https://github.com/andreisss/capa-ta/assets/10872139/fc308b42-abc7-41e6-af00-d1b9d0a14dcd)

----------------------------------------------------------------------------------------------------------------------------------------


# Admin Settings

### Configuration Table

<div align="center">

| Setting               | Description                                           |
|-----------------------|-------------------------------------------------------|
| Upload Folder         | Directory for storing uploaded files.                 |
| Capa Rules Path       | Folder path for Capa rules.                           |
| Analysis Files Folder | Location for analysis reports and temporary files.    |
| App Secret Key        | Secret key for securing cookies and sessions.         |
| Allowed Extensions    | File types permitted for upload.                      |
| Admin Password        | Password for administrative access.                   |
| VirusTotal API Key    | API key for VirusTotal integration.                   |

</div>

----------------------------------------------------------------------------------------------------------------------------------------


![image](https://github.com/andreisss/capa-ta/assets/10872139/6473f466-15a8-4a58-ab2e-70ef66ef7295)

# Team page:

![image](https://github.com/andreisss/capa-ta/assets/10872139/d615e4c7-25ed-4395-8d3c-c803e75acc90)

----------------------------------------------------------------------------------------------------------------------------------------


# Report Page:

![image](https://github.com/andreisss/capa-ta/assets/10872139/98a5c8a7-f2c9-43a8-a119-b5fd6acaf32d)

----------------------------------------------------------------------------------------------------------------------------------------


![image](https://github.com/andreisss/capa-ta/assets/10872139/93c0e7b7-deef-4802-ab32-660bc11105b9)

----------------------------------------------------------------------------------------------------------------------------------------


![image](https://github.com/andreisss/capa-ta/assets/10872139/73a7e80b-e26d-46d5-95d4-0bcbb033bd5d)

----------------------------------------------------------------------------------------------------------------------------------------

![image](https://github.com/andreisss/capa-ta/assets/10872139/b34e68a7-4917-4212-a933-d7876e3657f8)


