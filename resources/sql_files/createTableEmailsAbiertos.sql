CREATE TABLE IF NOT EXISTS EmailsAbiertos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_guardado_id INTEGER,
    ip TEXT NOT NULL,
    location TEXT,
    zip TEXT,
    user_agent TEXT,
    fecha_abierto DATETIME NOT NULL,
    FOREIGN KEY (email_guardado_id) REFERENCES EmailsGuardados(id)
);
