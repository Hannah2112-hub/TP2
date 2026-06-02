from typing import List, Dict, Any
from ..config.database import execute_query


class CarreraRepository:
    @staticmethod
    def setup_table():
        query = """
        CREATE TABLE IF NOT EXISTS carreras (
            carreraid SERIAL PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            facultad VARCHAR(150) NOT NULL,
            activo BOOLEAN DEFAULT TRUE
        );
        """
        execute_query(query)
        
        # Add carreraid to cursos if it doesn't exist
        query_alter = """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                           WHERE table_name='cursos' AND column_name='carreraid') THEN
                ALTER TABLE cursos ADD COLUMN carreraid INT REFERENCES carreras(carreraid);
            END IF;
        END
        $$;
        """
        execute_query(query_alter)

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return execute_query("SELECT * FROM carreras WHERE activo = TRUE")

    @staticmethod
    def get_by_id(carrera_id: int) -> Dict[str, Any]:
        result = execute_query(
            "SELECT * FROM carreras WHERE carreraid = %s AND activo = TRUE",
            [carrera_id],
        )
        return result[0] if result else None

    @staticmethod
    def create(nombre: str, facultad: str) -> Dict[str, Any]:
        result = execute_query(
            "INSERT INTO carreras (nombre, facultad) VALUES (%s, %s) RETURNING carreraid",
            [nombre, facultad],
        )
        if result:
            return {"Exito": True, "ID": result[0]["carreraid"], "Mensaje": "Carrera registrada"}
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def update(carrera_id: int, nombre: str, facultad: str) -> bool:
        execute_query(
            "UPDATE carreras SET nombre = COALESCE(%s, nombre), facultad = COALESCE(%s, facultad) WHERE carreraid = %s",
            [nombre, facultad, carrera_id],
        )
        return True

    @staticmethod
    def delete(carrera_id: int) -> bool:
        execute_query("UPDATE carreras SET activo = FALSE WHERE carreraid = %s", [carrera_id])
        return True
