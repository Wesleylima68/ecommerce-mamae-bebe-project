import { render, screen } from '@testing-library/react';
import App from './App';

test('renderiza pagina inicial', () => {
  render(<App />);
  const titleElement = screen.getByText(/Bem-vindo\(a\) ao Mamãe & Bebê/i);
  expect(titleElement).toBeInTheDocument();
});
