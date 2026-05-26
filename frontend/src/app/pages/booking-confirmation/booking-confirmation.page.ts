import { CurrencyPipe, DatePipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Booking } from '../../core/models';
import { BookingService } from '../../core/booking.service';

@Component({
  selector: 'app-booking-confirmation-page',
  imports: [CurrencyPipe, DatePipe, RouterLink],
  template: `
    <section class="confirmation-page">
      <header class="confirm-hero">
        <div class="confirm-icon"><span class="material-symbols-outlined">check_circle</span></div>
        <h1>Your reservation is confirmed!</h1>
        <p>A confirmation email is on its way to your inbox.</p>
        <span class="confirm-code">Confirmation Code: {{ code() }}</span>
      </header>

      @if (booking(); as item) {
        <article class="confirm-card">
          <section class="confirm-property">
            <img src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=900&q=85" [alt]="item.property_title" />
            <div>
              <span class="eyebrow">AelithraStay reservation</span>
              <h2>{{ item.property_title }}</h2>
              <p class="muted">Hosted stay · {{ item.status }}</p>
              <div class="host-mini">
                <span class="material-symbols-outlined">account_circle</span>
                <div>
                  <strong>Your host is ready</strong>
                  <p>Check-in details will be shared before arrival.</p>
                </div>
              </div>
            </div>
          </section>

          <section class="confirm-summary">
            <div>
              <h3>Reservation Details</h3>
              <p><span class="material-symbols-outlined">calendar_today</span>{{ item.check_in | date:'mediumDate' }} to {{ item.check_out | date:'mediumDate' }}</p>
              <p><span class="material-symbols-outlined">group</span>{{ item.guests }} guests · {{ item.nights }} nights</p>
            </div>
            <div>
              <h3>Price Breakdown</h3>
              <div class="price-line"><span>Stay total</span><strong>{{ item.total_price | currency:'XAF' }}</strong></div>
              <div class="price-line"><span>Status</span><strong>{{ item.status }}</strong></div>
            </div>
          </section>

          <footer class="confirm-actions">
            <a routerLink="/bookings"><span class="material-symbols-outlined">flight_takeoff</span>View Trips</a>
            <a routerLink="/profile"><span class="material-symbols-outlined">chat_bubble</span>Contact Host</a>
            <button type="button" (click)="print()"><span class="material-symbols-outlined">picture_as_pdf</span>Print PDF</button>
          </footer>
        </article>
      } @else {
        <p class="notice">Loading confirmation...</p>
      }

      <section class="help-card-grid">
        <article><span class="material-symbols-outlined">location_on</span><h3>Getting there</h3><p>Check your email for map and arrival instructions.</p></article>
        <article><span class="material-symbols-outlined">policy</span><h3>Cancellation policy</h3><p>Review your trip policies before making changes.</p></article>
        <article><span class="material-symbols-outlined">help</span><h3>Need help?</h3><p>Reach out to support from your profile anytime.</p></article>
      </section>
    </section>
  `
})
export class BookingConfirmationPage {
  private readonly route = inject(ActivatedRoute);
  private readonly bookingsApi = inject(BookingService);

  protected readonly booking = signal<Booking | null>(null);
  protected readonly code = signal('AEL-' + Math.random().toString(36).slice(2, 10).toUpperCase());

  constructor() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.bookingsApi.detail(id).subscribe((booking) => this.booking.set(booking));
  }

  print(): void {
    window.print();
  }
}
