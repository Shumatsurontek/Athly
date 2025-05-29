import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';

const Contact: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    setIsSubmitted(true);
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  const contactMethods = [
    {
      icon: '📧',
      title: 'Email',
      description: 'Nous vous répondons sous 24h',
      value: 'contact@athly.fr',
      href: 'mailto:contact@athly.fr',
      color: '#FF6B9D',
      mascot: 'robot'
    },
    {
      icon: '💬',
      title: 'Chat en direct',
      description: 'Support instantané avec notre IA',
      value: 'Discuter maintenant',
      href: '/chat',
      color: '#4ECDC4',
      mascot: 'fox'
    },
    {
      icon: '📍',
      title: 'Adresse',
      description: 'Notre bureau principal',
      value: 'Paris, France',
      href: 'https://maps.google.com',
      color: '#FFD93D',
      mascot: 'both'
    }
  ];

  const socialLinks = [
    { icon: '📘', name: 'Facebook', href: 'https://facebook.com/athly', color: '#1877F2' },
    { icon: '📷', name: 'Instagram', href: 'https://instagram.com/athly', color: '#E4405F' },
    { icon: '🐦', name: 'Twitter', href: 'https://twitter.com/athly', color: '#1DA1F2' },
    { icon: '💼', name: 'LinkedIn', href: 'https://linkedin.com/company/athly', color: '#0A66C2' },
  ];

  const features = [
    {
      title: 'Support 24/7',
      description: 'Notre équipe et notre IA sont disponibles pour vous aider',
      icon: '🕐',
      gradient: 'linear-gradient(135deg, #FF6B9D, #4ECDC4)'
    },
    {
      title: 'Réponse Rapide',
      description: 'Nous nous engageons à répondre sous 24h maximum',
      icon: '⚡',
      gradient: 'linear-gradient(135deg, #4ECDC4, #FFD93D)'
    },
    {
      title: 'Expertise Technique',
      description: 'Une équipe d\'experts en sport et en technologie',
      icon: '🎯',
      gradient: 'linear-gradient(135deg, #FFD93D, #FF6B9D)'
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

    return () => {
      observer.disconnect();
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div>
      <Head>
        <title>Contact - Athly</title>
        <meta name="description" content="Contactez-nous pour en savoir plus sur Athly, votre coach sportif IA personnel." />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <Layout title="Contact - Athly" description="Contactez-nous pour toute question sur Athly, votre coach sportif IA personnel">
        <div className="athly-home">
          
          {/* Hero Section with Parallax */}
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
                <div className="athly-hero-text" style={{ textAlign: 'center' }}>
                  <div className="athly-hero-badge">
                    <span>💬 Nous sommes là pour vous</span>
                  </div>
                  
                  <h1 className="athly-hero-title">
                    <span className="athly-gradient-text">Contactez</span> notre équipe
                  </h1>
                  
                  <p className="athly-hero-subtitle">
                    Une question ? Un problème ? Une suggestion ? 
                    Notre équipe d'experts est là pour vous accompagner dans votre parcours sportif.
                  </p>
                  
                  <div className="athly-hero-stats">
                    <div className="athly-stat">
                      <div className="athly-stat-number">&lt;24h</div>
                      <div className="athly-stat-label">Temps de réponse</div>
                    </div>
                    <div className="athly-stat">
                      <div className="athly-stat-number">24/7</div>
                      <div className="athly-stat-label">Support IA</div>
                    </div>
                    <div className="athly-stat">
                      <div className="athly-stat-number">100%</div>
                      <div className="athly-stat-label">Satisfaction</div>
                    </div>
                  </div>
                </div>
                
                <div className="athly-hero-visual">
                  <div className="athly-mascot-container">
                    <div className="athly-mascot athly-mascot-robot">
                      <img src="/robot.png" alt="Robot Coach IA" />
                      <div className="athly-mascot-bubble athly-bubble-robot">
                        <p>Je peux vous aider instantanément ! 🤖</p>
                      </div>
                    </div>
                    
                    <div className="athly-mascot athly-mascot-fox">
                      <img src="/fox.png" alt="Fox Athly" />
                      <div className="athly-mascot-bubble athly-bubble-fox">
                        <p>L'équipe humaine aussi ! 🦊</p>
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
                  Un <span className="athly-gradient-text">support</span> exceptionnel
                </h2>
                <p className="athly-section-subtitle">
                  Nous mettons tout en œuvre pour vous offrir la meilleure expérience possible
                </p>
              </div>
              
              <div className="athly-features-grid">
                {features.map((feature, index) => (
                  <div 
                    key={index}
                    className="athly-feature-card scroll-reveal"
                    style={{ 
                      animationDelay: `${index * 0.2}s`,
                      background: feature.gradient + ', var(--bg-glass)'
                    }}
                  >
                    <div className="athly-feature-header">
                      <div className="athly-feature-icon">{feature.icon}</div>
                      <img 
                        src={index % 2 === 0 ? "/robot.png" : "/fox.png"} 
                        alt="Mascot" 
                        className="athly-feature-mascot" 
                      />
                    </div>
                    <h3 className="athly-feature-title">{feature.title}</h3>
                    <p className="athly-feature-description">{feature.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Contact Methods Section */}
          <section className="athly-contact-methods scroll-reveal">
            <div className="container">
              <div className="athly-section-header">
                <h2 className="athly-section-title">
                  <span className="athly-gradient-text">Moyens</span> de contact
                </h2>
                <p className="athly-section-subtitle">
                  Choisissez le canal de communication qui vous convient le mieux
                </p>
              </div>
              
              <div className="athly-contact-methods-grid">
                {contactMethods.map((method, index) => (
                  <a
                    key={method.title}
                    href={method.href}
                    className="athly-contact-method-card scroll-reveal"
                    style={{ animationDelay: `${index * 0.15}s` }}
                    target={method.href.startsWith('http') ? '_blank' : undefined}
                    rel={method.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                  >
                    <div className="athly-contact-method-header">
                      <div className="athly-contact-method-mascot">
                        {method.mascot === 'robot' && (
                          <img src="/robot.png" alt="Robot" />
                        )}
                        {method.mascot === 'fox' && (
                          <img src="/fox.png" alt="Fox" />
                        )}
                        {method.mascot === 'both' && (
                          <div className="athly-mascot-duo">
                            <img src="/robot.png" alt="Robot" />
                            <img src="/fox.png" alt="Fox" />
                          </div>
                        )}
                      </div>
                      
                      <div 
                        className="athly-contact-method-icon"
                        style={{ background: `linear-gradient(135deg, ${method.color}, ${method.color}99)` }}
                      >
                        {method.icon}
                      </div>
                    </div>
                    
                    <h3 className="athly-contact-method-title">{method.title}</h3>
                    <p className="athly-contact-method-description">{method.description}</p>
                    <p className="athly-contact-method-value">{method.value}</p>
                    
                    <div className="athly-contact-method-action">
                      <span>Contacter</span>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </section>

          {/* Contact Form Section */}
          <section className="athly-contact-form-section scroll-reveal">
            <div className="container">
              <div className="athly-contact-form-grid">
                
                {/* Form */}
                <div className="athly-contact-form-container">
                  <div className="athly-form-header">
                    <h2 className="athly-form-title">Envoyez-nous un message</h2>
                    <p className="athly-form-subtitle">
                      Décrivez votre demande et nous vous répondrons rapidement
                    </p>
                  </div>
                  
                  {isSubmitted ? (
                    <div className="athly-success-message">
                      <div className="athly-success-animation">
                        <div className="athly-success-icon">✅</div>
                        <img src="/robot.png" alt="Robot Success" className="athly-success-mascot" />
                      </div>
                      <h3>Message envoyé avec succès !</h3>
                      <p>Merci pour votre message. Notre équipe vous répondra dans les plus brefs délais.</p>
                      <button 
                        className="athly-btn athly-btn-primary"
                        onClick={() => setIsSubmitted(false)}
                      >
                        Envoyer un autre message
                      </button>
                    </div>
                  ) : (
                    <form className="athly-contact-form" onSubmit={handleSubmit}>
                      <div className="athly-form-row">
                        <div className="athly-form-group">
                          <label htmlFor="name">Nom complet</label>
                          <input
                            type="text"
                            id="name"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                            placeholder="Votre nom"
                            className="athly-form-input"
                          />
                        </div>
                        <div className="athly-form-group">
                          <label htmlFor="email">Email</label>
                          <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                            placeholder="votre@email.com"
                            className="athly-form-input"
                          />
                        </div>
                      </div>

                      <div className="athly-form-group">
                        <label htmlFor="subject">Sujet</label>
                        <select
                          id="subject"
                          name="subject"
                          value={formData.subject}
                          onChange={handleInputChange}
                          required
                          className="athly-form-select"
                        >
                          <option value="">Choisissez un sujet</option>
                          <option value="support">Support technique</option>
                          <option value="billing">Facturation</option>
                          <option value="feature">Demande de fonctionnalité</option>
                          <option value="partnership">Partenariat</option>
                          <option value="other">Autre</option>
                        </select>
                      </div>

                      <div className="athly-form-group">
                        <label htmlFor="message">Message</label>
                        <textarea
                          id="message"
                          name="message"
                          value={formData.message}
                          onChange={handleInputChange}
                          required
                          rows={6}
                          placeholder="Décrivez votre demande en détail..."
                          className="athly-form-textarea"
                        />
                      </div>

                      <button 
                        type="submit" 
                        className={`athly-btn athly-btn-primary athly-btn-large ${isSubmitting ? 'loading' : ''}`}
                        disabled={isSubmitting}
                        style={{ width: '100%' }}
                      >
                        {isSubmitting ? (
                          <>
                            <div className="athly-spinner"></div>
                            Envoi en cours...
                          </>
                        ) : (
                          <>
                            Envoyer le message
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                              <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                          </>
                        )}
                      </button>
                    </form>
                  )}
                </div>

                {/* Contact Info Sidebar */}
                <div className="athly-contact-info">
                  <div className="athly-contact-info-card">
                    <h3>Informations utiles</h3>
                    
                    <div className="athly-info-item">
                      <div className="athly-info-icon">⏰</div>
                      <div>
                        <h4>Horaires de support</h4>
                        <p>Lun-Ven: 9h-18h<br />Sam-Dim: Support IA uniquement</p>
                      </div>
                    </div>
                    
                    <div className="athly-info-item">
                      <div className="athly-info-icon">🌍</div>
                      <div>
                        <h4>Langue</h4>
                        <p>Français, Anglais<br />Support IA multilingue</p>
                      </div>
                    </div>
                    
                    <div className="athly-info-item">
                      <div className="athly-info-icon">🚀</div>
                      <div>
                        <h4>Urgence</h4>
                        <p>Pour les urgences techniques,<br />utilisez le chat IA</p>
                      </div>
                    </div>
                  </div>

                  <div className="athly-social-section">
                    <h3>Suivez-nous</h3>
                    <div className="athly-social-links">
                      {socialLinks.map((social, index) => (
                        <a
                          key={social.name}
                          href={social.href}
                          className="athly-social-link"
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{ animationDelay: `${index * 0.1}s` }}
                        >
                          <span className="athly-social-icon">{social.icon}</span>
                          <span>{social.name}</span>
                        </a>
                      ))}
                    </div>
                  </div>

                  <div className="athly-contact-mascots">
                    <img src="/fox.png" alt="Fox" className="athly-contact-mascot" />
                  </div>
                </div>

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
                    Besoin d'aide <span className="athly-gradient-text">immédiatement</span> ?
                  </h2>
                  <p className="athly-cta-subtitle">
                    Notre coach IA est disponible 24/7 pour répondre à toutes vos questions
                  </p>
                </div>
                
                <div className="athly-cta-actions">
                  <a href="/chat" className="athly-btn athly-btn-primary athly-btn-large">
                    <img src="/robot.png" alt="Robot" width="20" height="20" />
                    <span>Parler au coach IA</span>
                  </a>
                  <a href="/generator" className="athly-btn athly-btn-outline athly-btn-large">
                    <span>Créer un programme</span>
                  </a>
                </div>
              </div>
            </div>
          </section>
        </div>
      </Layout>
    </div>
  );
};

export default Contact; 