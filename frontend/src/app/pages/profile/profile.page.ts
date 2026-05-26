import { Component, inject } from '@angular/core';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-profile-page',
  template: `
    <section class="page-section narrow">
      <header class="profile-header">
        <span class="eyebrow">Account</span>
        <h1>Your Profile</h1>
      </header>
      
      @if (auth.currentUser(); as user) {
        <div class="profile-card">
          <div class="profile-main">
            <div class="avatar-large">
              @if (user.avatar) {
                <img [src]="user.avatar" [alt]="user.username" />
              } @else {
                <span class="material-symbols-outlined">account_circle</span>
              }
            </div>
            <div class="user-details">
              <h2>{{ user.first_name }} {{ user.last_name }}</h2>
              <p class="username">@{{ user.username }}</p>
              <span class="role-badge">{{ user.role }}</span>
            </div>
          </div>
          
          <hr class="divider" />
          
          <div class="profile-info">
            <div class="info-group">
              <span class="label">Email address</span>
              <p>{{ user.email }}</p>
            </div>
            <div class="info-group">
              <span class="label">Phone number</span>
              <p>{{ user.phone || 'Not provided' }}</p>
            </div>
            <div class="info-group">
              <span class="label">Bio</span>
              <p>{{ user.bio || 'No bio yet. Tell the world about yourself!' }}</p>
            </div>
          </div>
          
          <div class="profile-actions">
            <button class="btn-primary">Edit Profile</button>
            <button class="btn-outline">Security Settings</button>
          </div>
        </div>
      } @else {
        <div class="empty-state">
          <span class="material-symbols-outlined">login</span>
          <h3>Please login</h3>
          <p>You need to be logged in to view and manage your profile settings.</p>
          <a routerLink="/login" class="btn-primary">Login now</a>
        </div>
      }
    </section>
  `,
  styles: [`
    .narrow { max-width: 800px; margin: 0 auto; padding: 64px 24px; }
    .profile-header { margin-bottom: 40px; }
    .eyebrow { color: #ba0036; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; display: block; }
    h1 { font-size: 2.5rem; font-weight: 900; margin: 0; }
    
    .profile-card { background: #fff; border: 1px solid #f0eded; border-radius: 24px; padding: 40px; box-shadow: 0 12px 32px rgba(0,0,0,0.06); }
    
    .profile-main { display: flex; align-items: center; gap: 32px; margin-bottom: 32px; }
    .avatar-large { width: 120px; height: 120px; border-radius: 50%; background: #f6f3f2; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 4px solid #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .avatar-large .material-symbols-outlined { font-size: 80px; color: #ccc; }
    .avatar-large img { width: 100%; height: 100%; object-fit: cover; }
    
    .user-details h2 { font-size: 1.8rem; font-weight: 800; margin: 0 0 4px; }
    .username { color: #5c3f41; font-weight: 600; margin: 0 0 12px; }
    .role-badge { display: inline-block; padding: 6px 16px; background: #fdf2f2; color: #ba0036; border-radius: 99px; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; }
    
    .divider { border: 0; border-top: 1px solid #eee; margin: 32px 0; }
    
    .profile-info { display: grid; gap: 24px; }
    .info-group .label { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: #888; letter-spacing: 0.05em; display: block; margin-bottom: 4px; }
    .info-group p { font-size: 1.1rem; color: #1b1c1c; margin: 0; font-weight: 500; }
    
    .profile-actions { display: flex; gap: 16px; margin-top: 40px; }
    .btn-primary { padding: 14px 32px; background: #ba0036; color: #fff; border: 0; border-radius: 12px; font-weight: 800; cursor: pointer; transition: all 0.2s; }
    .btn-primary:hover { background: #a0002e; transform: translateY(-2px); }
    .btn-outline { padding: 14px 32px; background: transparent; border: 2px solid #f0eded; color: #1b1c1c; border-radius: 12px; font-weight: 800; cursor: pointer; transition: all 0.2s; }
    .btn-outline:hover { background: #f6f3f2; }
    
    .empty-state { text-align: center; padding: 60px 0; }
    .empty-state .material-symbols-outlined { font-size: 64px; color: #ccc; margin-bottom: 16px; }
  `]
})
export class ProfilePage {
  protected readonly auth = inject(AuthService);
}
