import React, { createContext, useState, useEffect } from 'react';
import { storeService } from '../services/storeService';
import toast from 'react-hot-toast';
import { useAuth } from '../hooks/useAuth';

export const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      fetchCart();
    }
  }, [isAuthenticated]);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const cartData = await storeService.getCart();
      setCart(cartData);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    try {
      const updatedCart = await storeService.addToCart(productId, quantity);
      setCart(updatedCart);
      toast.success('Item added to cart');
      return updatedCart;
    } catch (error) {
      toast.error('Failed to add item to cart');
      throw error;
    }
  };

  const updateCartItem = async (itemId, quantity) => {
    try {
      const updatedCart = await storeService.updateCartItem(itemId, quantity);
      setCart(updatedCart);
      toast.success('Cart updated');
      return updatedCart;
    } catch (error) {
      toast.error('Failed to update cart');
      throw error;
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      const updatedCart = await storeService.removeFromCart(itemId);
      setCart(updatedCart);
      toast.success('Item removed from cart');
      return updatedCart;
    } catch (error) {
      toast.error('Failed to remove item');
      throw error;
    }
  };

  const clearCart = async () => {
    try {
      await storeService.clearCart();
      setCart(null);
      toast.success('Cart cleared');
    } catch (error) {
      toast.error('Failed to clear cart');
      throw error;
    }
  };

  const getCartTotal = () => {
    if (!cart || !cart.items) return 0;
    return cart.items.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getCartItemCount = () => {
    if (!cart || !cart.items) return 0;
    return cart.items.reduce((count, item) => count + item.quantity, 0);
  };

  const value = {
    cart,
    loading,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    refreshCart: fetchCart,
    getCartTotal,
    getCartItemCount,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};
