import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Home: React.FC = () => {
  const [activeFeature, setActiveFeature] = useState<string>('chat');
  
  const features = [
    {
      id: 'chat',
      title: 'Chat Intelligent',
      description: 'Posez vos questions et obtenez des conseils personnalisés grâce à notre IA coach sportif.',
      icon: '💬'
    },
    {
      id: 'program',
      title: 'Programmes Personnalisés',
      description: 'Générez des programmes d\'entraînement sur mesure pour atteindre vos objectifs sportifs.',
      icon: '📊'
    },
    {
      id: 'multi',
      title: 'Approche Multisport',
      description: 'Combinez course à pied, musculation et exercices au poids du corps dans un programme cohérent.',
      icon: '🏃‍♂️'
    }
  ];
  
  return (
    <div className="home-page">
      <Head>
        <title>Athly - Votre coach sportif IA personnel</title>
        <meta name="description" content="Athly est une application d'IA qui génère des programmes d'entraînement personnalisés pour la course à pied, la musculation et les exercices au poids du corps" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <header className="hero-section">
        <div className="container">
          <div className="logo-container">
            <img 
              src="/logo.png" 
              alt="Athly Logo" 
              width="120" 
              height="120"
            />
            <h1 className="logo-text">Athly</h1>
          </div>
          
          <h2 className="hero-title">Votre coach sportif IA personnel</h2>
          <p className="hero-subtitle">
            Générez des programmes d'entraînement personnalisés et recevez des conseils adaptés à vos objectifs
          </p>
          
          <div className="cta-buttons">
            <Link href="/generator" className="primary-button">
              Générer mon programme
            </Link>
            <Link href="/chat" className="secondary-button">
              Discuter avec le coach
            </Link>
          </div>
        </div>
      </header>
      
      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Pourquoi choisir Athly?</h2>
          
          <div className="features-grid">
            {features.map(feature => (
              <div 
                key={feature.id}
                className={`feature-card ${activeFeature === feature.id ? 'active' : ''}`}
                onClick={() => setActiveFeature(feature.id)}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      <section className="disciplines-section">
        <div className="container">
          <h2 className="section-title">Disciplines</h2>
          
          <div className="disciplines-list">
            <div className="discipline-item">
              <div className="discipline-icon">🏃‍♂️</div>
              <h3>Course à pied</h3>
              <p>Des programmes d'endurance adaptés à votre niveau, du débutant au confirmé.</p>
            </div>
            
            <div className="discipline-item">
              <div className="discipline-icon">💪</div>
              <h3>Poids de Corps</h3>
              <p>Entraînez-vous n'importe où avec des exercices efficaces sans matériel.</p>
            </div>
            
            <div className="discipline-item">
              <div className="discipline-icon">🏋️</div>
              <h3>Musculation</h3>
              <p>Développez force et masse musculaire avec des programmes structurés.</p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="testimonials-section">
        <div className="container">
          <h2 className="section-title">Ce que disent nos utilisateurs</h2>
          
          <div className="testimonials-slider">
            <div className="testimonial-card">
              <p className="testimonial-text">
                "Athly m'a permis de combiner efficacement course à pied et musculation. Mes performances se sont nettement améliorées en seulement 12 semaines."
              </p>
              <div className="testimonial-author">Thomas, 32 ans</div>
            </div>
            
            <div className="testimonial-card">
              <p className="testimonial-text">
                "En tant que débutante, j'avais peur de me blesser. Le programme généré était parfaitement adapté à mon niveau et j'ai progressé en toute sécurité."
              </p>
              <div className="testimonial-author">Sophie, 28 ans</div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="cta-section">
        <div className="container">
          <h2 className="cta-title">Prêt à transformer votre entraînement?</h2>
          <p className="cta-text">Générez votre programme personnalisé dès maintenant</p>
          
          <div className="cta-buttons">
            <Link href="/pricing" className="primary-button">
              Voir les forfaits
            </Link>
            <Link href="/generator" className="secondary-button">
              Essayer gratuitement
            </Link>
          </div>
        </div>
      </section>
      
      <footer className="footer">
        <div className="container">
          <div className="footer-logo">
            <img 
              src="/logo.png" 
              alt="Athly Logo" 
              width="60" 
              height="60"
            />
            <span>Athly</span>
          </div>
          
          <div className="footer-links">
            <div className="footer-links-column">
              <h4>Navigation</h4>
              <Link href="/">Accueil</Link>
              <Link href="/generator">Générateur</Link>
              <Link href="/chat">Chat</Link>
              <Link href="/pricing">Tarifs</Link>
            </div>
            
            <div className="footer-links-column">
              <h4>Contact</h4>
              <Link href="/contact">Nous contacter</Link>
              <a href="https://instagram.com/athly" target="_blank" rel="noopener noreferrer">Instagram</a>
              <a href="https://wa.me/votrenuméro" target="_blank" rel="noopener noreferrer">WhatsApp</a>
            </div>
            
            <div className="footer-links-column">
              <h4>Légal</h4>
              <Link href="/terms">Conditions d'utilisation</Link>
              <Link href="/privacy">Politique de confidentialité</Link>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>© {new Date().getFullYear()} Athly. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home; 