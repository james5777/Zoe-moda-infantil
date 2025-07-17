SQLserver = (
        'mssql+pyodbc://zoe_app_user:98013153647@DESKTOP-FNK7EFN/Zoe?'
        'driver=ODBC+Driver+17+for+SQL+Server&encrypt=yes&TrustServerCertificate=yes'
    )


class Config: 
    DEBUG = True
    SECRET_KEY = 'dev'
   
    SQLALCHEMY_DATABASE_URI = SQLserver

    SQLALCHEMY_TRACK_MODIFICATIONS = False