import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ChatMessage from '../components/ChatMessage';

const mockItem = {
  _id: 'abc123',
  user_id: 0,
  question: 'What is the weather?',
  answer: 'It is sunny today.',
};

describe('ChatMessage', () => {
  it('renders the question text', () => {
    render(<ChatMessage item={mockItem} />);
    expect(screen.getByText('What is the weather?')).toBeInTheDocument();
  });

  it('renders the answer text', () => {
    render(<ChatMessage item={mockItem} />);
    expect(screen.getByText('It is sunny today.')).toBeInTheDocument();
  });
});
