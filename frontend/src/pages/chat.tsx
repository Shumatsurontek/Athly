import React from 'react';
import Head from 'next/head';
import ChatInterface from '../components/ChatInterface';

const ChatPage: React.FC = () => {
  return (
    <div className="chat-page">
      <Head>
        <title>Chat avec Athly - Votre coach sportif IA</title>
        <meta name="description" content="Discutez avec Athly, votre coach sportif IA personnel et obtenez des conseils adaptés à vos besoins." />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <ChatInterface />
    </div>
  );
};

export default ChatPage; 