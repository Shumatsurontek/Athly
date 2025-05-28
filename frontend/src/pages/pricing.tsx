import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import Link from 'next/link';

const Pricing: React.FC = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const plans = [
    {
      name: 'Gratuit',
      price: '0€',
      frequency: '/mois',
      description: 'Parfait pour commencer',
      features: [
        '3 programmes générés par mois',
        'Chat IA limité (10 messages/mois)',
        'Exercices de base',
        'Support communautaire'
      ],
      cta: 'Commencer gratuitement',
      href: '/generator',
      popular: false,
      color: '#4ECDC4',
      mascot: 'fox'
    },
    {
      name: 'Pro',
      price: '9€',
      frequency: '/mois',
      description: 'Pour les sportifs sérieux',
      features: [
        'Programmes illimités',
        'Chat IA illimité',
        'Tous les exercices',
        'Suivi de progression',
        'Support prioritaire',
        'Analyses détaillées'
      ],
      cta: 'Commencer l\'essai',
      href: '/generator',
      popular: true,
      color: '#FF6B9D',
      mascot: 'robot'
    },
    {
      name: 'Elite',
      price: '19€',
      frequency: '/mois',
      description: 'Pour les athlètes exigeants',
      features: [
        'Tout du plan Pro',
        'Coach IA personnalisé',
        'Programmes de nutrition',
        'Consultation vidéo mensuelle',
        'Programmes de compétition',
        'API pour apps tierces'
      ],
      cta: 'Devenir Elite',
      href: '/contact',
      popular: false,
      color: '#FFD93D',
      mascot: 'both'
    }
  ];

  const faqs = [
    {
      question: 'Puis-je changer de plan à tout moment ?',
      answer: 'Oui, vous pouvez upgrader ou downgrader votre plan à tout moment depuis votre espace personnel. Les changements sont effectifs immédiatement.',
      icon: '🔄'
    },
    {
      question: 'Y a-t-il une période d\'essai ?',
      answer: 'Tous nos plans payants incluent une période d\'essai gratuite de 7 jours, sans engagement. Annulez à tout moment.',
      icon: '⏱️'
    },
    {
      question: 'Comment fonctionne le support ?',
      answer: 'Le plan gratuit bénéficie du support communautaire, tandis que les plans payants ont accès au support prioritaire par email et chat.',
      icon: '💬'
    },
    {
      question: 'Les données sont-elles sécurisées ?',
      answer: 'Absolument ! Vos données sont cryptées et stockées de manière sécurisée. Nous respectons strictement le RGPD.',
      icon: '🔒'
    }
  ];

  const features = [
    {
      title: 'Intelligence Artificielle Avancée',
      description: 'Notre IA analyse vos besoins et crée des programmes personnalisés',
      icon: '🤖',
      gradient: 'linear-gradient(135deg, #FF6B9D, #4ECDC4)'
    },
    {
      title: 'Programmes Multidisciplinaires',
      description: 'Course, musculation, poids du corps - tout en un',
      icon: '🏃‍♂️',
      gradient: 'linear-gradient(135deg, #4ECDC4, #FFD93D)'
    },
    {
      title: 'Suivi en Temps Réel',
      description: 'Analysez vos progrès et ajustez vos objectifs',
      icon: '📊',
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
    <Layout title="Tarifs - Athly" description="Découvrez nos plans tarifaires pour votre coaching sportif IA personnalisé">
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
                  <span>💰 Tarifs Transparents</span>
                </div>
                
                <h1 className="athly-hero-title">
                  Choisissez votre <span className="athly-gradient-text">Plan d'Entraînement</span>
                </h1>
                
                <p className="athly-hero-subtitle">
                  Des tarifs transparents pour tous les niveaux sportifs. 
                  Commencez gratuitement et évoluez selon vos besoins.
                </p>
                
                <div className="athly-hero-stats">
                  <div className="athly-stat">
                    <div className="athly-stat-number">7 jours</div>
                    <div className="athly-stat-label">Essai gratuit</div>
                  </div>
                  <div className="athly-stat">
                    <div className="athly-stat-number">0€</div>
                    <div className="athly-stat-label">Pour commencer</div>
                  </div>
                  <div className="athly-stat">
                    <div className="athly-stat-number">24/7</div>
                    <div className="athly-stat-label">Accès illimité</div>
                  </div>
                </div>
              </div>
              
              <div className="athly-hero-visual">
                <div className="athly-mascot-container">
                  <div className="athly-mascot athly-mascot-robot">
                    <img src="/robot.png" alt="Robot Coach IA" />
                    <div className="athly-mascot-bubble athly-bubble-robot">
                      <p>Prêt à choisir votre plan ? 💪</p>
                    </div>
                  </div>
                  
                  <div className="athly-mascot athly-mascot-fox">
                    <img src="/fox.png" alt="Fox Athly" />
                    <div className="athly-mascot-bubble athly-bubble-fox">
                      <p>Commencez gratuitement ! 🎯</p>
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
                Une technologie d'intelligence artificielle avancée au service de vos objectifs
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

        {/* Pricing Section */}
        <section className="athly-pricing scroll-reveal">
          <div className="container">
            <div className="athly-section-header">
              <h2 className="athly-section-title">
                <span className="athly-gradient-text">Plans</span> et Tarifs
              </h2>
              <p className="athly-section-subtitle">
                Choisissez le plan qui correspond à vos ambitions sportives
              </p>
            </div>
            
            <div className="athly-pricing-grid">
              {plans.map((plan, index) => (
                <div 
                  key={plan.name}
                  className={`athly-pricing-card scroll-reveal ${plan.popular ? 'popular' : ''}`}
                  style={{ animationDelay: `${index * 0.15}s` }}
                >
                  {plan.popular && (
                    <div className="athly-popular-badge">
                      ⭐ Le plus populaire
                    </div>
                  )}
                  
                  <div className="athly-pricing-header">
                    <div className="athly-pricing-mascot">
                      {plan.mascot === 'robot' && (
                        <img src="/robot.png" alt="Robot" />
                      )}
                      {plan.mascot === 'fox' && (
                        <img src="/fox.png" alt="Fox" />
                      )}
                      {plan.mascot === 'both' && (
                        <div className="athly-mascot-duo">
                          <img src="/robot.png" alt="Robot" />
                          <img src="/fox.png" alt="Fox" />
                        </div>
                      )}
                    </div>
                    
                    <h3 className="athly-pricing-name">{plan.name}</h3>
                    <p className="athly-pricing-description">{plan.description}</p>
                    
                    <div className="athly-pricing-price">
                      <span className="athly-price-amount">{plan.price}</span>
                      <span className="athly-price-frequency">{plan.frequency}</span>
                    </div>
                  </div>

                  <ul className="athly-pricing-features">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex}>
                        <span className="athly-check-icon">✓</span>
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <Link href={plan.href} className="athly-pricing-btn">
                    {plan.cta}
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="athly-faq scroll-reveal">
          <div className="container">
            <div className="athly-section-header">
              <h2 className="athly-section-title">
                Questions <span className="athly-gradient-text">Fréquentes</span>
              </h2>
              <p className="athly-section-subtitle">
                Tout ce que vous devez savoir sur nos plans et services
              </p>
            </div>
            
            <div className="athly-faq-grid">
              {faqs.map((faq, index) => (
                <div 
                  key={index}
                  className="athly-faq-card scroll-reveal"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="athly-faq-icon">{faq.icon}</div>
                  <h3 className="athly-faq-question">{faq.question}</h3>
                  <p className="athly-faq-answer">{faq.answer}</p>
                  
                  <div className="athly-faq-mascot">
                    <img 
                      src={index % 2 === 0 ? "/robot.png" : "/fox.png"} 
                      alt="Mascot" 
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
                  Prêt à commencer votre <span className="athly-gradient-text">transformation</span> ?
                </h2>
                <p className="athly-cta-subtitle">
                  Commencez gratuitement dès aujourd'hui et découvrez le pouvoir de l'IA pour votre entraînement
                </p>
              </div>
              
              <div className="athly-cta-actions">
                <Link href="/generator" className="athly-btn athly-btn-primary athly-btn-large">
                  <span>Commencer gratuitement</span>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </Link>
                <Link href="/contact" className="athly-btn athly-btn-outline athly-btn-large">
                  <span>Parler à un expert</span>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Pricing; 