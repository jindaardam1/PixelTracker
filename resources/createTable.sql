CREATE TABLE IF NOT EXISTS EmailsAbiertos (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            ip TEXT NOT NULL,
            user_agent TEXT NULL,
            fecha_abierto DATETIME NOT NULL
        )