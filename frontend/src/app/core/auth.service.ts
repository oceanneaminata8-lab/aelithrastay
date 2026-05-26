import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { API_BASE_URL } from './api';
import { Page, User } from './models';

interface TokenResponse {
  access: string;
  refresh: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser = signal<User | null>(this.loadStoredUser());

  constructor(private http: HttpClient) {}

  register(payload: Partial<User> & { password: string }): Observable<User> {
    return this.http.post<User>(`${API_BASE_URL}/auth/register/`, payload);
  }

  login(username: string, password: string): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${API_BASE_URL}/auth/login/`, { username, password }).pipe(
      tap((tokens) => {
        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
      })
    );
  }

  loadMe(): Observable<Page<User>> {
    return this.http.get<Page<User>>(`${API_BASE_URL}/users/`).pipe(
      tap((page) => {
        const user = page.results[0] ?? null;
        this.currentUser.set(user);
        if (user) {
          localStorage.setItem('current_user', JSON.stringify(user));
        }
      })
    );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
    this.currentUser.set(null);
  }

  isLoggedIn(): boolean {
    return Boolean(localStorage.getItem('access_token'));
  }

  private loadStoredUser(): User | null {
    const stored = localStorage.getItem('current_user');
    return stored ? JSON.parse(stored) : null;
  }
}
