class Config:
    UPLOAD_FOLDER = '/tmp'
    CAPA_RULES_PATH = '/opt/capa-rules-7.0.1/'
    ALLOWED_EXTENSIONS = ['exe', 'dll', 'bin', 'sys']
    DATABASE_FILE = 'teams.json'
    ANALYSIS_FILES_FOLDER = '/capa-projext/analysis_files'
    SECRET_KEY = 'xxxxxxxxxxxxxxx' 
    ADMIN_PASS = 'xxxxxxxxxxxxx'
    VIRUSTOTAL_API_KEY = 'xxxxxxxxxxxxxxxxxxx'


    @classmethod
    def update_config(cls, upload_folder, capa_rules_path, allowed_extensions, analysis_files_folder, secret_key):
        cls.UPLOAD_FOLDER = upload_folder
        cls.CAPA_RULES_PATH = capa_rules_path
        cls.ALLOWED_EXTENSIONS = allowed_extensions
        cls.ANALYSIS_FILES_FOLDER = analysis_files_folder
        cls.SECRET_KEY = secret_key
        cls.ADMIN_PASS = admin_pass
        cls.VIRUSTOTAL_API_KEY = virustotal_api_key
