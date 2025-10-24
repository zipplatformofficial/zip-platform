import React from 'react';
import { FiShoppingCart, FiStar } from 'react-icons/fi';
import Card, { CardContent, CardTitle, CardFooter } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { formatCurrency } from '../../utils/formatters';

const ProductCard = ({ product, onAddToCart }) => {
  return (
    <Card hover>
      {product.images && product.images[0] && (
        <img
          src={product.images[0]}
          alt={product.name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      )}

      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-2">
          <CardTitle className="text-lg">{product.name}</CardTitle>
          {product.in_stock ? (
            <Badge variant="success" size="sm">In Stock</Badge>
          ) : (
            <Badge variant="danger" size="sm">Out of Stock</Badge>
          )}
        </div>

        <p className="text-gray-400 text-sm mb-3 line-clamp-2">
          {product.description}
        </p>

        <div className="flex items-center gap-2 mb-3">
          <div className="flex items-center">
            <FiStar className="h-4 w-4 text-yellow-500 fill-current" />
            <span className="text-sm text-gray-400 ml-1">
              {product.average_rating || '0.0'}
            </span>
          </div>
          <span className="text-gray-600">•</span>
          <span className="text-sm text-gray-400">
            {product.stock_quantity} available
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-red-500 font-bold text-xl">
            {formatCurrency(product.price)}
          </span>
        </div>
      </CardContent>

      <CardFooter>
        <Button
          variant="primary"
          size="sm"
          className="w-full"
          onClick={() => onAddToCart(product)}
          disabled={!product.in_stock}
        >
          <FiShoppingCart className="mr-2 h-4 w-4" />
          Add to Cart
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;
