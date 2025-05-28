import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import EnhancedLogo from './EnhancedLogo';

const Header: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navigation = [
    { name: 'Accueil', href: '/' },
    { name: 'Générateur', href: '/generator' },
    { name: 'Chat IA', href: '/chat' },
    { name: 'Tarifs', href: '/pricing' },
    { name: 'Contact', href: '/contact' },
  ];

  const isActive = (path: string) => router.pathname === path;

  return (
    <>
      <header className={`athly-header ${isScrolled ? 'scrolled' : ''}`}>
        <div className="athly-header-container">
          {/* Logo Section */}
          <div className="athly-logo-section">
            <Link href="/" className="athly-logo-link">
              <img 
                src="/logo.png" 
                alt="Athly Logo" 
                width="40"
                height="40"
                className="athly-logo-image"
              />
              <span className="athly-logo-text">Athly</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="athly-desktop-nav">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`athly-nav-item ${isActive(item.href) ? 'active' : ''}`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* CTA Section */}
          <div className="athly-cta-section">
            <Link href="/generator" className="athly-cta-btn">
              <span>Commencer</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
          </div>

          {/* Mobile Menu Toggle */}
          <button
            className={`athly-mobile-toggle ${isMobileMenuOpen ? 'active' : ''}`}
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle navigation"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>

        {/* Mobile Navigation */}
        <div className={`athly-mobile-nav ${isMobileMenuOpen ? 'open' : ''}`}>
          <div className="athly-mobile-nav-content">
            <div className="athly-mobile-nav-header">
              <h3>Navigation</h3>
              <button 
                className="athly-close-btn"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                ×
              </button>
            </div>
            
            <div className="athly-mobile-nav-links">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`athly-mobile-nav-item ${isActive(item.href) ? 'active' : ''}`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <span>{item.name}</span>
                  {isActive(item.href) && <div className="athly-active-indicator"></div>}
                </Link>
              ))}
            </div>
            
            <div className="athly-mobile-cta">
              <Link 
                href="/generator" 
                className="athly-mobile-cta-btn"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Commencer maintenant
              </Link>
            </div>
          </div>
        </div>

        {/* Mobile Overlay */}
        {isMobileMenuOpen && (
          <div 
            className="athly-mobile-overlay"
            onClick={() => setIsMobileMenuOpen(false)}
          />
        )}
      </header>
    </>
  );
};

export default Header; 