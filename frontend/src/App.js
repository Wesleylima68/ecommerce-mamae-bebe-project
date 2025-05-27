// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Importe seus componentes de página
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import CartPage from './pages/CartPage';
import LoginPage from './pages/LoginPage';
import MyAccountPage from './pages/MyAccountPage';

// Componente de Cabeçalho (Header)
// Agora usando <Link> do React Router para navegação
const Header = () => {
  return (
    <header className="bg-pink-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-3xl font-bold">
          <Link to="/" className="hover:text-pink-200">👶 Mamãe & Bebê 💖</Link>
        </h1>
        <nav className="space-x-4">
          <Link to="/" className="text-lg font-medium hover:text-pink-200">Início</Link>
          <Link to="/produtos" className="text-lg font-medium hover:text-pink-200">Produtos</Link>
          <Link to="/minha-conta" className="text-lg font-medium hover:text-pink-200">Minha Conta</Link>
          <Link to="/carrinho" className="text-lg font-medium hover:text-pink-200">🛒 Carrinho</Link>
          <Link to="/login" className="text-lg font-medium hover:text-pink-200">Entrar</Link>
        </nav>
      </div>
    </header>
  );
};

// Componente de Rodapé (Footer) - Sem alterações
const Footer = () => {
  return (
    <footer className="bg-pink-700 text-white p-6 text-center text-sm">
      <div className="container mx-auto">
        <p>&copy; {new Date().getFullYear()} Mamãe & Bebê. Todos os direitos reservados.</p>
        <div className="mt-2 space-x-4">
          <a href="#" className="hover:underline">Política de Privacidade</a>
          <a href="#" className="hover:underline">Termos de Uso</a>
          <a href="#" className="hover:underline">Contato</a>
        </div>
      </div>
    </footer>
  );
};

// Componente Principal do Aplicativo (App)
function App() {
  return (
    <Router> {/* O Router envolve todo o aplicativo */}
      <div className="min-h-screen flex flex-col bg-pink-50">
        <Header />

        {/* A área principal onde as páginas serão renderizadas */}
        <main className="flex-grow py-8">
          <Routes> {/* As Routes definem as diferentes rotas */}
            <Route path="/" element={<HomePage />} />
            <Route path="/produtos" element={<ProductsPage />} />
            <Route path="/carrinho" element={<CartPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/minha-conta" element={<MyAccountPage />} />
            {/* Você pode adicionar uma rota para 404 Not Found aqui se quiser */}
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;