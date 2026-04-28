export interface Estudiante {
  id?: number;
  codigo: string;
  nombre: string;
  creditos: number;
  correo: string;
}

export interface Docente {
  id?: number;
  codigo: string;
  nombre: string;
  especialidad: string;
  correo: string;
}

export interface Curso {
  id?: number;
  codigo: string;
  nombre: string;
  creditos: number;
  prereq: string;
  docente: string;
  cupos: number;
  nombreDocente?: string;
}

export interface Aula {
  id?: number;
  nombre: string;
  capacidad: number;
  edificio: string;
  equipamiento: string;
}

export interface Matricula {
  id?: number;
  estudiante: string;
  curso: string;
  estado: string;
  detalle: string;
  nombreEstudiante?: string;
  nombreCurso?: string;
}

export interface AsignacionHorario {
  id?: number;
  curso: string;
  codigo: string;
  docente: string;
  dia: string;
  horaInicio: number;
  horaFin: number;
  aula: string;
  color: string;
}

export type TipoUsuario = 'admin' | 'docente' | 'estudiante';

export interface Usuario {
  email: string;
  password: string;
  tipo: TipoUsuario;
  nombre: string;
}

