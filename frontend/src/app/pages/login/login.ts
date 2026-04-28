import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { TipoUsuario } from '../../models/modelos';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginComponent {
  email = signal('');
  password = signal('');
  tipoUsuario = signal<TipoUsuario>('admin');
  errorMessage = signal('');
  showError = signal(false);

  constructor(
    private auth: AuthService,
    private router: Router,
  ) {}

  selectType(tipo: TipoUsuario) {
    this.tipoUsuario.set(tipo);
  }

  login() {
    const success = this.auth.login(this.email(), this.password(), this.tipoUsuario());
    if (success) {
      this.router.navigate(['/dashboard']);
    } else {
      this.showError.set(true);
      this.errorMessage.set('Credenciales incorrectas. Intenta de nuevo.');
      setTimeout(() => this.showError.set(false), 4000);
    }
  }
}
