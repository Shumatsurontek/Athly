import React, { useState } from 'react';
import axios from 'axios';

interface ProgramRequest {
  disciplines: string[];
  duration: number;
  level: string;
  goals: string;
  constraints: string;
  equipment: string;
  frequency: number;
  time_per_session: number;
}

interface ProgramGeneratorProps {
  onProgramGenerated: (program: any) => void;
}

const ProgramGenerator: React.FC<ProgramGeneratorProps> = ({ onProgramGenerated }) => {
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [formData, setFormData] = useState<ProgramRequest>({
    disciplines: [],
    duration: 8,
    level: 'débutant',
    goals: '',
    constraints: '',
    equipment: '',
    frequency: 3,
    time_per_session: 60
  });

  const disciplines = [
    { id: 'running', label: 'Course à pied' },
    { id: 'bodyweight', label: 'Poids de Corps' },
    { id: 'strength', label: 'Musculation' }
  ];

  const levels = [
    { id: 'débutant', label: 'Débutant' },
    { id: 'intermédiaire', label: 'Intermédiaire' },
    { id: 'avancé', label: 'Avancé' }
  ];

  const durations = [
    { weeks: 8, label: '8 semaines' },
    { weeks: 10, label: '10 semaines' },
    { weeks: 12, label: '12 semaines' },
    { weeks: 16, label: '16 semaines' }
  ];

  const handleDisciplineChange = (discipline: string) => {
    setFormData(prev => {
      const disciplines = [...prev.disciplines];
      if (disciplines.includes(discipline)) {
        return { ...prev, disciplines: disciplines.filter(d => d !== discipline) };
      } else {
        return { ...prev, disciplines: [...disciplines, discipline] };
      }
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration' || name === 'frequency' || name === 'time_per_session' 
        ? parseInt(value, 10) 
        : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.disciplines.length === 0) {
      alert('Veuillez sélectionner au moins une discipline');
      return;
    }

    setIsGenerating(true);

    try {
      const response = await axios.post('/api/generate-program', formData);
      onProgramGenerated(response.data.program);
    } catch (error) {
      console.error('Erreur lors de la génération du programme:', error);
      alert('Une erreur est survenue lors de la génération du programme.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="program-generator">
      <h2>Générer un Programme d'Entraînement Personnalisé</h2>
      
      <form onSubmit={handleSubmit} className="generator-form">
        <div className="form-section">
          <h3>Disciplines</h3>
          <p className="form-subtitle">Sélectionnez une ou plusieurs disciplines</p>
          <div className="discipline-options">
            {disciplines.map(discipline => (
              <div key={discipline.id} className="discipline-option">
                <input
                  type="checkbox"
                  id={`discipline-${discipline.id}`}
                  checked={formData.disciplines.includes(discipline.id)}
                  onChange={() => handleDisciplineChange(discipline.id)}
                />
                <label htmlFor={`discipline-${discipline.id}`}>{discipline.label}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="form-section">
          <h3>Durée du Programme</h3>
          <div className="duration-options">
            {durations.map(duration => (
              <div key={duration.weeks} className="duration-option">
                <input
                  type="radio"
                  id={`duration-${duration.weeks}`}
                  name="duration"
                  value={duration.weeks}
                  checked={formData.duration === duration.weeks}
                  onChange={handleInputChange}
                />
                <label htmlFor={`duration-${duration.weeks}`}>{duration.label}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="form-section">
          <h3>Niveau</h3>
          <select 
            name="level" 
            value={formData.level} 
            onChange={handleInputChange}
          >
            {levels.map(level => (
              <option key={level.id} value={level.id}>
                {level.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-section">
          <h3>Objectif Principal</h3>
          <textarea
            name="goals"
            value={formData.goals}
            onChange={handleInputChange}
            placeholder="Ex: Perdre du poids, améliorer l'endurance, préparer une compétition..."
            rows={3}
          />
        </div>

        <div className="form-section">
          <h3>Contraintes Physiques/Médicales</h3>
          <textarea
            name="constraints"
            value={formData.constraints}
            onChange={handleInputChange}
            placeholder="Ex: Douleur au genou, limitation d'amplitude d'épaule..."
            rows={3}
          />
        </div>

        <div className="form-section">
          <h3>Équipement Disponible</h3>
          <textarea
            name="equipment"
            value={formData.equipment}
            onChange={handleInputChange}
            placeholder="Ex: Haltères, barre, machines, élastiques..."
            rows={3}
          />
        </div>

        <div className="form-section form-row">
          <div className="form-column">
            <h3>Fréquence (jours/semaine)</h3>
            <input
              type="number"
              name="frequency"
              min={1}
              max={7}
              value={formData.frequency}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-column">
            <h3>Temps par séance (minutes)</h3>
            <input
              type="number"
              name="time_per_session"
              min={15}
              max={180}
              step={15}
              value={formData.time_per_session}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <button 
          type="submit" 
          className="generate-button" 
          disabled={isGenerating || formData.disciplines.length === 0}
        >
          {isGenerating ? 'Génération en cours...' : 'Générer mon Programme'}
        </button>
      </form>
    </div>
  );
};

export default ProgramGenerator; 