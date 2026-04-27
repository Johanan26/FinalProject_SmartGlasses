import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import LoadingBubble from '../components/LoadingBubble';

describe('LoadingBubble', () => {
  it('renders the sending indicator text', () => {
    render(<LoadingBubble />);
    expect(screen.getByText('Sending...')).toBeInTheDocument();
  });

  it('renders three animated bounce dots', () => {
    const { container } = render(<LoadingBubble />);
    const dots = container.querySelectorAll('.animate-bounce');
    expect(dots).toHaveLength(3);
  });
});
