import React from 'react';
import Head from 'next/head';
import ContactPage from '../components/ContactPage';

const Contact: React.FC = () => {
  return (
    <div>
      <Head>
        <title>Contact - Athly</title>
        <meta name="description" content="Contactez-nous pour en savoir plus sur Athly, votre coach sportif IA personnel." />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <ContactPage />
    </div>
  );
};

export default Contact; 