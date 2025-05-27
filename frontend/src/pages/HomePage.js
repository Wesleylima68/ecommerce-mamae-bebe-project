// frontend/src/pages/HomePage.js
import React from 'react';

const HomePage = () => {
  return (
    <div className="container mx-auto p-8 text-center">
      <h2 className="text-4xl font-bold text-pink-700 mb-4">Bem-vindo(a) ao Mamãe & Bebê!</h2>
      <p className="text-xl text-gray-700 mb-6">Tudo o que você precisa para esta fase tão especial.</p>
      <p className="mt-8 text-gray-600">
        Explore nossas categorias e encontre os melhores produtos para você e seu bebê.
      </p>
      {/* Conteúdo específico da Home Page virá aqui */}
    </div>
  );
};

export default HomePage;