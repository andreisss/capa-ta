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


## Features

- **Automated Malware Analysis:** Quickly identifies known malware patterns, saving hours of manual analysis.
- **Extensive Rule Set:** With over 1000+ rules, Capa-ta can recognize a wide range of malware characteristics.
- **Easy to Use:** Designed for usability, it integrates seamlessly into existing workflows.

The capa-ta web leverages the **Capa tool** and **VT** API to detect capabilities in executable files, offering a collaborative platform with the following features:

![image](https://github.com/andreisss/capa-ta/assets/10872139/45ee9a28-1e2b-4f10-b322-4cf39b9ec929)


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

![image](https://github.com/andreisss/capa-ta/assets/10872139/01a286e6-91ac-4e4a-8c6e-61d247dc4e5c)

# Application Functions

Our application offers a comprehensive set of functions to manage users and teams efficiently. Here's a quick overview of the key functionalities:

- **Create Users**: Allows administrators to add new users to the application, specifying essential information like usernames, passwords, and roles.

- **Create Teams**: Facilitates the creation of teams within the application, enabling better organization and collaboration among users.

- **Change User Team**: Enables the reassignment of users from one team to another, supporting flexible team management and project reorganization.

- **Delete User**: Provides the option to remove users from the application, ensuring that access is tightly controlled and can be revoked when necessary.

- **Delete Team**: Allows for the deletion of teams, making it easy to manage the application's organizational structure as projects evolve or conclude.

Each of these functions is designed to simplify administrative tasks, making it straightforward to manage the application's user base and organizational setup.


![image](https://github.com/andreisss/capa-ta/assets/10872139/fc308b42-abc7-41e6-af00-d1b9d0a14dcd)


# Admin Settings

Configure your application with ease using the admin settings page. Here, you'll find options for customizing various functionalities and security settings:

Below is a detailed overview of each setting available on the Functions Settings Page:

### Configuration Table

| Setting               | Description                                           |
|-----------------------|-------------------------------------------------------|
| Upload Folder         | Directory for storing uploaded files.                 |
| Capa Rules Path       | Folder path for Capa rules.                           |
| Analysis Files Folder | Location for analysis reports and temporary files.    |
| App Secret Key        | Secret key for securing cookies and sessions.         |
| Allowed Extensions    | File types permitted for upload.                      |
| Admin Password        | Password for administrative access.                   |
| VirusTotal API Key    | API key for VirusTotal integration.                   |

Adjust these settings as needed to tailor the application to your specific requirements and security standards.

![image](https://github.com/andreisss/capa-ta/assets/10872139/6473f466-15a8-4a58-ab2e-70ef66ef7295)


-------------------------------------------------------------------------------------------------------------------------------------------

### User Interface

![video1 (5)](https://github.com/andreisss/Capa-web/assets/10872139/6eadfd08-3687-4f54-8469-3fa19080e399)
