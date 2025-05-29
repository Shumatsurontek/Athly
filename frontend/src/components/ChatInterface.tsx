import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import rehypeRaw from 'rehype-raw';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: Date;
  isProgram?: boolean;
}

// Correction des styles pour respecter les types CSSProperties
const markdownStyles = {
  table: {
    borderCollapse: 'collapse' as const,
    width: '100%',
    marginTop: '1rem',
    marginBottom: '1rem',
    fontSize: '0.9rem',
  },
  tableHead: {
    backgroundColor: '#FF6B9D',
    color: 'white',
    fontWeight: 'bold',
  },
  tableCell: {
    border: '1px solid rgba(255, 255, 255, 0.1)',
    padding: '0.5rem',
  },
  tableRow: {
    backgroundColor: 'transparent',
  },
  tableRowOdd: {
    backgroundColor: 'rgba(255, 255, 255, 0.02)',
  },
  tableRowHover: {
    backgroundColor: 'rgba(255, 107, 157, 0.1)',
  },
  pre: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    padding: '1rem',
    borderRadius: '0.5rem',
    overflowX: 'auto' as const,
    fontSize: '0.9rem',
    marginTop: '0.5rem',
    marginBottom: '0.5rem',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  },
  code: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    padding: '0.2rem 0.4rem',
    borderRadius: '0.25rem',
    fontSize: '0.9rem',
    color: '#4ECDC4',
  },
  h1: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginTop: '1.5rem',
    marginBottom: '0.5rem',
    background: 'linear-gradient(135deg, #FF6B9D, #4ECDC4)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  h2: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginTop: '1.25rem',
    marginBottom: '0.5rem',
    color: '#4ECDC4',
  },
  h3: {
    fontSize: '1.125rem',
    fontWeight: 'bold',
    marginTop: '1rem',
    marginBottom: '0.5rem',
    color: '#FFD93D',
  },
  listItem: {
    marginLeft: '1.5rem',
    listStyleType: 'disc',
  },
  orderedListItem: {
    marginLeft: '1.5rem',
    listStyleType: 'decimal',
  },
};

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'ai',
      text: "Salut ! 🤖 Je suis votre coach IA Athly ! Prêt à transformer votre entraînement ? Posez-moi vos questions sur le fitness, la course à pied, la musculation ou demandez-moi de créer un programme personnalisé !",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState<string | null>(null);
  const [currentMascot, setCurrentMascot] = useState<'robot' | 'fox'>('robot');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Suggestions prédéfinies améliorées
  const suggestions = [
    "Créer un programme de course débutant",
    "Programme musculation prise de masse",
    "Exercices poids du corps pour débutants",
    "Plan entraînement marathon",
    "Conseils nutrition pré-entraînement",
    "Comment éviter les blessures ?",
    "Programme HIIT 20 minutes",
    "Routine étirements post-workout"
  ];

  const formatMarkdown = (text: string): string => {
    let formattedText = text.replace(/(\d+\.\s+)/g, '\n\n$1');
    formattedText = formattedText.replace(/(\s*-\s+)/g, '\n\n- ');
    formattedText = formattedText.replace(/(#+\s+)/g, '\n\n$1');
    formattedText = formattedText.replace(/(\|[-]+\|)/g, '$1\n');
    formattedText = formattedText.replace(/([,.])(\S)/g, '$1 $2');
    formattedText = formattedText.replace(/(\S)(\*\*)(\S)/g, '$1 $2$3');
    formattedText = formattedText.replace(/(###\s+.*?)(\n\d+\.)/g, '$1\n\n$2');
    return formattedText;
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Changer de mascotte aléatoirement
    const interval = setInterval(() => {
      setCurrentMascot(prev => prev === 'robot' ? 'fox' : 'robot');
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await axios.post('/api/chat', {
        message: input
      });
      
      const isProgram = input.toLowerCase().includes('programme') && 
                        (response.data.message.includes('Programme Semaine') || 
                         response.data.message.includes('Votre Programme Personnalisé'));
      
      const formattedText = formatMarkdown(response.data.message);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: formattedText,
        timestamp: new Date(),
        isProgram
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Erreur lors de la communication avec l\'IA:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: "Oups ! 🤖 J'ai rencontré un petit problème technique. Pouvez-vous réessayer ? Je suis là pour vous aider !",
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const exportToPDF = async (messageId: string) => {
    setIsExporting(messageId);
    
    try {
      const message = messages.find(m => m.id === messageId);
      if (!message) return;

      const response = await axios.post('/api/export-pdf', {
        content: message.text,
        filename: `programme-athly-${new Date().toISOString().split('T')[0]}.pdf`
      }, {
        responseType: 'blob'
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `programme-athly-${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erreur lors de l\'export PDF:', error);
    } finally {
      setIsExporting(null);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="athly-chat-container">
      {/* Header amélioré avec mascotte */}
      <div className="athly-chat-header">
        <div className="athly-chat-title">
          <div className="athly-chat-mascot">
            <img 
              src={currentMascot === 'robot' ? "/robot.png" : "/fox.png"} 
              alt={currentMascot === 'robot' ? "Robot Coach" : "Fox Athly"} 
              className="athly-mascot-animated"
            />
          </div>
          <div className="athly-chat-info">
            <h1>Coach IA Athly</h1>
            <p>Votre assistant personnel pour l'entraînement</p>
          </div>
        </div>
        <div className="athly-chat-status">
          <div className="athly-status-indicator">
            <div className="athly-status-dot"></div>
            <span>En ligne</span>
          </div>
        </div>
      </div>

      {/* Messages avec design amélioré */}
      <div className="athly-messages-container">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`athly-message ${message.sender === 'user' ? 'athly-user-message' : 'athly-ai-message'}`}
          >
            {message.sender === 'ai' && (
              <div className="athly-message-avatar">
                <img src="/robot.png" alt="Coach IA" />
              </div>
            )}
            
            <div className="athly-message-content">
              <div className="athly-message-bubble">
                <div className="athly-markdown-content">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm, remarkBreaks]}
                    rehypePlugins={[rehypeRaw]}
                    components={{
                      table: ({ children }) => (
                        <table style={markdownStyles.table}>
                          {children}
                        </table>
                      ),
                      thead: ({ children }) => (
                        <thead style={markdownStyles.tableHead}>
                          {children}
                        </thead>
                      ),
                      th: ({ children }) => (
                        <th style={markdownStyles.tableCell}>
                          {children}
                        </th>
                      ),
                      td: ({ children }) => (
                        <td style={markdownStyles.tableCell}>
                          {children}
                        </td>
                      ),
                      tr: ({ children, ...props }) => (
                        <tr style={markdownStyles.tableRow}>
                          {children}
                        </tr>
                      ),
                      pre: ({ children }) => (
                        <pre style={markdownStyles.pre}>
                          {children}
                        </pre>
                      ),
                      code: ({ children, inline }) => (
                        inline ? (
                          <code style={markdownStyles.code}>
                            {children}
                          </code>
                        ) : (
                          <code>{children}</code>
                        )
                      ),
                      h1: ({ children }) => (
                        <h1 style={markdownStyles.h1}>
                          {children}
                        </h1>
                      ),
                      h2: ({ children }) => (
                        <h2 style={markdownStyles.h2}>
                          {children}
                        </h2>
                      ),
                      h3: ({ children }) => (
                        <h3 style={markdownStyles.h3}>
                          {children}
                        </h3>
                      ),
                      li: ({ children, ordered }) => (
                        <li style={ordered ? markdownStyles.orderedListItem : markdownStyles.listItem}>
                          {children}
                        </li>
                      ),
                    }}
                  >
                    {message.text}
                  </ReactMarkdown>
                </div>
                
                {message.isProgram && (
                  <div className="athly-program-actions">
                    <button
                      onClick={() => exportToPDF(message.id)}
                      disabled={isExporting === message.id}
                      className="athly-export-btn"
                    >
                      {isExporting === message.id ? (
                        <>
                          <div className="athly-spinner"></div>
                          Export en cours...
                        </>
                      ) : (
                        <>
                          📄 Télécharger PDF
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
              
              <div className="athly-message-time">
                {formatTime(message.timestamp)}
              </div>
            </div>

            {message.sender === 'user' && (
              <div className="athly-message-avatar athly-user-avatar">
                <div className="athly-user-icon">👤</div>
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="athly-message athly-ai-message">
            <div className="athly-message-avatar">
              <img src="/robot.png" alt="Coach IA" />
            </div>
            <div className="athly-message-content">
              <div className="athly-message-bubble">
                <div className="athly-typing-indicator">
                  <div className="athly-typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="athly-typing-text">Le coach réfléchit...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions améliorées */}
      {messages.length <= 1 && (
        <div className="athly-suggestions">
          <h4>💡 Suggestions pour commencer :</h4>
          <div className="athly-suggestion-chips">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="athly-suggestion-chip"
                onClick={() => handleSuggestionClick(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input amélioré */}
      <div className="athly-chat-input-section">
        <form onSubmit={handleSubmit} className="athly-chat-form">
          <div className="athly-input-container">
            <input
              type="text"
              value={input}
              onChange={handleInputChange}
              placeholder="Posez votre question au coach IA..."
              disabled={isLoading}
              className="athly-chat-input"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="athly-send-btn"
            >
              {isLoading ? (
                <div className="athly-spinner-small"></div>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </button>
          </div>
        </form>
        
        <div className="athly-chat-footer">
          <p>💬 Coach IA alimenté par la technologie Athly</p>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 