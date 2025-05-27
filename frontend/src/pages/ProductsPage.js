// frontend/src/pages/ProductsPage.js
import React from 'react';

const ProductsPage = () => {
  return (
    <div className="container mx-auto p-8">
      <h2 className="text-3xl font-bold text-pink-700 mb-6 text-center">Nossos Produtos</h2>
      <p className="text-gray-700 text-center">Aqui você encontrará uma vasta seleção de produtos para mamães e bebês.</p>
      {/* Lógica de busca, filtros e listagem de produtos virá aqui */}
    </div>
  );
};

export default ProductsPage;