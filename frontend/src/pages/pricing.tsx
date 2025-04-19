import React from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import ContactPage from '../components/ContactPage';

const PricingPage: React.FC = () => {
  const router = useRouter();
  
  React.useEffect(() => {
    // Redirect to contact page with the pricing section focused
    router.push('/contact');
  }, [router]);

  return (
    <div>
      <Head>
        <title>Tarifs - Athly</title>
        <meta name="description" content="Découvrez nos formules d'abonnement pour Athly, votre coach sportif IA personnel." />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="loading">Redirection vers nos formules...</div>
    </div>
  );
};

export default PricingPage; 