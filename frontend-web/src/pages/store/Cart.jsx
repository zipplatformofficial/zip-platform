import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../hooks/useCart';
import Card, { CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Loading from '../../components/ui/Loading';
import { formatCurrency } from '../../utils/formatters';
import { FiTrash2, FiShoppingBag } from 'react-icons/fi';

const Cart = () => {
  const navigate = useNavigate();
  const { cart, loading, updateCartItem, removeFromCart, getCartTotal } = useCart();

  const handleUpdateQuantity = async (itemId, quantity) => {
    if (quantity < 1) return;
    try {
      await updateCartItem(itemId, quantity);
    } catch (error) {
      console.error('Update quantity error:', error);
    }
  };

  const handleRemoveItem = async (itemId) => {
    try {
      await removeFromCart(itemId);
    } catch (error) {
      console.error('Remove item error:', error);
    }
  };

  const handleCheckout = () => {
    navigate('/store/checkout');
  };

  if (loading) {
    return <Loading fullScreen />;
  }

  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <div className="min-h-screen bg-midnight-950 pt-20 pb-12 px-4">
        <div className="max-w-3xl mx-auto">
          <Card>
            <div className="text-center py-12">
              <FiShoppingBag className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">Your cart is empty</h2>
              <p className="text-gray-400 mb-6">Add some products to get started!</p>
              <Button variant="primary" onClick={() => navigate('/store')}>
                Browse Products
              </Button>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-midnight-950 pt-20 pb-12 px-4">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Shopping Cart</h1>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            {cart.items.map((item) => (
              <Card key={item.id}>
                <CardContent className="p-6">
                  <div className="flex gap-4">
                    {item.product?.images?.[0] && (
                      <img
                        src={item.product.images[0]}
                        alt={item.product.name}
                        className="w-24 h-24 object-cover rounded-lg"
                      />
                    )}

                    <div className="flex-1">
                      <h3 className="text-white font-semibold mb-1">
                        {item.product?.name}
                      </h3>
                      <p className="text-gray-400 text-sm mb-3">
                        {formatCurrency(item.price)} each
                      </p>

                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                            className="w-8 h-8 rounded bg-dark-800 text-white hover:bg-dark-700"
                          >
                            -
                          </button>
                          <span className="text-white w-8 text-center">{item.quantity}</span>
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                            className="w-8 h-8 rounded bg-dark-800 text-white hover:bg-dark-700"
                          >
                            +
                          </button>
                        </div>

                        <button
                          onClick={() => handleRemoveItem(item.id)}
                          className="text-red-500 hover:text-red-400 flex items-center gap-1 text-sm"
                        >
                          <FiTrash2 className="h-4 w-4" />
                          Remove
                        </button>
                      </div>
                    </div>

                    <div className="text-right">
                      <p className="text-red-500 font-bold text-lg">
                        {formatCurrency(item.price * item.quantity)}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="lg:col-span-1">
            <Card className="sticky top-24">
              <CardContent className="p-6">
                <h3 className="text-white font-bold text-lg mb-4">Order Summary</h3>

                <div className="space-y-3 mb-6">
                  <div className="flex justify-between text-gray-400">
                    <span>Subtotal</span>
                    <span>{formatCurrency(getCartTotal())}</span>
                  </div>
                  <div className="flex justify-between text-gray-400">
                    <span>Delivery</span>
                    <span>Calculated at checkout</span>
                  </div>
                  <div className="border-t border-dark-700 pt-3 flex justify-between text-white font-bold text-lg">
                    <span>Total</span>
                    <span className="text-red-500">{formatCurrency(getCartTotal())}</span>
                  </div>
                </div>

                <Button
                  variant="primary"
                  size="lg"
                  className="w-full"
                  onClick={handleCheckout}
                >
                  Proceed to Checkout
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
