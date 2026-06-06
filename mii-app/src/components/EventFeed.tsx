import type { Event } from '../types';

interface Props {
  events: Event[];
}

function timeAgo(ts: number): string {
  const secs = Math.floor((Date.now() - ts) / 1000);
  if (secs < 5) return 'just now';
  if (secs < 60) return `${secs}s ago`;
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins}m ago`;
  return `${Math.floor(mins / 60)}h ago`;
}

export default function EventFeed({ events }: Props) {
  return (
    <div className="feed">
      <h2>🌴 Island Log</h2>
      {events.length === 0 && <p className="feed-empty">Nothing happening yet... it's very peaceful.</p>}
      <ul>
        {events.map((e) => (
          <li key={e.id} className="feed-item">
            <span className="feed-emoji">{e.emoji}</span>
            <span className="feed-text">{e.text}</span>
            <span className="feed-time">{timeAgo(e.timestamp)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
