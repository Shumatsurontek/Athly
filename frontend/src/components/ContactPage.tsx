import React from 'react';

interface PricingOption {
  id: string;
  title: string;
  price: number;
  frequency: string;
  features: string[];
  isPopular?: boolean;
}

const ContactPage: React.FC = () => {
  const pricingOptions: PricingOption[] = [
    {
      id: 'basic',
      title: 'Coaching Basique',
      price: 9.99,
      frequency: '/mois',
      features: [
        'Accès à l\'interface de chat IA',
        'Programmes d\'entraînement personnalisés',
        '1 discipline au choix',
        'Génération de 2 programmes par mois'
      ]
    },
    {
      id: 'premium',
      title: 'Coaching Premium',
      price: 19.99,
      frequency: '/mois',
      features: [
        'Toutes les fonctionnalités Basique',
        'Toutes les disciplines disponibles',
        'Génération illimitée de programmes',
        'Suivi de progression personnalisé',
        'Adaptations hebdomadaires des programmes'
      ],
      isPopular: true
    },
    {
      id: 'elite',
      title: 'Coaching Elite',
      price: 39.99,
      frequency: '/mois',
      features: [
        'Toutes les fonctionnalités Premium',
        'Coach humain dédié',
        'Consultation personnelle mensuelle',
        'Support WhatsApp prioritaire',
        'Programmes sur mesure avec vidéos explicatives',
        'Analyses avancées de performances'
      ]
    }
  ];

  const socialLinks = [
    { name: 'WhatsApp', icon: 'whatsapp', url: 'https://wa.me/votrenuméro', color: '#25D366' },
    { name: 'Instagram', icon: 'instagram', url: 'https://instagram.com/athly', color: '#E1306C' }
  ];

  return (
    <div className="contact-page">
      <section className="contact-hero">
        <h1>Transformez votre entraînement avec Athly</h1>
        <p>Obtenez un coaching personnalisé et un suivi adapté à vos objectifs</p>
      </section>

      <section className="pricing-section">
        <h2>Nos Formules</h2>
        <p className="pricing-subtitle">Choisissez l'offre qui correspond à vos besoins</p>
        
        <div className="pricing-cards">
          {pricingOptions.map(option => (
            <div 
              key={option.id} 
              className={`pricing-card ${option.isPopular ? 'popular' : ''}`}
            >
              {option.isPopular && <div className="popular-badge">Plus populaire</div>}
              <h3>{option.title}</h3>
              <div className="price">
                <span className="amount">{option.price}€</span>
                <span className="frequency">{option.frequency}</span>
              </div>
              <ul className="features-list">
                {option.features.map((feature, index) => (
                  <li key={index}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <button className="subscribe-button">S'abonner</button>
            </div>
          ))}
        </div>
      </section>

      <section className="contact-section">
        <h2>Nous Contacter</h2>
        <p>Des questions? Contactez-nous directement via WhatsApp ou Instagram</p>
        
        <div className="social-links">
          {socialLinks.map(link => (
            <a 
              key={link.name} 
              href={link.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="social-link"
              style={{ backgroundColor: link.color }}
            >
              <span className={`icon-${link.icon}`}></span>
              {link.name}
            </a>
          ))}
        </div>
      </section>

      <section className="contact-form">
        <h2>Demande d'Information</h2>
        <form>
          <div className="form-group">
            <label htmlFor="name">Nom complet</label>
            <input type="text" id="name" placeholder="Votre nom" required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" placeholder="Votre email" required />
          </div>
          <div className="form-group">
            <label htmlFor="phone">Téléphone</label>
            <input type="tel" id="phone" placeholder="Votre numéro de téléphone" />
          </div>
          <div className="form-group">
            <label htmlFor="message">Message</label>
            <textarea id="message" rows={4} placeholder="Comment pouvons-nous vous aider?" required></textarea>
          </div>
          <button type="submit" className="submit-button">Envoyer</button>
        </form>
      </section>

      <section className="faq-section">
        <h2>Questions Fréquentes</h2>
        <div className="faq-list">
          <div className="faq-item">
            <h3>Comment fonctionne le coaching IA?</h3>
            <p>Notre IA est entraînée avec des connaissances approfondies en sport et en programmation d'entraînement. Elle génère des programmes adaptés à vos besoins, votre niveau et vos objectifs. Vous pouvez interagir avec elle via notre interface de chat pour obtenir des conseils personnalisés.</p>
          </div>
          <div className="faq-item">
            <h3>Puis-je changer de formule à tout moment?</h3>
            <p>Oui, vous pouvez passer d'une formule à une autre à tout moment. La nouvelle tarification sera appliquée dès le prochain cycle de facturation.</p>
          </div>
          <div className="faq-item">
            <h3>Comment se déroule une séance avec un coach humain?</h3>
            <p>Les séances avec un coach humain se déroulent par visioconférence et durent environ 45 minutes. Votre coach analysera vos performances, ajustera votre programme et répondra à toutes vos questions.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ContactPage; 