import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

interface EnhancedLogoProps {
  size?: 'small' | 'medium' | 'large' | 'hero';
  showText?: boolean;
  interactive?: boolean;
  className?: string;
  href?: string;
}

const EnhancedLogo: React.FC<EnhancedLogoProps> = ({
  size = 'medium',
  showText = true,
  interactive = true,
  className = '',
  href = '/'
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const logoRef = useRef<HTMLDivElement>(null);

  const sizeConfig = {
    small: { img: 40, text: '1.3rem', gap: '0.6rem' },
    medium: { img: 48, text: '1.5rem', gap: '0.75rem' },
    large: { img: 80, text: '2rem', gap: '1rem' },
    hero: { img: 120, text: '3rem', gap: '1.5rem' }
  };

  const config = sizeConfig[size];

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!logoRef.current || !interactive || size === 'small') return;
    
    const rect = logoRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    setMousePosition({
      x: (e.clientX - centerX) / 30,
      y: (e.clientY - centerY) / 30
    });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setMousePosition({ x: 0, y: 0 });
  };

  const logoContent = (
    <div
      ref={logoRef}
      className={`enhanced-logo ${className} ${interactive ? 'interactive' : ''} ${size}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
      onMouseMove={handleMouseMove}
      style={{
        transform: interactive && size !== 'small'
          ? `translate(${mousePosition.x}px, ${mousePosition.y}px) ${isHovered ? 'scale(1.05)' : 'scale(1)'}` 
          : interactive && isHovered ? 'scale(1.02)' : undefined
      }}
    >
      {/* Floating particles effect */}
      {interactive && isHovered && size !== 'small' && (
        <div className="particles-container">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="particle"
              style={{
                animationDelay: `${i * 0.1}s`,
                transform: `rotate(${i * 60}deg)`
              }}
            />
          ))}
        </div>
      )}

      {/* Glow effect */}
      {interactive && size !== 'small' && (
        <div className="logo-glow" style={{ opacity: isHovered ? 1 : 0 }} />
      )}

      {/* Logo image */}
      <div className="logo-image-container">
        <img 
          src="/logo.png" 
          alt="Athly Logo" 
          width={config.img}
          height={config.img}
          className="logo-image"
        />
        
        {/* Shine effect */}
        {interactive && <div className="shine-effect" />}
      </div>

      {/* Logo text */}
      {showText && (
        <div className="logo-text-container">
          <span className="logo-text">
            {'Athly'.split('').map((letter, index) => (
              <span 
                key={index}
                className="logo-letter"
                style={{ 
                  animationDelay: interactive && isHovered ? `${index * 0.1}s` : '0s' 
                }}
              >
                {letter}
              </span>
            ))}
          </span>
          
          {/* Animated underline */}
          {interactive && (
            <div className="logo-underline" style={{ width: isHovered ? '100%' : '0%' }} />
          )}
        </div>
      )}

      <style jsx>{`
        .enhanced-logo {
          display: flex;
          align-items: center;
          gap: ${config.gap};
          text-decoration: none;
          position: relative;
          transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
          z-index: 1;
          height: fit-content;
        }

        .enhanced-logo.interactive {
          cursor: pointer;
        }

        .enhanced-logo:focus {
          outline: 2px solid var(--primary);
          outline-offset: 4px;
          border-radius: var(--radius-md);
        }

        .particles-container {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          pointer-events: none;
          z-index: -1;
        }

        .particle {
          position: absolute;
          width: 3px;
          height: 3px;
          background: var(--gradient-primary);
          border-radius: 50%;
          animation: particleFloat 2s ease-in-out infinite;
        }

        @keyframes particleFloat {
          0%, 100% { 
            transform: translateY(0) scale(0);
            opacity: 0;
          }
          50% { 
            transform: translateY(-15px) scale(1);
            opacity: 1;
          }
        }

        .logo-glow {
          position: absolute;
          top: -8px;
          left: -8px;
          right: -8px;
          bottom: -8px;
          background: var(--gradient-primary);
          border-radius: 50%;
          filter: blur(15px);
          transition: opacity 0.4s ease;
          z-index: -1;
        }

        .logo-image-container {
          position: relative;
          overflow: hidden;
          border-radius: var(--radius-md);
          transition: all 0.4s ease;
          flex-shrink: 0;
        }

        .logo-image {
          border-radius: var(--radius-md);
          transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
          box-shadow: var(--shadow-sm);
          display: block;
        }

        .enhanced-logo.interactive:hover .logo-image {
          box-shadow: var(--shadow-md), 0 0 20px rgba(255, 92, 151, 0.3);
          filter: brightness(1.1) saturate(1.2);
        }

        .shine-effect {
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.3) 50%,
            transparent 70%
          );
          transform: translateX(-100%);
          transition: transform 0.6s ease;
        }

        .enhanced-logo.interactive:hover .shine-effect {
          transform: translateX(100%);
        }

        .logo-text-container {
          position: relative;
          overflow: hidden;
          display: flex;
          align-items: center;
        }

        .logo-text {
          font-size: ${config.text};
          font-weight: 800;
          background: var(--gradient-primary);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          font-family: 'Poppins', sans-serif;
          letter-spacing: -0.02em;
          display: flex;
          line-height: 1;
        }

        .logo-letter {
          display: inline-block;
          transition: all 0.3s ease;
        }

        .enhanced-logo.interactive:hover .logo-letter {
          animation: letterBounce 0.6s ease-in-out;
        }

        @keyframes letterBounce {
          0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-6px);
          }
          60% {
            transform: translateY(-3px);
          }
        }

        .logo-underline {
          position: absolute;
          bottom: -2px;
          left: 0;
          height: 2px;
          background: var(--gradient-primary);
          border-radius: 1px;
          transition: width 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        /* Size-specific adjustments */
        .enhanced-logo.hero {
          flex-direction: column;
          text-align: center;
          gap: 1rem;
        }

        .enhanced-logo.hero .logo-text {
          font-size: clamp(2rem, 5vw, 3.5rem);
        }

        .enhanced-logo.small .logo-text {
          font-weight: 700;
        }

        /* Header specific styles */
        .enhanced-logo.small {
          min-height: 40px;
          max-height: 50px;
        }

        .enhanced-logo.small .logo-image {
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .enhanced-logo.small.interactive:hover .logo-image {
          box-shadow: 0 4px 12px rgba(255, 92, 151, 0.2);
          filter: brightness(1.05);
        }

        .enhanced-logo.small .logo-text {
          font-weight: 700;
        }

        /* Accessibility */
        @media (prefers-reduced-motion: reduce) {
          .enhanced-logo,
          .logo-image,
          .logo-letter,
          .shine-effect,
          .particle {
            animation: none !important;
            transition: none !important;
          }
        }

        /* Dark mode optimizations */
        @media (prefers-color-scheme: dark) {
          .logo-image {
            filter: brightness(1.1);
          }
        }
      `}</style>
    </div>
  );

  if (href) {
    return (
      <Link href={href} className="logo-link">
        {logoContent}
        <style jsx>{`
          .logo-link {
            text-decoration: none;
            display: inline-flex;
          }
        `}</style>
      </Link>
    );
  }

  return logoContent;
};

export default EnhancedLogo; 