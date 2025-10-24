import React, { useState } from 'react';
import { FiCreditCard, FiPlus, FiTrash2 } from 'react-icons/fi';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const PaymentMethods = () => {
  const [paymentMethods] = useState([
    {
      id: 1,
      type: 'Mobile Money',
      number: '**** **** **** 1234',
      provider: 'MTN',
      isDefault: true,
    },
  ]);

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Payment Methods</h1>
            <p className="text-gray-400">Manage your payment methods for faster checkout</p>
          </div>
          <Button variant="primary">
            <FiPlus className="h-4 w-4 mr-2" />
            Add Payment Method
          </Button>
        </div>

        {/* Payment Methods List */}
        <div className="space-y-4">
          {paymentMethods.length === 0 ? (
            <Card>
              <CardContent className="p-12 text-center">
                <FiCreditCard className="h-16 w-16 text-gray-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No Payment Methods</h3>
                <p className="text-gray-400 mb-6">Add a payment method to speed up checkout</p>
                <Button variant="primary">
                  <FiPlus className="h-4 w-4 mr-2" />
                  Add Payment Method
                </Button>
              </CardContent>
            </Card>
          ) : (
            paymentMethods.map((method) => (
              <Card key={method.id} hover>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-16 h-16 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                        <FiCreditCard className="h-8 w-8 text-white" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-semibold text-white">{method.type}</h3>
                          {method.isDefault && (
                            <span className="px-2 py-0.5 bg-green-500/10 text-green-500 text-xs rounded-full">
                              Default
                            </span>
                          )}
                        </div>
                        <p className="text-gray-400">{method.provider} - {method.number}</p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {!method.isDefault && (
                        <Button variant="outline" size="sm">
                          Set as Default
                        </Button>
                      )}
                      <Button variant="danger" size="sm">
                        <FiTrash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Supported Payment Methods */}
        <Card className="mt-8">
          <CardTitle className="p-6 pb-0">Supported Payment Methods</CardTitle>
          <CardContent className="p-6">
            <div className="grid md:grid-cols-3 gap-4">
              <div className="p-4 border border-dark-700 rounded-lg text-center">
                <div className="text-2xl mb-2">📱</div>
                <p className="text-white font-medium">Mobile Money</p>
                <p className="text-gray-400 text-sm">MTN, Vodafone, AirtelTigo</p>
              </div>
              <div className="p-4 border border-dark-700 rounded-lg text-center">
                <div className="text-2xl mb-2">💳</div>
                <p className="text-white font-medium">Cards</p>
                <p className="text-gray-400 text-sm">Visa, Mastercard</p>
              </div>
              <div className="p-4 border border-dark-700 rounded-lg text-center">
                <div className="text-2xl mb-2">🏦</div>
                <p className="text-white font-medium">Bank Transfer</p>
                <p className="text-gray-400 text-sm">All major banks</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PaymentMethods;
