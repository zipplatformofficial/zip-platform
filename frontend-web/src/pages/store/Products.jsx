import React, { useState, useEffect } from 'react';
import { FiSearch } from 'react-icons/fi';
import { storeService } from '../../services/storeService';
import { useCart } from '../../hooks/useCart';
import ProductCard from '../../components/store/ProductCard';
import Input from '../../components/ui/Input';
import Loading from '../../components/ui/Loading';
import toast from 'react-hot-toast';

const Products = () => {
  const { addToCart } = useCart();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const data = await storeService.getProducts();
      setProducts(Array.isArray(data) ? data : []);
    } catch (error) {
      toast.error('Failed to load products');
      console.error('Error fetching products:', error);
      setProducts([]); // Set empty array on error to prevent filter errors
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (product) => {
    try {
      await addToCart(product.id, 1);
    } catch (error) {
      console.error('Add to cart error:', error);
    }
  };

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="min-h-screen bg-midnight-950 pt-20 pb-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Auto Parts Store
          </h1>
          <p className="text-xl text-gray-400 mb-8">
            Genuine auto parts and accessories
          </p>

          <div className="max-w-md mx-auto">
            <Input
              placeholder="Search products..."
              icon={FiSearch}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {filteredProducts.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={handleAddToCart}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No products found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Products;
