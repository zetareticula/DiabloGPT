class Config:
    def __init__(self,):
        self.sytheticDir = "Queries/sytheic"
        self.JOBDir = "Queries/JOB"
        self.schemaFile = "schema.sql"
        self.dbName = ""
        self.userName = ""
        self.password = ""
        self.ip = "127.0.0.1"
        self.port = 5432

        self.db_user = self.userName
        self.db_password = self.password
        self.db_host = self.ip
        self.db_port = self.port
        self.db = self.dbName

