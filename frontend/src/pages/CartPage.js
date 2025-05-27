// frontend/src/pages/CartPage.js
import React from 'react';

const CartPage = () => {
  return (
    <div className="container mx-auto p-8">
      <h2 className="text-3xl font-bold text-pink-700 mb-6 text-center">Seu Carrinho de Compras</h2>
      <p className="text-gray-700 text-center">Detalhes dos itens no seu carrinho serão exibidos aqui.</p>
      {/* Lógica do carrinho de compras e checkout virá aqui */}
    </div>
  );
};

export default CartPage;