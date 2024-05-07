-- Crear la base de datos
CREATE DATABASE clinica;

-- Usar la base de datos recién creada
USE clinica;

-- Crear la tabla de Pacientes
CREATE TABLE Pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    identificacion VARCHAR(20),
    contacto VARCHAR(100)
);

-- Crear la tabla de Tipos de Estudio
CREATE TABLE TiposEstudio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);

-- Crear la tabla de Turnos
CREATE TABLE Turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_turno INT,
    tipo_estudio_id INT,
    paciente_id INT,
    fecha_hora_emision DATETIME,
    estado VARCHAR(25) CHECK (estado IN ('paciente nuevo', 'paciente con expediente')),  -- Restricción de verificación
    FOREIGN KEY (tipo_estudio_id) REFERENCES TiposEstudio(id),
    FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
);

drop database clinica;
drop table Turnos;
SHOW DATABASES;