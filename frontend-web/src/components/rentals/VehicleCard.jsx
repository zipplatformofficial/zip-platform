import React from 'react';
import { FiUsers, FiPackage, FiDollarSign } from 'react-icons/fi';
import Card, { CardContent, CardTitle, CardDescription, CardFooter } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { formatCurrency } from '../../utils/formatters';

const VehicleCard = ({ vehicle, onBook }) => {
  return (
    <Card hover>
      {vehicle.photos && vehicle.photos[0] && (
        <img
          src={vehicle.photos[0]}
          alt={vehicle.name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      )}

      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-2">
          <CardTitle>{vehicle.make} {vehicle.model}</CardTitle>
          <Badge variant={vehicle.is_available ? 'success' : 'danger'}>
            {vehicle.is_available ? 'Available' : 'Unavailable'}
          </Badge>
        </div>

        <p className="text-gray-400 text-sm mb-4">{vehicle.year}</p>

        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="flex items-center text-gray-400">
            <FiUsers className="h-4 w-4 mr-2 text-red-500" />
            <span>{vehicle.seats} Seats</span>
          </div>
          <div className="flex items-center text-gray-400">
            <FiPackage className="h-4 w-4 mr-2 text-red-500" />
            <span>{vehicle.transmission}</span>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-dark-700">
          <div className="flex items-center justify-between">
            <span className="text-gray-400 text-sm">Daily Rate</span>
            <span className="text-red-500 font-bold text-lg">
              {formatCurrency(vehicle.daily_rate)}
            </span>
          </div>
        </div>
      </CardContent>

      <CardFooter>
        <Button
          variant="primary"
          size="sm"
          className="w-full"
          onClick={() => onBook(vehicle)}
          disabled={!vehicle.is_available}
        >
          {vehicle.is_available ? 'Rent Now' : 'Unavailable'}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default VehicleCard;
