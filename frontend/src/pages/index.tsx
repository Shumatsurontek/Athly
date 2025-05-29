import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Link from 'next/link';

const Home: React.FC = () => {
  const [activeFeature, setActiveFeature] = useState<string>('chat');
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  
  const features = [
    {
      id: 'chat',
      title: 'Coach IA Intelligent',
      description: 'Discutez avec notre IA coach sportif pour obtenir des conseils personnalisés et des réponses immédiates à vos questions.',
      icon: '🤖',
      mascot: 'robot',
      gradient: 'linear-gradient(135deg, #FF6B9D, #4ECDC4)'
    },
    {
      id: 'program',
      title: 'Programmes Personnalisés',
      description: 'Générez instantanément des programmes d\'entraînement sur mesure adaptés à votre niveau et vos objectifs.',
      icon: '📊',
      mascot: 'fox',
      gradient: 'linear-gradient(135deg, #4ECDC4, #FFD93D)'
    },
    {
      id: 'multi',
      title: 'Approche Multisport',
      description: 'Combinez harmonieusement course à pied, musculation et exercices au poids du corps.',
      icon: '🏃‍♂️',
      mascot: 'both',
      gradient: 'linear-gradient(135deg, #FFD93D, #FF6B9D)'
    }
  ];

  const disciplines = [
    {
      title: 'Course à pied',
      description: 'Programmes d\'endurance personnalisés, du 5K au marathon',
      icon: '🏃‍♂️',
      color: '#FF6B9D',
      stats: '+2000 coureurs accompagnés'
    },
    {
      title: 'Poids de Corps',
      description: 'Entraînements efficaces sans matériel, partout et à tout moment',
      icon: '💪',
      color: '#4ECDC4',
      stats: '+1500 programmes générés'
    },
    {
      title: 'Musculation',
      description: 'Plans structurés pour développer force et masse musculaire',
      icon: '🏋️',
      color: '#FFD93D',
      stats: '+800 transformations'
    }
  ];

  const testimonials = [
    {
      text: "Athly a transformé ma façon de m'entraîner. L'IA comprend vraiment mes besoins et s'adapte à mes progrès. Mes performances ont explosé !",
      author: "Thomas M.",
      role: "Coureur amateur",
      avatar: "👨‍💼",
      rating: 5
    },
    {
      text: "En tant que débutante, j'avais peur de me blesser. Les programmes générés sont parfaitement adaptés et la progression est naturelle.",
      author: "Sophie L.",
      role: "Débutante fitness",
      avatar: "👩‍🎓",
      rating: 5
    },
    {
      text: "L'approche multisport est géniale ! Je combine maintenant course et musculation de façon intelligente, sans surmenage.",
      author: "Marc D.",
      role: "Triathlète",
      avatar: "👨‍🔬",
      rating: 5
    }
  ];

  useEffect(() => {
    // Mouse parallax effect
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 100,
        y: (e.clientY / window.innerHeight) * 100
      });
    };

    // Scroll reveal animation
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
        }
      });
    }, observerOptions);

    const scrollElements = document.querySelectorAll('.scroll-reveal');
    scrollElements.forEach(el => observer.observe(el));

    window.addEventListener('mousemove', handleMouseMove);

    // Auto-rotate features
    const interval = setInterval(() => {
      setActiveFeature(prev => {
        const currentIndex = features.findIndex(f => f.id === prev);
        const nextIndex = (currentIndex + 1) % features.length;
        return features[nextIndex].id;
      });
    }, 4000);

    return () => {
      observer.disconnect();
      window.removeEventListener('mousemove', handleMouseMove);
      clearInterval(interval);
    };
  }, []);
  
  return (
    <Layout>
      <div className="athly-home">
        
        {/* Hero Section with Mascots */}
        <section className="athly-hero">
          <div className="athly-hero-bg">
            <div 
              className="athly-parallax-element athly-parallax-1"
              style={{
                transform: `translate(${mousePosition.x * 0.02}px, ${mousePosition.y * 0.02}px)`
              }}
            />
            <div 
              className="athly-parallax-element athly-parallax-2"
              style={{
                transform: `translate(${mousePosition.x * -0.015}px, ${mousePosition.y * -0.015}px)`
              }}
            />
          </div>
          
          <div className="container">
            <div className="athly-hero-content">
              <div className="athly-hero-text">
                <div className="athly-hero-badge">
                  <span>🚀 IA Nouvelle Génération</span>
                </div>
                
                <h1 className="athly-hero-title">
                  Votre <span className="athly-gradient-text">Coach Sportif IA</span><br />
                  Personnel et Intelligent
                </h1>
                
                <p className="athly-hero-subtitle">
                  Transformez votre entraînement avec l'intelligence artificielle. 
                  Programmes personnalisés, conseils en temps réel, et accompagnement 24/7.
                </p>
                
                <div className="athly-hero-stats">
                  <div className="athly-stat">
                    <div className="athly-stat-number">4.8/5</div>
                    <div className="athly-stat-label">Note utilisateurs</div>
                  </div>
                  <div className="athly-stat">
                    <div className="athly-stat-number">5K+</div>
                    <div className="athly-stat-label">Programmes générés</div>
                  </div>
                  <div className="athly-stat">
                    <div className="athly-stat-number">24/7</div>
                    <div className="athly-stat-label">Assistance IA</div>
                  </div>
                </div>
                
                <div className="athly-hero-actions">
                  <Link href="/generator" className="athly-btn athly-btn-primary">
                    <span>Commencer maintenant</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </Link>
                  <Link href="/chat" className="athly-btn athly-btn-secondary">
                    <img src="/robot.png" alt="Robot" width="20" height="20" />
                    <span>Discuter avec l'IA</span>
                  </Link>
                </div>
              </div>
              
              <div className="athly-hero-visual">
                <div className="athly-mascot-container">
                  <div className="athly-mascot athly-mascot-robot">
                    <img src="/robot.png" alt="Robot Coach IA" />
                    <div className="athly-mascot-bubble athly-bubble-robot">
                      <p>Prêt pour un entraînement personnalisé ? 🚀</p>
                    </div>
                  </div>
                  
                  <div className="athly-mascot athly-mascot-fox">
                    <img src="/fox.png" alt="Fox Athly" />
                    <div className="athly-mascot-bubble athly-bubble-fox">
                      <p>Atteignons vos objectifs ensemble ! 🦊</p>
                    </div>
                  </div>
                  
                  <div className="athly-hero-logo">
                    <img src="/logo.png" alt="Athly Logo" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Features Section */}
        <section className="athly-features scroll-reveal">
          <div className="container">
            <div className="athly-section-header">
              <h2 className="athly-section-title">
                Pourquoi choisir <span className="athly-gradient-text">Athly</span> ?
              </h2>
              <p className="athly-section-subtitle">
                Une technologie d'intelligence artificielle avancée au service de vos objectifs sportifs
              </p>
            </div>
            
            <div className="athly-features-grid">
              {features.map((feature, index) => (
                <div 
                  key={feature.id}
                  className={`athly-feature-card ${activeFeature === feature.id ? 'active' : ''}`}
                  onClick={() => setActiveFeature(feature.id)}
                  style={{ 
                    animationDelay: `${index * 0.2}s`,
                    background: activeFeature === feature.id ? feature.gradient : ''
                  }}
                >
                  <div className="athly-feature-header">
                    <div className="athly-feature-icon">{feature.icon}</div>
                    {feature.mascot === 'robot' && (
                      <img src="/robot.png" alt="Robot" className="athly-feature-mascot" />
                    )}
                    {feature.mascot === 'fox' && (
                      <img src="/fox.png" alt="Fox" className="athly-feature-mascot" />
                    )}
                    {feature.mascot === 'both' && (
                      <div className="athly-feature-mascots">
                        <img src="/robot.png" alt="Robot" className="athly-feature-mascot-small" />
                        <img src="/fox.png" alt="Fox" className="athly-feature-mascot-small" />
                      </div>
                    )}
                  </div>
                  <h3 className="athly-feature-title">{feature.title}</h3>
                  <p className="athly-feature-description">{feature.description}</p>
                  
                  <div className="athly-feature-progress">
                    <div 
                      className="athly-feature-progress-bar"
                      style={{ 
                        width: activeFeature === feature.id ? '100%' : '0%',
                        background: feature.gradient
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Disciplines Section */}
        <section className="athly-disciplines scroll-reveal">
          <div className="container">
            <div className="athly-section-header">
              <h2 className="athly-section-title">
                <span className="athly-gradient-text">Disciplines</span> Supportées
              </h2>
              <p className="athly-section-subtitle">
                Une approche complète pour tous vos objectifs sportifs
              </p>
            </div>
            
            <div className="athly-disciplines-grid">
              {disciplines.map((discipline, index) => (
                <div 
                  key={index}
                  className="athly-discipline-card scroll-reveal"
                  style={{ animationDelay: `${index * 0.15}s` }}
                >
                  <div className="athly-discipline-header">
                    <div 
                      className="athly-discipline-icon"
                      style={{ background: `linear-gradient(135deg, ${discipline.color}, ${discipline.color}99)` }}
                    >
                      {discipline.icon}
                    </div>
                    <div className="athly-discipline-stats">
                      {discipline.stats}
                    </div>
                  </div>
                  
                  <h3 className="athly-discipline-title">{discipline.title}</h3>
                  <p className="athly-discipline-description">{discipline.description}</p>
                  
                  <div className="athly-discipline-action">
                    <Link href="/generator" className="athly-discipline-btn">
                      Explorer
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Testimonials Section */}
        <section className="athly-testimonials scroll-reveal">
          <div className="container">
            <div className="athly-section-header">
              <h2 className="athly-section-title">
                Ce que disent nos <span className="athly-gradient-text">athlètes</span>
              </h2>
              <p className="athly-section-subtitle">
                Des transformations réelles, des résultats mesurables
              </p>
            </div>
            
            <div className="athly-testimonials-grid">
              {testimonials.map((testimonial, index) => (
                <div 
                  key={index}
                  className="athly-testimonial-card scroll-reveal"
                  style={{ animationDelay: `${index * 0.2}s` }}
                >
                  <div className="athly-testimonial-content">
                    <div className="athly-testimonial-rating">
                      {Array(testimonial.rating).fill(0).map((_, i) => (
                        <span key={i} className="athly-star">⭐</span>
                      ))}
                    </div>
                    
                    <p className="athly-testimonial-text">"{testimonial.text}"</p>
                    
                    <div className="athly-testimonial-author">
                      <div className="athly-testimonial-avatar">
                        {testimonial.avatar}
                      </div>
                      <div className="athly-testimonial-info">
                        <div className="athly-testimonial-name">{testimonial.author}</div>
                        <div className="athly-testimonial-role">{testimonial.role}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="athly-testimonial-mascot">
                    <img 
                      src={index % 2 === 0 ? "/robot.png" : "/fox.png"} 
                      alt={index % 2 === 0 ? "Robot" : "Fox"} 
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* CTA Section */}
        <section className="athly-cta scroll-reveal">
          <div className="container">
            <div className="athly-cta-content">
              <div className="athly-cta-mascots">
                <img src="/robot.png" alt="Robot" className="athly-cta-robot" />
                <img src="/fox.png" alt="Fox" className="athly-cta-fox" />
              </div>
              
              <div className="athly-cta-text">
                <h2 className="athly-cta-title">
                  Prêt à transformer votre <span className="athly-gradient-text">entraînement</span> ?
                </h2>
                <p className="athly-cta-subtitle">
                  Rejoignez des milliers d'athlètes qui ont déjà révolutionné leur approche du sport avec Athly
                </p>
              </div>
              
              <div className="athly-cta-actions">
                <Link href="/generator" className="athly-btn athly-btn-primary athly-btn-large">
                  <span>Générer mon programme</span>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </Link>
                <Link href="/pricing" className="athly-btn athly-btn-outline athly-btn-large">
                  <span>Voir les forfaits</span>
                </Link>
              </div>
            </div>
          </div>
        </section>
        
        {/* Enhanced Footer */}
        <footer className="athly-footer">
          <div className="container">
            <div className="athly-footer-content">
              <div className="athly-footer-brand">
                <div className="athly-footer-logo">
                  <img src="/logo.png" alt="Athly Logo" />
                  <span>Athly</span>
                </div>
                <p className="athly-footer-tagline">
                  L'intelligence artificielle au service de votre forme physique
                </p>
                <div className="athly-footer-mascots">
                  <img src="/robot.png" alt="Robot" />
                  <img src="/fox.png" alt="Fox" />
                </div>
              </div>
              
              <div className="athly-footer-links">
                <div className="athly-footer-column">
                  <h4>Produit</h4>
                  <Link href="/generator">Générateur</Link>
                  <Link href="/chat">Chat IA</Link>
                  <Link href="/pricing">Tarifs</Link>
                </div>
                
                <div className="athly-footer-column">
                  <h4>Support</h4>
                  <Link href="/contact">Contact</Link>
                  <Link href="/help">Aide</Link>
                  <Link href="/faq">FAQ</Link>
                </div>
                
                <div className="athly-footer-column">
                  <h4>Légal</h4>
                  <Link href="/terms">CGU</Link>
                  <Link href="/privacy">Confidentialité</Link>
                  <Link href="/cookies">Cookies</Link>
                </div>
                
                <div className="athly-footer-column">
                  <h4>Communauté</h4>
                  <a href="#" target="_blank">Instagram</a>
                  <a href="#" target="_blank">Twitter</a>
                  <a href="#" target="_blank">Discord</a>
                </div>
              </div>
            </div>
            
            <div className="athly-footer-bottom">
              <p>© {new Date().getFullYear()} Athly. Tous droits réservés.</p>
              <div className="athly-footer-badges">
                <span className="athly-badge">🚀 IA Powered</span>
                <span className="athly-badge">🔒 Sécurisé</span>
                <span className="athly-badge">⚡ Instantané</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </Layout>
  );
};

export default Home; 