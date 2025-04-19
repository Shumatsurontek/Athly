import React, { useState } from 'react';
import Head from 'next/head';
import ProgramGenerator from '../components/ProgramGenerator';

const GeneratorPage: React.FC = () => {
  const [generatedProgram, setGeneratedProgram] = useState<string | null>(null);

  const handleProgramGenerated = (program: string) => {
    setGeneratedProgram(program);
  };

  return (
    <div className="generator-page">
      <Head>
        <title>Générateur de Programme - Athly</title>
        <meta name="description" content="Créez votre programme d'entraînement personnalisé avec Athly, votre coach sportif IA." />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      {!generatedProgram ? (
        <ProgramGenerator onProgramGenerated={handleProgramGenerated} />
      ) : (
        <div className="program-result">
          <h2>Votre Programme Personnalisé</h2>
          <div className="program-content">
            {generatedProgram.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
          <button 
            className="primary-button"
            onClick={() => setGeneratedProgram(null)}
          >
            Générer un nouveau programme
          </button>
        </div>
      )}
    </div>
  );
};

export default GeneratorPage; 