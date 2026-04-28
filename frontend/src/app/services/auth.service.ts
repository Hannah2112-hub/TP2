import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { TipoUsuario } from '../models/modelos';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private loggedIn = signal(false);
  private userType = signal<TipoUsuario | null>(null);
  private userName = signal('');
  private userId = signal<number | null>(null);

  constructor(private router: Router) {
    if (typeof window !== 'undefined' && window.localStorage) {
      const saved = localStorage.getItem('auth');
      if (saved) {
        const data = JSON.parse(saved);
        this.loggedIn.set(data.loggedIn);
        this.userType.set(data.userType);
        this.userName.set(data.userName);
        this.userId.set(data.userId || null);
      }
    }
  }

  get isLoggedIn() {
    return this.loggedIn.asReadonly();
  }
  get currentUserType() {
    return this.userType.asReadonly();
  }
  get currentUserName() {
    return this.userName.asReadonly();
  }
  get currentUserId() {
    return this.userId.asReadonly();
  }

  login(email: string, password: string, tipo: TipoUsuario): boolean {
    // Aceptamos cualquier credencial como solicitaste
    let nombreGenerico = 'Usuario';
    if (tipo === 'admin') nombreGenerico = 'Administrador';
    else if (tipo === 'docente') nombreGenerico = 'Docente';
    else if (tipo === 'estudiante') nombreGenerico = 'Estudiante';

    this.loggedIn.set(true);
    this.userType.set(tipo);
    this.userName.set(nombreGenerico);
    
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem(
        'auth',
        JSON.stringify({
          loggedIn: true,
          userType: tipo,
          userName: nombreGenerico,
        }),
      );
    }
    return true;
  }

  logout() {
    this.loggedIn.set(false);
    this.userType.set(null);
    this.userName.set('');
    this.userId.set(null);
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.removeItem('auth');
    }
    this.router.navigate(['/login']);
  }

  checkAuth(): boolean {
    return this.loggedIn();
  }
}
