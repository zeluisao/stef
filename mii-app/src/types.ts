export interface Mii {
  id: string;
  name: string;
  skinTone: string;
  hairColor: string;
  shirtColor: string;
  mood: 'happy' | 'content' | 'sleepy' | 'hungry' | 'bored';
  happiness: number; // 0-100
  activity: string;
  friends: string[];
}

export interface Event {
  id: string;
  miiId: string;
  miiName: string;
  text: string;
  timestamp: number;
  emoji: string;
}
