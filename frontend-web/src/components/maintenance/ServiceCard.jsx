import React from 'react';
import { FiClock, FiDollarSign } from 'react-icons/fi';
import Card, { CardContent, CardTitle, CardDescription, CardFooter } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { formatCurrency } from '../../utils/formatters';

const ServiceCard = ({ service, onBook }) => {
  return (
    <Card hover className="group">
      <CardTitle className="group-hover:text-red-500 transition-colors duration-300">{service.name}</CardTitle>
      <CardDescription className="mt-2 mb-4">
        {service.description}
      </CardDescription>

      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center text-gray-400 group-hover:text-white transition-colors duration-300">
              <FiClock className="h-4 w-4 mr-2 group-hover:animate-pulse-slow" />
              <span className="text-sm">{service.estimated_duration} mins</span>
            </div>
            <Badge variant="primary" className="group-hover:scale-110 transition-transform duration-300">
              {formatCurrency(service.base_price)}
            </Badge>
          </div>

          {service.includes && service.includes.length > 0 && (
            <div>
              <p className="text-sm font-medium text-gray-400 mb-2">Includes:</p>
              <ul className="text-sm text-gray-500 space-y-1">
                {service.includes.slice(0, 3).map((item, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-red-500 mr-2">•</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter>
        <Button
          variant="primary"
          size="sm"
          className="w-full"
          onClick={() => onBook(service)}
        >
          Book Service
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ServiceCard;
