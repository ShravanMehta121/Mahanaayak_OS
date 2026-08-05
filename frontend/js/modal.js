/**
 * MAHANAYAK OS — Reusable Modal Component Controller
 * Handles fullscreen modal dialog creation, backdrop blur, ESC key dismiss, and scroll lock.
 */

const Modal = {
  backdrop: null,
  dialog: null,
  body: null,
  title: null,

  init() {
    if (this.backdrop) return;

    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');

    backdrop.innerHTML = `
      <div class="modal-dialog" role="dialog" aria-modal="true">
        <div class="modal-header">
          <h2 class="modal-title" id="modalTitle"></h2>
          <button class="modal-close" type="button" aria-label="Close modal">&times;</button>
        </div>
        <div class="modal-body" id="modalBody"></div>
      </div>
    `;

    document.body.appendChild(backdrop);

    this.backdrop = backdrop;
    this.dialog = backdrop.querySelector('.modal-dialog');
    this.title = backdrop.querySelector('#modalTitle');
    this.body = backdrop.querySelector('#modalBody');

    const closeBtn = backdrop.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => this.close());

    // Dismiss on backdrop click
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) this.close();
    });

    // Dismiss on ESC key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen()) {
        this.close();
      }
    });
  },

  /**
   * Opens modal with custom title and HTML content.
   * @param {{title: string, contentHtml: string}} options 
   */
  open({ title, contentHtml }) {
    this.init();

    if (this.title) this.title.innerHTML = title || 'Details';
    if (this.body) this.body.innerHTML = contentHtml || '';

    this.backdrop.classList.add('open');
    this.backdrop.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  },

  close() {
    if (!this.backdrop) return;

    this.backdrop.classList.remove('open');
    this.backdrop.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  },

  isOpen() {
    return Boolean(this.backdrop && this.backdrop.classList.contains('open'));
  }
};

window.Modal = Modal;
