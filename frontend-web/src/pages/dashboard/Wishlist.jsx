import React, { useState } from 'react';
import { FiHeart, FiShoppingCart, FiTrash2 } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const Wishlist = () => {
  const [wishlistItems] = useState([]);

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">My Wishlist</h1>
          <p className="text-gray-400">Save your favorite products for later</p>
        </div>

        {wishlistItems.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <FiHeart className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Your Wishlist is Empty</h3>
              <p className="text-gray-400 mb-6">
                Browse our store and add products you love to your wishlist
              </p>
              <Button variant="primary" onClick={() => window.location.href = '/store'}>
                Browse Store
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {wishlistItems.map((item) => (
              <Card key={item.id} hover>
                <CardContent className="p-0">
                  <div className="aspect-square bg-dark-800 rounded-t-lg relative">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-full h-full object-cover rounded-t-lg"
                    />
                    <button className="absolute top-3 right-3 w-10 h-10 bg-red-500 rounded-full flex items-center justify-center hover:bg-red-600 transition-colors">
                      <FiHeart className="h-5 w-5 text-white fill-current" />
                    </button>
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-white mb-1">{item.name}</h3>
                    <p className="text-gray-400 text-sm mb-3">{item.description}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-white">GH₵ {item.price}</span>
                      <div className="flex gap-2">
                        <Button variant="primary" size="sm">
                          <FiShoppingCart className="h-4 w-4 mr-2" />
                          Add to Cart
                        </Button>
                        <Button variant="danger" size="sm">
                          <FiTrash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Wishlist;
