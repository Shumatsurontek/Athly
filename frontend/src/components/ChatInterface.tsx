import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import rehypeRaw from 'rehype-raw';
import '../styles/Chat.css';

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
    backgroundColor: '#4F46E5',
    color: 'white',
    fontWeight: 'bold',
  },
  tableCell: {
    border: '1px solid #e2e8f0',
    padding: '0.5rem',
  },
  tableRow: {
    backgroundColor: 'transparent',
  },
  tableRowOdd: {
    backgroundColor: '#f8fafc',
  },
  tableRowHover: {
    backgroundColor: '#f1f5f9',
  },
  pre: {
    backgroundColor: '#f1f5f9',
    padding: '1rem',
    borderRadius: '0.5rem',
    overflowX: 'auto' as const,
    fontSize: '0.9rem',
    marginTop: '0.5rem',
    marginBottom: '0.5rem',
  },
  code: {
    backgroundColor: '#f1f5f9',
    padding: '0.2rem 0.4rem',
    borderRadius: '0.25rem',
    fontSize: '0.9rem',
  },
  h1: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginTop: '1.5rem',
    marginBottom: '0.5rem',
  },
  h2: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginTop: '1.25rem',
    marginBottom: '0.5rem',
  },
  h3: {
    fontSize: '1.125rem',
    fontWeight: 'bold',
    marginTop: '1rem',
    marginBottom: '0.5rem',
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
      text: "Bonjour ! Je suis votre coach Athly. Comment puis-je vous aider avec votre entraînement aujourd'hui ?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fonction pour améliorer le formatage du texte
  const formatMarkdown = (text: string): string => {
    // Ajouter des sauts de ligne avant les éléments numérotés
    let formattedText = text.replace(/(\d+\.\s+)/g, '\n\n$1');
    
    // Ajouter des sauts de ligne avant les éléments à puces
    formattedText = formattedText.replace(/(\s*-\s+)/g, '\n\n- ');
    
    // Ajouter des sauts de ligne avant les titres
    formattedText = formattedText.replace(/(#+\s+)/g, '\n\n$1');
    
    // Améliorer le formatage des tableaux en ajoutant des lignes vides
    formattedText = formattedText.replace(/(\|[-]+\|)/g, '$1\n');
    
    // Assurer des espaces après la ponctuation
    formattedText = formattedText.replace(/([,.])(\S)/g, '$1 $2');
    
    // Remplacer les étoiles sans espace par des étoiles avec espace pour le gras
    formattedText = formattedText.replace(/(\S)(\*\*)(\S)/g, '$1 $2$3');
    
    // Séparer les sections avec des sauts de ligne
    formattedText = formattedText.replace(/(###\s+.*?)(\n\d+\.)/g, '$1\n\n$2');
    
    return formattedText;
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message
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
      // Send message to backend
      const response = await axios.post('/api/chat', {
        message: input
      });
      
      // Check if the response contains a training program
      const isProgram = input.toLowerCase().includes('programme') && 
                        (response.data.message.includes('Programme Semaine') || 
                         response.data.message.includes('Votre Programme Personnalisé'));
      
      // Format the response text
      const formattedText = formatMarkdown(response.data.message);
      
      // Add AI response
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
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: "Désolé, j'ai rencontré une erreur. Pouvez-vous réessayer?",
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const downloadAsExcel = async (programText: string, messageId: string) => {
    if (isExporting) return;
    
    setIsExporting(messageId);
    
    try {
      const response = await axios.post('/api/convert-to-excel', 
        { content: programText }, 
        { responseType: 'blob' }
      );
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'programme_entrainement.xlsx');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Erreur lors de la génération du fichier Excel:', error);
      alert('Une erreur est survenue lors de la génération du fichier Excel.');
    } finally {
      setIsExporting(null);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-title">
          <img src="/logo.png" alt="Athly Logo" className="chat-logo" />
          <h2>Coach Athly</h2>
        </div>
        <p className="chat-subtitle">Votre coach IA personnel</p>
      </div>
      
      <div className="messages-container">
        {messages.map(message => (
          <div
            key={message.id} 
            className={`message ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}
          >
            <div className="message-content">
              {message.sender === 'user' ? (
                <p>{message.text}</p>
              ) : (
                <div className="markdown-content">
                  <ReactMarkdown 
                    remarkPlugins={[remarkGfm, remarkBreaks]} 
                    rehypePlugins={[rehypeRaw]}
                  >
                    {message.text}
                  </ReactMarkdown>
                  {message.isProgram && (
                    <button 
                      className={`download-program-btn ${isExporting === message.id ? 'loading' : ''}`}
                      onClick={() => downloadAsExcel(message.text, message.id)}
                      disabled={isExporting !== null}
                    >
                      {isExporting === message.id ? 'Génération Excel...' : 'Télécharger en Excel'}
                    </button>
                  )}
                </div>
              )}
              <span className="message-time">{formatTime(message.timestamp)}</span>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message ai-message">
            <div className="message-content typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Posez une question à votre coach..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </form>
      
      <div className="chat-suggestions">
        <p>Suggestions:</p>
        <div className="suggestion-chips">
          <button 
            onClick={() => setInput("Créez-moi un programme de course à pied sur 8 semaines")}
            className="suggestion-chip"
          >
            Programme de course 8 semaines
          </button>
          <button 
            onClick={() => setInput("Comment améliorer ma technique de squat ?")}
            className="suggestion-chip"
          >
            Améliorer ma technique de squat
          </button>
          <button 
            onClick={() => setInput("Quels exercices au poids du corps pour renforcer mon dos ?")}
            className="suggestion-chip"
          >
            Exercices de dos au poids du corps
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 