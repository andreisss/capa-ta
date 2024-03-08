# Capa-ta - Enhance Your Malware Analysis

![PyPI](https://img.shields.io/pypi/v/capa-ta)
![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Number of Rules](https://img.shields.io/badge/rules-1000+-brightgreen)
![Downloads](https://img.shields.io/github/downloads/andreisss/capa-ta/total.svg)
![License](https://img.shields.io/github/license/andreisss/capa-ta)

Capa-ta leverages the **Capa tool** and **VT API** to detect capabilities in executable files, offering a platform for automated malware analysis and team collaboration.

## Key Features

- **Automated Malware Analysis:** Quickly identifies known malware patterns, saving manual analysis time.
- **Extensive Rule Set:** Over 1000+ rules to recognize a wide range of malware characteristics.
- **Easy to Use:** Integrates seamlessly into existing workflows.
- **Team Collaboration:** Share analysis reports and manage team workflows efficiently.

## Based On

- **[Capa](https://github.com/mandiant/capa):** An open-source tool by Mandiant for automatic pattern detection in binary files.
- **[VT API](https://docs.virustotal.com/):** VirusTotal's comprehensive file scanning API for applications.

## Admin Features

### User and Team Management

- **Create, Edit, Delete Users:** Manage user access and roles.
- **Create, Modify, Delete Teams:** Organize users for better collaboration.

### Settings Configuration

- **VT API Key:** Integrate VirusTotal's scanning capabilities.
- **Admin Password:** Secure admin access.
- **Capa Path & Analysis Folder:** Specify paths for Capa rules and analysis reports.
- **Allowed Extensions & Upload Folder:** Control file uploads.

### Admin GUI Access

Default access credentials: `admin / password123`

![image](https://github.com/andreisss/capa-ta/assets/10872139/8e217f01-9e5d-4624-b6d7-53e635b44316)

## User Features

- **Upload File:** Analyze files with ease.
- **Collaborate with Your Team:** Use the Default team or assign specific teams for project management.

![image](https://github.com/andreisss/capa-ta/assets/10872139/3348c22c-ec81-45cd-8c62-2b29cf96574a)


# Quick Start

Follow these steps to get started:

1. **Install python3 and pip3**



2. **Launch Capa-ta with Gunicorn**
First, install Gunicorn:

Then, start your application with Gunicorn by replacing `your_ip` with your actual IP address:


3. **Log in to the Admin Console**
Access the admin console using the following credentials:
- Username: `admin`
- Password: `password123`

4. **Configure Settings**
In the settings page, set the following configurations:
- Default Capa Rules Directory
- Upload Folder
- App Secret Key
- Admin Password
- VT API Key

----------------------------------------------------------------------------------------------------------------------------------------


![image](https://github.com/andreisss/capa-ta/assets/10872139/035ebbd3-81de-4d4d-91b1-618bac904e68)

----------------------------------------------------------------------------------------------------------------------------------------



![image](https://github.com/andreisss/capa-ta/assets/10872139/6473f466-15a8-4a58-ab2e-70ef66ef7295)

----------------------------------------------------------------------------------------------------------------------------------------


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


