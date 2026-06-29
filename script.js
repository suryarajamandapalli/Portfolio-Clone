document.addEventListener('DOMContentLoaded', () => {
    initPreloader();
    initCanvas();
    initTiltCards();
    initScrollReveal();
});

/* ==========================================
   1. PRELOADER LOGIC
   ========================================== */
function initPreloader() {
    const preloader = document.getElementById('preloader');
    const progressBar = document.querySelector('.loader-bar');
    const progressText = document.querySelector('.loader-percentage');
    const loaderStatus = document.querySelector('.loader-text');

    if (!preloader) return;

    let progress = 0;
    const duration = 2800; // 2.8 seconds total loader duration
    const intervalTime = 30;
    const step = 100 / (duration / intervalTime);

    const statusMessages = [
        { limit: 20, message: "Initializing Loom..." },
        { limit: 50, message: "Spinning Threads..." },
        { limit: 80, message: "Weaving Digital Mesh..." },
        { limit: 95, message: "Polishing Nodes..." },
        { limit: 100, message: "Web Complete." }
    ];

    const timer = setInterval(() => {
        progress += step;
        if (progress >= 100) {
            progress = 100;
            clearInterval(timer);
            
            // Finalize status and trigger exit
            loaderStatus.textContent = "Web Complete.";
            progressBar.style.width = '100%';
            progressText.textContent = '100';
            
            setTimeout(() => {
                preloader.classList.add('fade-out');
                document.body.style.overflowY = 'auto'; // Re-enable scrolling
            }, 400);
        } else {
            // Update progress bar & text
            progressBar.style.width = `${progress}%`;
            progressText.textContent = Math.floor(progress);

            // Update status text based on progress
            const currentStatus = statusMessages.find(msg => progress <= msg.limit);
            if (currentStatus) {
                loaderStatus.textContent = currentStatus.message;
            }
        }
    }, intervalTime);
}

/* ==========================================
   2. INTERACTIVE CANVAS SPIDER WEB
   ========================================== */
function initCanvas() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const particles = [];
    // Adjust density based on screen size
    const particleCount = Math.min(80, Math.floor((width * height) / 15000));
    const connectionDistance = 140;
    const mouse = { x: null, y: null, radius: 180 };

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    window.addEventListener('mouseout', () => {
        mouse.x = null;
        mouse.y = null;
    });

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            // Slow, organic floating speeds
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.radius = Math.random() * 2 + 1.5;
        }

        update() {
            // Bounce off boundaries
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;

            this.x += this.vx;
            this.y += this.vy;

            // Mouse attraction (magnetic web effect)
            if (mouse.x !== null) {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < mouse.radius) {
                    const force = (mouse.radius - dist) / mouse.radius;
                    // Gently pull toward cursor
                    this.x += (dx / dist) * force * 0.6;
                    this.y += (dy / dist) * force * 0.6;
                }
            }
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(226, 169, 149, 0.7)';
            ctx.fill();
        }
    }

    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        // Draw radial grid background
        const grad = ctx.createRadialGradient(width / 2, height / 2, 10, width / 2, height / 2, Math.max(width, height));
        grad.addColorStop(0, 'rgba(10, 8, 8, 1)');
        grad.addColorStop(1, 'rgba(5, 5, 5, 1)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, width, height);

        // Draw subtle glowing circle around cursor
        if (mouse.x !== null) {
            ctx.beginPath();
            ctx.arc(mouse.x, mouse.y, mouse.radius * 0.6, 0, Math.PI * 2);
            const mouseGrad = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, mouse.radius * 0.6);
            mouseGrad.addColorStop(0, 'rgba(226, 169, 149, 0.04)');
            mouseGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = mouseGrad;
            ctx.fill();
        }

        // Update & Draw particles
        particles.forEach(p => {
            p.update();
            p.draw();
        });

        // Draw connections (Web weaving)
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < connectionDistance) {
                    // Alpha gets stronger the closer they are
                    const alpha = (1 - dist / connectionDistance) * 0.15;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(226, 169, 149, ${alpha})`;
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }

            // Connection to mouse
            if (mouse.x !== null) {
                const dx = particles[i].x - mouse.x;
                const dy = particles[i].y - mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < mouse.radius) {
                    const alpha = (1 - dist / mouse.radius) * 0.25;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(mouse.x, mouse.y);
                    ctx.strokeStyle = `rgba(226, 169, 149, ${alpha})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    animate();
}

/* ==========================================
   3. 3D TILT EFFECT & GLOWS ON CARDS
   ========================================== */
function initTiltCards() {
    const cards = document.querySelectorAll('.service-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x coordinate within the card
            const y = e.clientY - rect.top;  // y coordinate within the card

            // Set custom properties for hover radial glow
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);

            // Calculate rotation angles
            const cardWidth = rect.width;
            const cardHeight = rect.height;
            const centerX = cardWidth / 2;
            const centerY = cardHeight / 2;
            
            // Max rotation is 10 degrees
            const rotateX = ((centerY - y) / centerY) * 8;
            const rotateY = ((x - centerX) / centerX) * 8;

            card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });
}

/* ==========================================
   4. SCROLL REVEAL (INTERSECTION OBSERVER)
   ========================================== */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Reveal once
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
}
