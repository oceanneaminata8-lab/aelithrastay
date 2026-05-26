import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-login-page',
  imports: [ReactiveFormsModule, RouterLink],
  template: `
    <section class="auth-shell">
      <div class="auth-card">
        <div class="auth-card-head">
          <div class="auth-mark">
            <span class="material-symbols-outlined">domain</span>
          </div>
          <h1>Welcome back</h1>
          <p>Login to manage your trips or host your home.</p>
        </div>

        <form [formGroup]="form" (ngSubmit)="submit()">
          <label>Username<input formControlName="username" placeholder="your username" /></label>
          <label>
            <span class="label-row">Password <a href="#">Forgot password?</a></span>
            <input formControlName="password" type="password" placeholder="Enter your password" />
          </label>
          <label class="check-row">
            <input type="checkbox" />
            <span>Remember me</span>
          </label>
          @if (error()) {
            <p class="notice">{{ error() }}</p>
          }
          <button type="submit" [disabled]="form.invalid || loading()">{{ loading() ? 'Signing in...' : 'Log In' }}</button>
        </form>

        <div class="divider"><span>or continue with</span></div>
        <div class="social-grid">
          <button type="button" (click)="socialLogin('Google')"><span>G</span>Google</button>
          <button type="button" (click)="socialLogin('Apple')"><span class="material-symbols-outlined">ios</span>Apple</button>
        </div>

        <p class="auth-switch">Don't have an account? <a routerLink="/register">Sign up</a></p>
      </div>
    </section>

    @if (notice()) {
      <p class="toast">{{ notice() }}</p>
    }
  `
})
export class LoginPage {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly loading = signal(false);
  protected readonly error = signal('');
  protected readonly notice = signal('');
  protected readonly form = this.fb.nonNullable.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });

  submit(): void {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set('');
    const { username, password } = this.form.getRawValue();
    this.auth.login(username, password).subscribe({
      next: () => {
        this.auth.loadMe().subscribe({
          next: () => this.router.navigateByUrl('/'),
          error: () => this.router.navigateByUrl('/')
        });
      },
      error: () => {
        this.error.set('Invalid username or password.');
        this.loading.set(false);
      }
    });
  }

  socialLogin(provider: string): void {
    this.notice.set(`${provider} login is currently unavailable.`);
    window.setTimeout(() => this.notice.set(''), 3000);
  }
}
