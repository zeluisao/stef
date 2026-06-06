import type { Mii } from '../types';

const moodEmoji: Record<Mii['mood'], string> = {
  happy: '😊',
  content: '🙂',
  sleepy: '😴',
  hungry: '😋',
  bored: '😑',
};

interface Props {
  mii: Mii;
  size?: number;
}

export default function MiiFace({ mii, size = 80 }: Props) {
  const s = size;
  const cx = s / 2;
  const cy = s / 2;

  return (
    <div style={{ textAlign: 'center' }}>
      <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`}>
        {/* Head */}
        <ellipse cx={cx} cy={cy} rx={s * 0.42} ry={s * 0.45} fill={mii.skinTone} />
        {/* Hair */}
        <ellipse cx={cx} cy={cy * 0.45} rx={s * 0.38} ry={s * 0.28} fill={mii.hairColor} />
        {/* Eyes */}
        <ellipse cx={cx - s * 0.13} cy={cy - s * 0.05} rx={s * 0.07} ry={s * 0.09} fill="#fff" />
        <ellipse cx={cx + s * 0.13} cy={cy - s * 0.05} rx={s * 0.07} ry={s * 0.09} fill="#fff" />
        <circle cx={cx - s * 0.13} cy={cy - s * 0.04} r={s * 0.045} fill="#2C2C5E" />
        <circle cx={cx + s * 0.13} cy={cy - s * 0.04} r={s * 0.045} fill="#2C2C5E" />
        {/* Nose */}
        <ellipse cx={cx} cy={cy + s * 0.05} rx={s * 0.04} ry={s * 0.03} fill={mii.skinTone} stroke="#c8967a" strokeWidth="1" />
        {/* Mouth */}
        {mii.mood === 'happy' || mii.mood === 'content' ? (
          <path d={`M ${cx - s * 0.1} ${cy + s * 0.13} Q ${cx} ${cy + s * 0.22} ${cx + s * 0.1} ${cy + s * 0.13}`} fill="none" stroke="#c0555a" strokeWidth="2" strokeLinecap="round" />
        ) : mii.mood === 'sleepy' ? (
          <path d={`M ${cx - s * 0.08} ${cy + s * 0.16} Q ${cx} ${cy + s * 0.13} ${cx + s * 0.08} ${cy + s * 0.16}`} fill="none" stroke="#c0555a" strokeWidth="2" strokeLinecap="round" />
        ) : (
          <line x1={cx - s * 0.08} y1={cy + s * 0.16} x2={cx + s * 0.08} y2={cy + s * 0.16} stroke="#c0555a" strokeWidth="2" strokeLinecap="round" />
        )}
        {/* Shirt collar */}
        <ellipse cx={cx} cy={s * 0.95} rx={s * 0.28} ry={s * 0.12} fill={mii.shirtColor} />
      </svg>
      <div style={{ fontSize: '1.2em', marginTop: 2 }}>{moodEmoji[mii.mood]}</div>
      <div style={{ fontWeight: 600, fontSize: '0.85em', color: '#555' }}>{mii.name}</div>
      <div style={{ fontSize: '0.7em', color: '#888', maxWidth: 90, margin: '2px auto 0' }}>{mii.activity}</div>
    </div>
  );
}
