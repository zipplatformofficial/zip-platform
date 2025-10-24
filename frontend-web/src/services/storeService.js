import api from './api';

export const storeService = {
  async getProducts(params = {}) {
    const response = await api.get('/store/products', { params });
    return response.data;
  },

  async getProduct(id) {
    const response = await api.get(`/store/products/${id}`);
    return response.data;
  },

  async searchProducts(query) {
    const response = await api.get(`/store/products/search?q=${query}`);
    return response.data;
  },

  async getCart() {
    const response = await api.get('/store/cart');
    return response.data;
  },

  async addToCart(productId, quantity = 1) {
    const response = await api.post('/store/cart/add', {
      product_id: productId,
      quantity,
    });
    return response.data;
  },

  async updateCartItem(itemId, quantity) {
    const response = await api.put(`/store/cart/items/${itemId}`, { quantity });
    return response.data;
  },

  async removeFromCart(itemId) {
    const response = await api.delete(`/store/cart/items/${itemId}`);
    return response.data;
  },

  async clearCart() {
    const response = await api.delete('/store/cart/clear');
    return response.data;
  },

  async createOrder(orderData) {
    const response = await api.post('/store/orders', orderData);
    return response.data;
  },

  async getMyOrders() {
    const response = await api.get('/store/orders');
    return response.data;
  },

  async getOrder(id) {
    const response = await api.get(`/store/orders/${id}`);
    return response.data;
  },

  async cancelOrder(id) {
    const response = await api.put(`/store/orders/${id}/cancel`);
    return response.data;
  },
};

export default storeService;
