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

Capa-ta leverages advanced analysis techniques to dissect and understand malware at a deeper level.
Capa-ta helps security researchers and analysts automatically identify malware capabilities, making the analysis process faster and more comprehensive.

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

Funtions: Create Users, Create Teams, Change User team, Delete User, Delete Team

![admin (2)](https://github.com/andreisss/Capa-web/assets/10872139/d4a2084e-7714-462d-9db5-3f42f8b22923)



### Admin settings

Funcions Settings Page:  Upload Folder ,  Capa Rules Path ,  Analysis Files Folder ,  App Secret Key ,  Allowed Extensions , Admin Password,  VirusTotal API Key 


<p align="center">
  <img src="https://github.com/andreisss/Capa-web/assets/10872139/cdf9608a-a7c9-4ceb-8a53-a278b16da041" alt="Admin Control Panel" />
</p>

-------------------------------------------------------------------------------------------------------------------------------------------

### User Interface

![video1 (5)](https://github.com/andreisss/Capa-web/assets/10872139/6eadfd08-3687-4f54-8469-3fa19080e399)
