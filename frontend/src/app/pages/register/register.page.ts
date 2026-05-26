import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-register-page',
  imports: [ReactiveFormsModule, RouterLink],
  template: `
    <section class="auth-shell register-shell">
      <div class="auth-card register-card">
        <div class="register-head">
          <h1>Create an account</h1>
          <p>Join AelithraStay to find your next stay or start hosting.</p>
        </div>

        <form [formGroup]="form" (ngSubmit)="submit()">
          <label>
            Username
            <input formControlName="username" placeholder="john_doe" />
            <small class="field-hint">Use letters, numbers, @, ., +, -, or _. No spaces.</small>
          </label>
          <label>Email<input formControlName="email" type="email" placeholder="name@example.com" /></label>
          <div class="form-grid">
            <label>First name<input formControlName="first_name" placeholder="John" /></label>
            <label>Last name<input formControlName="last_name" placeholder="Doe" /></label>
          </div>
          <label>Password<input formControlName="password" type="password" placeholder="********" /></label>
          <label class="host-toggle">
            <span>
              <strong>I want to host</strong>
              <small>List your space and earn extra income.</small>
            </span>
            <select formControlName="role">
              <option value="guest">Guest</option>
              <option value="host">Host</option>
            </select>
          </label>
          <p class="terms">By continuing, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.</p>
          @if (error()) {
            <p class="notice">{{ error() }}</p>
          }
          <button type="submit" [disabled]="form.invalid || loading()">{{ loading() ? 'Creating...' : 'Sign Up' }}</button>
        </form>

        <div class="divider"><span>or</span></div>
        <div class="social-grid">
          <button type="button" (click)="socialLogin('Google')"><span>G</span>Google</button>
          <button type="button" (click)="socialLogin('Apple')"><span class="material-symbols-outlined">ios</span>Apple</button>
        </div>

        <p class="auth-switch">Already have an account? <a routerLink="/login">Log in</a></p>
      </div>
    </section>

    @if (notice()) {
      <p class="toast">{{ notice() }}</p>
    }
  `
})
export class RegisterPage {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly loading = signal(false);
  protected readonly error = signal('');
  protected readonly notice = signal('');
  protected readonly form = this.fb.nonNullable.group({
    username: ['', [Validators.required, Validators.pattern(/^[\w.@+-]+$/)]],
    email: ['', [Validators.required, Validators.email]],
    first_name: [''],
    last_name: [''],
    role: ['guest' as 'guest' | 'host'],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  submit(): void {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set('');
    const payload = this.form.getRawValue();
    this.auth.register({
      ...payload,
      username: payload.username.trim(),
      email: payload.email.trim(),
      first_name: payload.first_name.trim(),
      last_name: payload.last_name.trim()
    }).subscribe({
      next: () => this.router.navigateByUrl('/login'),
      error: (error: HttpErrorResponse) => {
        this.error.set(this.formatError(error));
        this.loading.set(false);
      }
    });
  }

  socialLogin(provider: string): void {
    this.notice.set(`${provider} registration is currently unavailable.`);
    window.setTimeout(() => this.notice.set(''), 3000);
  }

  private formatError(error: HttpErrorResponse): string {
    if (error.status === 0) {
      return 'Could not reach the server. Please make sure the Django backend is running.';
    }

    if (typeof error.error === 'string') {
      return error.error;
    }

    if (error.error && typeof error.error === 'object') {
      const messages = Object.entries(error.error).flatMap(([field, value]) => {
        const text = Array.isArray(value) ? value.join(' ') : String(value);
        return `${this.prettyField(field)}: ${text}`;
      });
      if (messages.length) {
        return messages.join(' ');
      }
    }

    return 'Registration failed. Please check your details.';
  }

  private prettyField(field: string): string {
    return field.replaceAll('_', ' ').replace(/^\w/, (char) => char.toUpperCase());
  }
}
