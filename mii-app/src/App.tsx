import { useState, useEffect, useCallback } from 'react';
import type { Mii, Event } from './types';
import { initialMiis, eventTemplates } from './miis';
import MiiFace from './components/MiiFace';
import EventFeed from './components/EventFeed';
import './App.css';

function generateEvent(miis: Mii[]): Event {
  const mii = miis[Math.floor(Math.random() * miis.length)];
  const template = eventTemplates[Math.floor(Math.random() * eventTemplates.length)];
  const friend = miis.find((m) => mii.friends.includes(m.id));
  const text = template.text
    .replace('{name}', mii.name)
    .replace('{friend}', friend?.name ?? 'someone');
  return {
    id: crypto.randomUUID(),
    miiId: mii.id,
    miiName: mii.name,
    text,
    timestamp: Date.now(),
    emoji: template.emoji,
  };
}

const moods: Mii['mood'][] = ['happy', 'content', 'sleepy', 'hungry', 'bored'];
const activities = [
  'reading by the window',
  'napping on the couch',
  'making tea',
  'staring out the window',
  'looking for snacks',
  'watering the plants',
  'humming softly',
  'reorganizing things',
  'watching clouds',
  'writing in a journal',
];

export default function App() {
  const [miis, setMiis] = useState<Mii[]>(initialMiis);
  const [events, setEvents] = useState<Event[]>([]);

  const tick = useCallback(() => {
    const event = generateEvent(miis);
    setEvents((prev) => [event, ...prev].slice(0, 30));

    setMiis((prev) =>
      prev.map((mii) => {
        if (mii.id !== event.miiId) return mii;
        const newHappiness = Math.min(100, mii.happiness + Math.floor(Math.random() * 8) - 2);
        return {
          ...mii,
          happiness: newHappiness,
          mood: moods[Math.floor(Math.random() * moods.length)],
          activity: activities[Math.floor(Math.random() * activities.length)],
        };
      })
    );
  }, [miis]);

  useEffect(() => {
    const interval = setInterval(tick, 5000);
    return () => clearInterval(interval);
  }, [tick]);

  return (
    <div className="app">
      <header className="header">
        <h1>🏝️ Mii Island</h1>
        <p>A chill little place. Everyone's doing fine.</p>
      </header>

      <div className="island">
        {miis.map((mii) => (
          <div key={mii.id} className="mii-slot">
            <MiiFace mii={mii} size={90} />
            <div className="happiness-bar">
              <div
                className="happiness-fill"
                style={{ width: `${mii.happiness}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="main">
        <EventFeed events={events} />
      </div>
    </div>
  );
}
